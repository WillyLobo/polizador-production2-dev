"""
Arma los paquetes ZIP de las resoluciones de un mes directamente en GCS, vía
gcs_zip.componer_zip() (compose de objetos, sin bajar y volver a subir el
contenido de cada PDF por el servidor de Django).

Pensado para correr por cron el día 1 de cada mes, empaquetando el mes que
acaba de terminar, y dejar los .zip listos para descargar desde el bucket:

    0 6 1 * * cd /ruta/al/proyecto && python manage.py empaquetar_resoluciones_mensual

También se puede pedir un mes/año puntual (backfill de meses viejos, pruebas):

    python manage.py empaquetar_resoluciones_mensual --ano 2026 --mes 3
"""
import zlib
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage

from secretariador.gcs_zip import EntradaZip, componer_zip, limpiar_temporales
from secretariador.models import InstrumentosLegalesResoluciones

DESTINO_PREFIJO = "instrumentoslegales/resoluciones/paquetes"


def _mes_anterior(hoy):
    if hoy.month == 1:
        return hoy.year - 1, 12
    return hoy.year, hoy.month - 1


def _armar_paquetes(entradas, tamano_maximo):
    """Agrupa las entradas en paquetes que no superen tamano_maximo bytes
    (greedy, mismo criterio que la vista de empaquetado manual). Una entrada
    más grande que tamano_maximo queda sola en su propio paquete."""
    paquetes = []
    paquete_actual = []
    tamano_actual = 0
    for entrada in entradas:
        if paquete_actual and tamano_actual + entrada.tamano > tamano_maximo:
            paquetes.append(paquete_actual)
            paquete_actual = []
            tamano_actual = 0
        paquete_actual.append(entrada)
        tamano_actual += entrada.tamano
    if paquete_actual:
        paquetes.append(paquete_actual)
    return paquetes


class Command(BaseCommand):
    help = "Arma los paquetes ZIP de resoluciones de un mes vía GCS compose, sin bajar los PDFs al servidor."

    def add_arguments(self, parser):
        parser.add_argument("--ano", type=int, help="Año a empaquetar (default: el mes anterior al actual).")
        parser.add_argument("--mes", type=int, help="Mes a empaquetar, 1-12 (default: el mes anterior al actual).")
        parser.add_argument(
            "--tamano-maximo-mb", type=int, default=13, dest="tamano_maximo_mb",
            help="Tamaño máximo por paquete, en MB (default: 13).",
        )

    def handle(self, *args, **options):
        ano = options["ano"]
        mes = options["mes"]
        if (ano is None) != (mes is None):
            raise CommandError("--ano y --mes se tienen que pasar juntos.")
        if ano is None:
            ano, mes = _mes_anterior(date.today())

        tamano_maximo = options["tamano_maximo_mb"] * 1024 * 1024

        resoluciones = InstrumentosLegalesResoluciones.objects.filter(
            instrumentolegalresoluciones_fecha_aprobacion__year=ano,
            instrumentolegalresoluciones_fecha_aprobacion__month=mes,
        ).exclude(instrumentolegalresoluciones="").order_by("instrumentolegalresoluciones_numero")

        if not resoluciones.exists():
            self.stdout.write(f"No hay resoluciones con archivo cargado para {mes:02d}/{ano}.")
            return

        bucket = default_storage.client.bucket(default_storage.bucket_name)

        entradas = []
        for resolucion in resoluciones:
            nombre = resolucion.instrumentolegalresoluciones.name
            blob = bucket.blob(nombre)
            blob.reload()

            crc = resolucion.instrumentolegalresoluciones_crc32
            if crc is None:
                # No debería pasar si backfill_resoluciones_crc32 ya corrió una vez
                # y el signal está cacheando las subidas nuevas, pero si igual falta
                # lo calculamos acá para que este comando nunca dependa de un paso
                # manual previo.
                self.stdout.write(f"  Calculando CRC-32 (no estaba cacheado) de {nombre}...")
                crc = 0
                with resolucion.instrumentolegalresoluciones.open("rb") as archivo:
                    for chunk in archivo.chunks():
                        crc = zlib.crc32(chunk, crc)
                resolucion.instrumentolegalresoluciones_crc32 = crc
                resolucion.save(update_fields=["instrumentolegalresoluciones_crc32"])

            entradas.append(EntradaZip(
                nombre_archivo=nombre.rsplit("/", 1)[-1],
                tamano=blob.size,
                crc32=crc,
                blob_origen=blob,
                date_time=resolucion.instrumentolegalresoluciones_fecha_aprobacion.timetuple()[:6],
            ))

        paquetes = _armar_paquetes(entradas, tamano_maximo)

        prefijo_destino = f"{DESTINO_PREFIJO}/{ano}-{mes:02d}"
        prefijo_scratch = f"{prefijo_destino}/_scratch"

        # Si esta corrida arma menos paquetes que una corrida anterior para el
        # mismo mes (p.ej. porque ahora entran en menos partes), esto evita
        # dejar un paquete-03.zip huérfano de la corrida vieja.
        for blob_viejo in bucket.list_blobs(prefix=f"{prefijo_destino}/paquete-"):
            blob_viejo.delete()

        rutas_generadas = []
        for indice, paquete in enumerate(paquetes, start=1):
            destino_nombre = f"{prefijo_destino}/paquete-{indice:02d}.zip"
            destino_blob, temporales = componer_zip(bucket, paquete, destino_nombre, prefijo_scratch)
            limpiar_temporales(temporales)
            rutas_generadas.append(destino_blob.name)
            self.stdout.write(f"  Armado {destino_blob.name} ({len(paquete)} resoluciones)")

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {len(rutas_generadas)} paquete(s) para {mes:02d}/{ano} en "
            f"gs://{bucket.name}/{prefijo_destino}/"
        ))
