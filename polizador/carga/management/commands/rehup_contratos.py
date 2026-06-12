import os

from django.core.management.base import BaseCommand
from carga.models import ContratosDigitales


class Command(BaseCommand):
    """
    Management command: escanea archivos en la carpeta
    polizador/media/contratos_obra/ (recursivamente), extrae el UUID del nombre
    de cada archivo, busca el Contrato correspondiente en la base de datos
    y sube el archivo al campo contratodigital_archivo.

    Uso: python manage.py rehup_contratos
    """

    CONTRATOS_DIR = os.path.join(
        os.path.dirname(__file__),  # .../carga/management/commands/
        "../../../media/contratos_obra",
    )

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Escaneando: {os.path.abspath(self.CONTRATOS_DIR)}")

        if not os.path.isdir(self.CONTRATOS_DIR):
            self.stderr.write(
                self.style.ERROR(
                    f"La carpeta no existe: {self.CONTRATOS_DIR}"
                )
            )
            return

        archivos = []
        for root, _dirs, files in os.walk(self.CONTRATOS_DIR):
            for fname in files:
                archivos.append(os.path.join(root, fname))

        self.stdout.write(f"Se encontraron {len(archivos)} archivo(s)")

        subidos = 0
        errores = 0

        for filepath in sorted(archivos):
            filename = os.path.basename(filepath)
            # El nombre del archivo es: {uuid}.pdf
            uuid_str = filename

            # Buscar contrato por contratodigital_uuid
            try:
                contrato = ContratosDigitales.objects.get(contratodigital_uuid=uuid_str)
            except ContratosDigitales.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"No se encontro Contrato con uuid: {uuid_str} -> {filename}"
                    )
                )
                continue
            except ContratosDigitales.MultipleObjectsReturned:
                self.stderr.write(
                    self.style.ERROR(
                        f"Multiple Contratos para uuid: {uuid_str} -> {filename}"
                    )
                )
                errores += 1
                continue

            # Subir archivo al campo contratodigital_archivo
            try:
                with open(filepath, "rb") as local_file:
                    contrato.contratodigital_archivo.save(
                        f"{uuid_str}.pdf",
                        local_file,
                        save=True,
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Subido -> {uuid_str}.pdf"
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
