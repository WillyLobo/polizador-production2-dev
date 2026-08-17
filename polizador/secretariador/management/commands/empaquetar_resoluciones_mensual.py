"""
Arma los paquetes mensuales de resoluciones (ZIP y/o PDF fusionado) y los deja
en GCS, listos para descargar desde PaginaListaPaquetesResoluciones.

Lee el contenido de cada resolución del disco local cuando está disponible
(ver secretariador/paquetes_resoluciones.py) y solo baja de GCS lo que falte
localmente.

Pensado para correr por cron el día 1 de cada mes, empaquetando el mes que
acaba de terminar, y dejar los paquetes listos para descargar desde el bucket:

    0 6 1 * * cd /ruta/al/proyecto && python manage.py empaquetar_resoluciones_mensual

También se puede pedir un mes/año puntual (backfill de meses viejos, pruebas)
y elegir qué formato(s) generar:

    python manage.py empaquetar_resoluciones_mensual --ano 2026 --mes 3
    python manage.py empaquetar_resoluciones_mensual --formato pdf
"""
import base64
import hashlib
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from secretariador.models import InstrumentosLegalesResoluciones
from secretariador.paquetes_resoluciones import (
    DESTINO_PREFIJO,
    EntradaResolucion,
    armar_paquetes,
    armar_pdf,
    armar_zip,
    mes_anterior,
)

FORMATOS_A_EXTENSIONES = {
    "zip": (".zip",),
    "pdf": (".pdf",),
    "ambos": (".zip", ".pdf"),
}


def _mismo_contenido(blob, contenido):
    """Compara un blob ya existente en GCS contra contenido recién armado en
    memoria, sin bajarlo: usa el tamaño y el md5_hash que list_blobs() ya trae
    en la metadata del objeto."""
    if blob.size != len(contenido):
        return False
    md5_nuevo = base64.b64encode(hashlib.md5(contenido).digest()).decode()
    return blob.md5_hash == md5_nuevo


class Command(BaseCommand):
    help = "Arma los paquetes (ZIP y/o PDF fusionado) de resoluciones de un mes."

    def add_arguments(self, parser):
        parser.add_argument("--ano", type=int, help="Año a empaquetar (default: el mes anterior al actual).")
        parser.add_argument("--mes", type=int, help="Mes a empaquetar, 1-12 (default: el mes anterior al actual).")
        parser.add_argument(
            "--tamano-maximo-mb", type=int, default=13, dest="tamano_maximo_mb",
            help="Tamaño máximo por parte, en MB (default: 13).",
        )
        parser.add_argument(
            "--formato", choices=sorted(FORMATOS_A_EXTENSIONES), default="ambos",
            help="Qué formato(s) generar (default: ambos).",
        )

    def handle(self, *args, **options):
        ano = options["ano"]
        mes = options["mes"]
        if (ano is None) != (mes is None):
            raise CommandError("--ano y --mes se tienen que pasar juntos.")
        if ano is None:
            ano, mes = mes_anterior(date.today())

        tamano_maximo = options["tamano_maximo_mb"] * 1024 * 1024
        extensiones = FORMATOS_A_EXTENSIONES[options["formato"]]

        resoluciones = InstrumentosLegalesResoluciones.objects.filter(
            instrumentolegalresoluciones_fecha_aprobacion__year=ano,
            instrumentolegalresoluciones_fecha_aprobacion__month=mes,
        ).exclude(instrumentolegalresoluciones="").order_by("instrumentolegalresoluciones_numero")

        if not resoluciones.exists():
            self.stdout.write(f"No hay resoluciones con archivo cargado para {mes:02d}/{ano}.")
            return

        bucket = default_storage.client.bucket(default_storage.bucket_name)
        media_root = Path(settings.MEDIA_ROOT)

        entradas = []
        for resolucion in resoluciones:
            nombre = resolucion.instrumentolegalresoluciones.name
            date_time = resolucion.instrumentolegalresoluciones_fecha_aprobacion.timetuple()[:6]
            ruta_local = media_root / nombre

            if ruta_local.exists():
                entradas.append(EntradaResolucion(
                    nombre_archivo=nombre.rsplit("/", 1)[-1],
                    tamano=ruta_local.stat().st_size,
                    date_time=date_time,
                    ruta_local=ruta_local,
                ))
            else:
                blob = bucket.blob(nombre)
                blob.reload()
                entradas.append(EntradaResolucion(
                    nombre_archivo=nombre.rsplit("/", 1)[-1],
                    tamano=blob.size,
                    date_time=date_time,
                    blob_origen=blob,
                ))

        paquetes = armar_paquetes(entradas, tamano_maximo)

        prefijo_destino = f"{DESTINO_PREFIJO}/{ano}-{mes:02d}"

        # Arma el contenido en memoria antes de tocar el bucket, para poder
        # compararlo con lo que ya está subido y evitar una subida (y el
        # borrado/reemplazo del blob viejo) cuando el contenido no cambió.
        contenidos = {}
        for indice, paquete in enumerate(paquetes, start=1):
            if ".zip" in extensiones:
                nombre = f"{prefijo_destino}/paquete-{indice:02d}.zip"
                contenidos[nombre] = (armar_zip(paquete), "application/zip", len(paquete))
            if ".pdf" in extensiones:
                nombre = f"{prefijo_destino}/paquete-{indice:02d}.pdf"
                contenidos[nombre] = (armar_pdf(paquete), "application/pdf", len(paquete))

        blobs_viejos = {
            blob.name: blob
            for blob in bucket.list_blobs(prefix=f"{prefijo_destino}/paquete-")
            if blob.name.endswith(extensiones)
        }

        for nombre, (contenido, content_type, cantidad) in contenidos.items():
            blob_viejo = blobs_viejos.pop(nombre, None)
            if blob_viejo is not None and _mismo_contenido(blob_viejo, contenido):
                self.stdout.write(f"  Sin cambios {nombre} ({cantidad} resoluciones)")
                continue
            destino = bucket.blob(nombre)
            destino.upload_from_string(contenido, content_type=content_type)
            self.stdout.write(f"  Armado {nombre} ({cantidad} resoluciones)")

        # Lo que queda en blobs_viejos son paquetes huérfanos de una corrida
        # anterior con más partes que la actual (p.ej. paquete-03.* si ahora
        # alcanza con 2 paquetes) — se borran.
        for blob_viejo in blobs_viejos.values():
            blob_viejo.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {len(paquetes)} paquete(s) para {mes:02d}/{ano} en "
            f"gs://{bucket.name}/{prefijo_destino}/"
        ))
