"""
Copia puntual (no programada) de los objetos de un bucket de GCS a otro,
pensada para llevar polizador-production-pdf -> polizador-dev-pdf una sola
vez. No es un sync continuo: para volver a alinear los buckets más adelante,
se vuelve a correr a mano.

Cada objeto se copia server-side (rewrite), sin bajarlo por este servidor, y
se lo puede dejar en una storage class distinta a la del origen (por defecto
COLDLINE, ya que en dev no hace falta acceso frecuente).

    python manage.py copiar_bucket_dev
    python manage.py copiar_bucket_dev --dry-run
    python manage.py copiar_bucket_dev --overwrite --storage-class NEARLINE
"""
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from google.cloud import storage

STORAGE_CLASSES = {"STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE"}


class Command(BaseCommand):
    help = "Copia (server-side) los objetos de un bucket GCS a otro. Copia puntual, no programada."

    def add_arguments(self, parser):
        parser.add_argument("--source", default="polizador-production-pdf", help="Bucket origen.")
        parser.add_argument("--destination", default="polizador-dev-pdf", help="Bucket destino.")
        parser.add_argument(
            "--storage-class", default="COLDLINE", choices=sorted(STORAGE_CLASSES),
            help="Storage class a asignar en destino (default: COLDLINE).",
        )
        parser.add_argument(
            "--overwrite", action="store_true",
            help="Volver a copiar objetos que ya existen en destino con el mismo tamaño (default: se saltean).",
        )
        parser.add_argument(
            "--dry-run", action="store_true",
            help="No copia nada, solo informa cuántos objetos copiaría/saltearía.",
        )

    def handle(self, *args, **options):
        if not settings.GS_CREDENTIALS:
            raise CommandError(
                "No hay credenciales de GCS cargadas (GS_CREDENTIALS es None). "
                "Falta polizador-production.json en BASE_DIR."
            )

        source_name = options["source"]
        destination_name = options["destination"]
        storage_class = options["storage_class"]
        overwrite = options["overwrite"]
        dry_run = options["dry_run"]

        client = storage.Client(credentials=settings.GS_CREDENTIALS, project=settings.GS_CREDENTIALS.project_id)
        source_bucket = client.bucket(source_name)
        destination_bucket = client.bucket(destination_name)

        self.stdout.write(f"Leyendo objetos existentes en gs://{destination_name}/...")
        existentes = {blob.name: blob.size for blob in client.list_blobs(destination_name)}
        self.stdout.write(f"  {len(existentes)} objeto(s) ya presentes en destino.")

        copiados = 0
        salteados = 0
        errores = 0

        for source_blob in client.list_blobs(source_name):
            tamano_existente = existentes.get(source_blob.name)
            if not overwrite and tamano_existente == source_blob.size:
                salteados += 1
                continue

            if dry_run:
                copiados += 1
                continue

            try:
                destination_blob = destination_bucket.blob(source_blob.name)
                destination_blob.storage_class = storage_class
                # rewrite() manda como body el resource completo de destination_blob: si solo
                # storage_class quedó seteado, GCS no hereda el resto de los metadatos del
                # origen (content_type termina None/octet-stream en destino, rompiendo la
                # previsualización inline de PDFs). Confirmado empíricamente, no es lo que dice
                # la documentación de la API. Hay que copiar a mano lo que sí nos importa.
                destination_blob.content_type = source_blob.content_type
                token = None
                while True:
                    token, _, _ = destination_blob.rewrite(source_blob, token=token)
                    if token is None:
                        break
                copiados += 1
            except Exception as exc:
                errores += 1
                self.stderr.write(f"  ERROR copiando {source_blob.name}: {exc}")

            if (copiados + salteados + errores) % 500 == 0:
                self.stdout.write(f"  ... {copiados} copiados, {salteados} salteados, {errores} error(es)")

        accion = "Se copiarían" if dry_run else "Copiados"
        self.stdout.write(self.style.SUCCESS(
            f"{accion} {copiados} objeto(s) a gs://{destination_name}/ "
            f"({salteados} ya estaban igual, {errores} error(es))."
        ))
