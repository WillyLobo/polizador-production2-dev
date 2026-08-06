"""
Corrige metadata de Content-Type faltante en objetos de un bucket de GCS.

Motivado por un bug en copiar_bucket_dev.py (ya corregido): al copiar objetos
server-side con rewrite() seteando storage_class de antemano, GCS no heredaba
el resto de los metadatos del objeto origen, dejando el Content-Type en blanco
(default application/octet-stream). Eso hace que los PDFs se descarguen en vez
de previsualizarse inline en el navegador. Este comando es la reparación
puntual de los objetos ya copiados con ese bug; no hace falta correrlo de
nuevo salvo que aparezca otro bucket/prefijo con el mismo problema.

No vuelve a copiar contenido (no hay transferencia de bytes): solo parchea
metadata via blob.patch(), en batches para no hacer una request HTTP por
objeto.

    python manage.py fix_bucket_content_type
    python manage.py fix_bucket_content_type --dry-run
    python manage.py fix_bucket_content_type --bucket polizador-dev-pdf --prefix instrumentoslegales/
"""
import mimetypes
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import storage

BATCH_SIZE = 100
BATCH_RETRIES = 3


class Command(BaseCommand):
    help = "Parchea el Content-Type de objetos GCS que quedaron sin setear (application/octet-stream o vacío)."

    def add_arguments(self, parser):
        parser.add_argument("--bucket", default=None, help="Bucket a corregir (default: settings.GS_BUCKET_NAME).")
        parser.add_argument("--prefix", default="", help="Solo objetos bajo este prefijo (default: todo el bucket).")
        parser.add_argument(
            "--dry-run", action="store_true",
            help="No parchea nada, solo informa cuántos objetos corregiría y con qué Content-Type.",
        )

    def handle(self, *args, **options):
        if not settings.GS_CREDENTIALS:
            raise CommandError(
                "No hay credenciales de GCS cargadas (GS_CREDENTIALS es None). "
                "Falta polizador-production.json en BASE_DIR."
            )

        bucket_name = options["bucket"] or settings.GS_BUCKET_NAME
        prefix = options["prefix"]
        dry_run = options["dry_run"]

        client = storage.Client(credentials=settings.GS_CREDENTIALS, project=settings.GS_CREDENTIALS.project_id)
        bucket = client.bucket(bucket_name)

        self.stdout.write(f"Listando objetos en gs://{bucket_name}/{prefix}...")

        corregidos = 0
        sin_tipo_detectable = 0
        revisados = 0
        lote = []

        def _flush(lote):
            if not lote:
                return
            if dry_run:
                return
            # El endpoint de batch de GCS a veces devuelve 503 transitorio (server(s) are not
            # responding) sin que haya nada mal con los objetos en sí. Reintenta el batch
            # completo un par de veces y, si sigue fallando, cae a parchear uno por uno (más
            # lento pero un objeto puntualmente problemático no tira abajo la corrida entera).
            for intento in range(BATCH_RETRIES):
                try:
                    with client.batch():
                        for blob in lote:
                            blob.patch()
                    return
                except GoogleAPICallError as e:
                    self.stdout.write(
                        f"{self.style.WARNING('  Batch falló')} (intento {intento + 1}/{BATCH_RETRIES}): {e}"
                    )
                    time.sleep(2 ** intento)

            self.stdout.write(self.style.WARNING("  Reintentando ese lote uno por uno..."))
            for blob in lote:
                try:
                    blob.patch()
                except GoogleAPICallError as e:
                    self.stdout.write(f"{self.style.ERROR('  Falló definitivamente:')} {blob.name}: {e}")

        for blob in client.list_blobs(bucket, prefix=prefix):
            revisados += 1
            if blob.content_type and blob.content_type != "application/octet-stream":
                continue

            guessed, _ = mimetypes.guess_type(blob.name)
            if not guessed:
                sin_tipo_detectable += 1
                self.stdout.write(f"{self.style.WARNING('  Sin tipo detectable:')} {blob.name}")
                continue

            corregidos += 1
            if not dry_run:
                blob.content_type = guessed
                lote.append(blob)
                if len(lote) >= BATCH_SIZE:
                    _flush(lote)
                    lote = []

            if revisados % 2000 == 0:
                self.stdout.write(f"  ... {revisados} revisados, {corregidos} corregidos")

        _flush(lote)

        accion = "Se corregirían" if dry_run else "Corregidos"
        self.stdout.write(self.style.SUCCESS(
            f"{accion} {corregidos} objeto(s) de {revisados} revisados "
            f"({sin_tipo_detectable} sin tipo detectable por nombre, dejados como estaban)."
        ))
