from django.core.management.base import BaseCommand
from django.db import transaction

from carga.models import Certificado, Obra


class Command(BaseCommand):
    """
    Management command: Arreglo de los numeros de certificados(ej. anticipo 22
    obra 22 dev.ant 22).
    Tambien arregla las obras que se cargaron erroneamente con FO.PRO.VI. como convenio.
    Uso: python manage.py certificados
    """

    help = "Corrige numeración de certificados de anticipo/Res.62 y obras con convenio FO.PRO.VI. mal cargado."

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self._fix_anticipos_res62()
            self._fix_anticipos_villas_asentamientos()
            self._fix_obras_foprovi()

    def _fix_anticipos_res62(self):
        anticipos_res62 = list(
            Certificado.objects.filter(
                certificado_rubro_anticipo__gte=1,
            ).exclude(
                certificado_mes_pct=0,
                certificado_devolucion_monto__gt=0,
                certificado_devolucion_monto_uvi__gt=0,
            ).filter(
                certificado_rubro_db=11,
            )
        )
        self.stdout.write(
            f"[Res.62] Certificados a corregir (anticipo/dev.anticipo -> 0): {len(anticipos_res62)}"
        )
        for anticipo in anticipos_res62:
            self.stdout.write(
                f"  Certificado #{anticipo.pk} (Expte. {anticipo.certificado_expediente}): "
                f"anticipo {anticipo.certificado_rubro_anticipo} -> 0, "
                f"dev.anticipo {anticipo.certificado_rubro_devanticipo} -> 0"
            )
            anticipo.certificado_rubro_anticipo = 0
            anticipo.certificado_rubro_devanticipo = 0
            anticipo.save(update_fields=["certificado_rubro_anticipo", "certificado_rubro_devanticipo"])
        self.stdout.write(self.style.SUCCESS(f"[Res.62] {len(anticipos_res62)} certificados corregidos."))

    def _fix_anticipos_villas_asentamientos(self):
        PROGRAMAS_A_ACHURAR = [6, 10]
        total = 0
        for programa in PROGRAMAS_A_ACHURAR:
            anticipos = list(
                Certificado.objects.filter(
                    certificado_rubro_anticipo__gte=1,
                ).exclude(
                    certificado_devolucion_monto__gt=0,
                    certificado_devolucion_monto_uvi__gt=0,
                ).filter(
                    certificado_obra__obra_programa=programa,
                )
            )
            self.stdout.write(
                f"[Programa {programa}] Certificados de anticipo a reclasificar como obra: {len(anticipos)}"
            )
            for anticipo in anticipos:
                self.stdout.write(
                    f"  Certificado #{anticipo.pk} (Expte. {anticipo.certificado_expediente}): "
                    f"obra {anticipo.certificado_rubro_obra} -> {anticipo.certificado_rubro_anticipo}, "
                    f"anticipo {anticipo.certificado_rubro_anticipo} -> 0, "
                    f"dev.anticipo {anticipo.certificado_rubro_devanticipo} -> 0"
                )
                anticipo.certificado_rubro_obra = anticipo.certificado_rubro_anticipo
                anticipo.certificado_rubro_anticipo = 0
                anticipo.certificado_rubro_devanticipo = 0
                anticipo.save(update_fields=[
                    "certificado_rubro_obra",
                    "certificado_rubro_anticipo",
                    "certificado_rubro_devanticipo",
                ])
            total += len(anticipos)
        self.stdout.write(self.style.SUCCESS(f"[Villas/Asentamientos] {total} certificados reclasificados."))

    def _fix_obras_foprovi(self):
        obras = list(Obra.objects.filter(obra_convenio="FO.PRO.VI."))
        self.stdout.write(f"[FO.PRO.VI.] Obras con convenio mal cargado: {len(obras)}")
        for obra in obras:
            self.stdout.write(f"  Obra #{obra.pk} ({obra.obra_nombre}): convenio 'FO.PRO.VI.' -> None")
            obra.obra_convenio = None
            obra.save(update_fields=["obra_convenio"])
        self.stdout.write(self.style.SUCCESS(f"[FO.PRO.VI.] {len(obras)} obras corregidas."))
