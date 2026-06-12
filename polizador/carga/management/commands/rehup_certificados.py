import os

from django.core.management.base import BaseCommand
from carga.models import Certificado


class Command(BaseCommand):
    """
    Management command: escanea archivos en la carpeta
    polizador/media/certificados/ (recursivamente), extrae el UUID del nombre
    de cada archivo, busca el Certificado correspondiente en la base de datos
    y sube el archivo al campo certificado_digital.

    Uso: python manage.py rehup_certificados
    """

    CERTIFICADOS_DIR = os.path.join(
        os.path.dirname(__file__),  # .../carga/management/commands/
        "../../../media/certificados",
    )

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Escaneando: {os.path.abspath(self.CERTIFICADOS_DIR)}")

        if not os.path.isdir(self.CERTIFICADOS_DIR):
            self.stderr.write(
                self.style.ERROR(
                    f"La carpeta no existe: {self.CERTIFICADOS_DIR}"
                )
            )
            return

        archivos = []
        for root, _dirs, files in os.walk(self.CERTIFICADOS_DIR):
            for fname in files:
                archivos.append(os.path.join(root, fname))

        self.stdout.write(f"Se encontraron {len(archivos)} archivo(s)")

        subidos = 0
        errores = 0

        for filepath in sorted(archivos):
            filename = os.path.basename(filepath)
            # El nombre del archivo es: {uuid}.pdf  o  {uuid}_{expediente}.pdf
            uuid_str = filename.rsplit("_", 1)[0]

            # Buscar certificado por certificado_uuid
            try:
                certificado = Certificado.objects.get(certificado_uuid=uuid_str)
            except Certificado.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"No se encontro Certificado con uuid: {uuid_str} -> {filename}"
                    )
                )
                continue
            except Certificado.MultipleObjectsReturned:
                self.stderr.write(
                    self.style.ERROR(
                        f"Multiple certificados para uuid: {uuid_str} -> {filename}"
                    )
                )
                errores += 1
                continue

            # Subir archivo al campo certificado_digital
            try:
                with open(filepath, "rb") as local_file:
                    certificado.certificado_digital.save(
                        f"{uuid_str}_{certificado.certificado_expediente}.pdf",
                        local_file,
                        save=True,
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Subido -> {uuid_str}_{certificado.certificado_expediente}.pdf"
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
