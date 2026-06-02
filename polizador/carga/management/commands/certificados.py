import os

from django.core.management.base import BaseCommand, CommandError
from carga.models import *
from secretariador.models import *
from django.db.models import Sum, Q
from datetime import datetime
import requests
import csv


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
        csv_path = "output.csv"

        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar='"')

            # Encabezado del CSV
            writer.writerow([
                "id",
                "expediente",
                "certificado_digital_name",
                "certificado_digital_url",
                "archivo_local"
            ])

            for certificado in Certificado.objects.all():
                # Solo procesa certificados que tengan un archivo digital asociado
                if certificado.certificado_digital:
                    # Construye la ruta local a partir del path del FileField.
                    # Se asume que el nombre del archivo tiene formato "subida/..."
                    directorio = (
                        f"{certificado.certificado_digital.name.split('/')[0]}/"
                        f"{certificado.certificado_digital.name.split('/')[1]}/"
                    )

                    # Crea los directorios si no existen
                    if not os.path.exists(directorio):
                        os.makedirs(directorio)

                    # Descarga el archivo remoto
                    response = requests.get(certificado.certificado_digital.url)

                    # Si la descarga fue exitosa, guarda el archivo localmente
                    if response.status_code == 200:
                        nombre_local = (
                            f"{directorio}{certificado.id}-"
                            f"{certificado.certificado_expediente}.pdf"
                        )
                        with open(nombre_local, "wb") as f:
                            f.write(response.content)
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Error {response.status_code} al descargar "
                                f"certificado {certificado.id}"
                            )
                        )
                        continue

                    # Escribe la fila en el CSV con la metadata del certificado
                    writer.writerow([
                        certificado.id,
                        certificado.certificado_expediente,
                        certificado.certificado_digital.name,
                        certificado.certificado_digital.url,
                        nombre_local
                    ])

                    self.stdout.write(
                        f"Descargado certificado {certificado.id} "
                        f"{certificado.certificado_expediente}"
                    )
