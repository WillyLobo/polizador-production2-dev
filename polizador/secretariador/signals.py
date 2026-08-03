import zlib

from django.core.files.uploadedfile import UploadedFile
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import InstrumentosLegalesResoluciones


@receiver(pre_save, sender=InstrumentosLegalesResoluciones)
def calcular_crc32_resolucion(sender, instance, **kwargs):
    """Cachea el CRC-32 del archivo apenas se sube, para poder armar los
    paquetes mensuales vía GCS compose (ver gcs_zip.py) sin tener que
    descargar cada PDF de nuevo solo para calcular su checksum.

    Solo recalcula cuando el archivo adjunto es una subida nueva (un
    UploadedFile en memoria/disco temporal); si el field ya apunta a un
    archivo existente en el storage no hay nada que recalcular.
    """
    archivo = instance.instrumentolegalresoluciones
    if not archivo or not isinstance(archivo.file, UploadedFile):
        return

    archivo.file.seek(0)
    instance.instrumentolegalresoluciones_crc32 = zlib.crc32(archivo.file.read())
    archivo.file.seek(0)
