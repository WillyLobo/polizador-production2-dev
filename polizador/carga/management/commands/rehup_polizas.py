import os

from django.core.management.base import BaseCommand
from carga.models import Poliza


class Command(BaseCommand):
    """
    Management command: escanea archivos en la carpeta
    polizador/media/obra/ (recursivamente), extrae el UUID del nombre
    de cada archivo, busca la Poliza correspondiente en la base de datos
    y sube el archivo al campo poliza_digital.

    Uso: python manage.py rehup_polizas
    """

    POLIZAS_DIR = os.path.join(
        os.path.dirname(__file__),  # .../carga/management/commands/
        "../../../media/polizas",
    )

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Escaneando: {os.path.abspath(self.POLIZAS_DIR)}")

        if not os.path.isdir(self.POLIZAS_DIR):
            self.stderr.write(
                self.style.ERROR(
                    f"La carpeta no existe: {self.POLIZAS_DIR}"
                )
            )
            return

        archivos = []
        for root, _dirs, files in os.walk(self.POLIZAS_DIR):
            for fname in files:
                archivos.append(os.path.join(root, fname))

        self.stdout.write(f"Se encontraron {len(archivos)} archivo(s)")

        subidos = 0
        errores = 0

        for filepath in sorted(archivos):
            filename = os.path.basename(filepath)
            # El nombre del archivo es: {uuid}.pdf  o  {uuid}_{expediente}.pdf
            uuid_str = filename.rsplit("_", 1)[0]

            # Buscar poliza por poliza_uuid
            try:
                poliza = Poliza.objects.get(poliza_uuid=uuid_str)
            except Poliza.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"No se encontro Poliza con uuid: {uuid_str} -> {filename}"
                    )
                )
                continue
            except Poliza.MultipleObjectsReturned:
                self.stderr.write(
                    self.style.ERROR(
                        f"Multiple Polizas para uuid: {uuid_str} -> {filename}"
                    )
                )
                errores += 1
                continue

            # Subir archivo al campo poliza_digital
            try:
                with open(filepath, "rb") as local_file:
                    poliza.poliza_digital.save(
                        f"{uuid_str}_{poliza.poliza_expediente}.pdf",
                        local_file,
                        save=True,
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Subido -> {uuid_str}_{poliza.poliza_expediente}.pdf"
                    )
                )
                subidos += 1
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f"Error al subir '{filename}': {e}"
                    )
                )
                errores += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nResumen: {subidos} subido(s), {errores} error(es)"
            )
        )
