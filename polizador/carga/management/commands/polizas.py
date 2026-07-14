import os

from django.core.management.base import BaseCommand, CommandError
from carga.models import *
from secretariador.models import *
from django.db.models import Sum, Q
from datetime import datetime
import requests
import csv
from django.conf import settings

"""
ContratosDigitales, contratodigital_archivo
Poliza, poliza_digital
Certificado, certificado_digital
"""

class Command(BaseCommand):
    """
    Management command: descarga los certificados digitales almacenados como
    archivos remotos (FileField) y los guarda localmente en el sistema de
    archivos. Además genera un archivo output.csv con metadata de cada
    certificado descargado.

    Uso: python manage.py certificados
    """

    def handle(self, *args, **kwargs):
        # Ruta del archivo CSV de salida
            for poliza in Poliza.objects.all():
                # Solo procesa certificados que tengan un archivo digital asociado
                if poliza.poliza_digital:
                    # Construye la ruta local a partir del path del FileField.
                    # Se asume que el nombre del archivo tiene formato "subida/..."
                    
                    # VARIABLES DIRECTORIO
                    directorio_full_path = poliza.poliza_digital.name.split('/')
                    directorio_base = directorio_full_path[0]
                    directorio_fecha = directorio_full_path[1]
                    directorio_fecha_mes = directorio_fecha.split('-')[0]
                    directorio_fecha_anio = directorio_fecha.split('-')[1]
                    
                    directorio = (
                        f"polizador/media/"
                        f"{directorio_base}/"
                        f"{directorio_fecha_anio}/"
                        f"{directorio_fecha_mes}/"
                    )
                    
                    # Crea los directorios si no existen
                    if not os.path.exists(directorio):
                        os.makedirs(directorio)

                    # Descarga el archivo remoto
                    response = requests.get(poliza.poliza_digital.url)

                    # Si la descarga fue exitosa, guarda el archivo localmente
                    if response.status_code == 200:
                        nombre_local = (
                            f"{directorio}{poliza.poliza_uuid}_{poliza.poliza_expediente}.pdf"
                        )
                        with open(nombre_local, "wb") as f:
                            f.write(response.content)
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Error {response.status_code} al descargar "
                                f"Poliza {poliza.poliza_uuid}"
                            )
                        )
                        continue

                    self.stdout.write(
                        f"Descargada Poliza {directorio}{poliza.poliza_uuid}_{poliza.poliza_expediente}.pdf"
                    )
