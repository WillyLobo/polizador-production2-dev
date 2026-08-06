"""
Lógica compartida para armar los paquetes mensuales de resoluciones (ZIP y
PDF fusionado), usada por el management command empaquetar_resoluciones_mensual
y por la vista de listado/descarga (paqueteresolucionesviews.py).

Cada entrada se lee del disco local cuando está disponible: GCloudAndLocalStorage
(polizador/storages.py) guarda toda subida tanto en GCS como en MEDIA_ROOT, así
que en producción el contenido de las resoluciones ya está en disco y no hace
falta bajarlo de GCS para armar los paquetes. leer_contenido() solo baja de GCS
como fallback (resoluciones subidas antes de ese storage, entornos sin disco
persistente, etc).

Con el contenido ya en memoria, el ZIP se arma con el módulo estándar zipfile
y el PDF fusionado con pikepdf (basado en QPDF) — a diferencia del ZIP, un PDF
no se puede concatenar a nivel de bytes: hace falta reescribir su tabla de
referencias cruzadas y renumerar objetos, que es lo que hace pikepdf al
fusionar páginas.
"""
import io
import zipfile

import pikepdf
from dataclasses import dataclass

DESTINO_PREFIJO = "instrumentoslegales/resoluciones/paquetes"


@dataclass
class EntradaResolucion:
    nombre_archivo: str          # nombre dentro del paquete, p.ej. "1234-2026-P.pdf"
    tamano: int                  # bytes
    date_time: tuple             # para el encabezado del ZIP
    ruta_local: object = None    # Path si el archivo está en MEDIA_ROOT (caso común en producción)
    blob_origen: object = None   # google.cloud.storage.Blob; fallback si no está en disco local


def mes_anterior(hoy):
    if hoy.month == 1:
        return hoy.year - 1, 12
    return hoy.year, hoy.month - 1


def armar_paquetes(entradas, tamano_maximo):
    """Agrupa entradas (cualquier objeto con atributo .tamano en bytes) en
    paquetes que no superen tamano_maximo bytes (greedy, mismo criterio para
    ZIP y PDF). Una entrada más grande que tamano_maximo queda sola en su
    propio paquete."""
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


def leer_contenido(entrada):
    if entrada.ruta_local is not None:
        return entrada.ruta_local.read_bytes()
    return entrada.blob_origen.download_as_bytes()


def armar_zip(paquete):
    """Arma un .zip en memoria con las entradas del paquete, en orden."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as zf:
        for entrada in paquete:
            zinfo = zipfile.ZipInfo(filename=entrada.nombre_archivo, date_time=entrada.date_time)
            zinfo.compress_type = zipfile.ZIP_STORED
            zinfo.external_attr = 0o600 << 16
            zf.writestr(zinfo, leer_contenido(entrada))
    return buffer.getvalue()


def armar_pdf(paquete):
    """Fusiona las páginas de las entradas del paquete, en orden, en un único PDF."""
    fusionado = pikepdf.new()
    try:
        for entrada in paquete:
            with pikepdf.open(io.BytesIO(leer_contenido(entrada))) as origen:
                fusionado.pages.extend(origen.pages)
        buffer = io.BytesIO()
        fusionado.save(buffer)
    finally:
        fusionado.close()
    return buffer.getvalue()
