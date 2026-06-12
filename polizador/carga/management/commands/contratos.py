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
"""

class Command(BaseCommand):
    """
    Management command: descarga los contratos digitales almacenados como
    archivos remotos (FileField) y los guarda localmente en el sistema de
    archivos.

    Uso: python manage.py contratos
    """

    def handle(self, *args, **kwargs):
        # Ruta del archivo CSV de salida
            for contrato in ContratosDigitales.objects.all():
                # Solo procesa ContratosDigitales que tengan un archivo digital asociado
                if contrato.contratodigital_archivo:
                    # Construye la ruta local a partir del path del FileField.
                    # Se asume que el nombre del archivo tiene formato "subida/..."
                    
                    # VARIABLES DIRECTORIO
                    directorio_full_path = contrato.contratodigital_archivo.name.split('/')
                    directorio_base = directorio_full_path[0]+"_obra"
                    
                    directorio = (
                        f"polizador/media/"
                        f"{directorio_base}/"
                    )
                    
                    # Crea los directorios si no existen
                    if not os.path.exists(directorio):
                        os.makedirs(directorio)

                    # Descarga el archivo remoto
                    response = requests.get(contrato.contratodigital_archivo.url)

                    # Si la descarga fue exitosa, guarda el archivo localmente
                    if response.status_code == 200:
                        nombre_local = (
                            f"{directorio}{contrato.contratodigital_uuid}.pdf"
                        )
                        with open(nombre_local, "wb") as f:
                            f.write(response.content)
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Error {response.status_code} al descargar "
                                f"Contrato {contrato.contratodigital_uuid}"
                            )
                        )
                        continue

                    self.stdout.write(
                        f"Descargado Contrato {directorio}{contrato.contratodigital_uuid}.pdf"
                    )
