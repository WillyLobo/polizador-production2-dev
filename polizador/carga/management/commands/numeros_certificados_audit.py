from django.core.management.base import BaseCommand
from django.db import transaction

from carga.models import Certificado, Obra

PROGRAMAS_A_ACHURAR = [6, 10]


class Command(BaseCommand):
    """
    Management command: Arreglo de los numeros de certificados(ej. anticipo 22
    obra 22 dev.ant 22).
    Tambien arregla las obras que se cargaron erroneamente con FO.PRO.VI. como convenio.
    Uso: python manage.py numeros_certificados_audit
    """

    help = "Corrige numeración de certificados de anticipo/Res.62 y obras con convenio FO.PRO.VI. mal cargado."

    def add_arguments(self, parser):
        parser.add_argument(
            "--check",
            action="store_true",
            help="No modifica nada: solo cuenta cuántos registros necesita cada corrección.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Muestra el detalle de los cambios que se harían (registro por registro), sin guardarlos.",
        )

    def handle(self, *args, **options):
        if options["check"]:
            self._check()
            return

        dry_run = options["dry_run"]
        total = 0
        with transaction.atomic():
            total += self._fix_anticipos_res62(dry_run)
            total += self._fix_anticipos_villas_asentamientos(dry_run)
            total += self._fix_obras_foprovi(dry_run)

            if dry_run:
                self.stdout.write(self.style.WARNING("Dry-run: no se guardó ningún cambio."))
                transaction.set_rollback(True)

        self.stdout.write(self.style.SUCCESS(f"Total: {total} registro(s) corregidos."))

    # ------------------------------------------------------------------
    # Querysets compartidos entre --check y las correcciones reales, para que el
    # conteo rápido de --check no pueda desincronizarse de lo que --dry-run/apply
    # efectivamente tocan.
    # ------------------------------------------------------------------

    def _anticipos_res62_qs(self):
        return (
            Certificado.objects.filter(certificado_rubro_anticipo__gte=1)
            .exclude(
                certificado_mes_pct=0,
                certificado_devolucion_monto__gt=0,
                certificado_devolucion_monto_uvi__gt=0,
            )
            .filter(certificado_rubro_db=11)
        )

    def _anticipos_programa_qs(self, programa):
        return (
            Certificado.objects.filter(certificado_rubro_anticipo__gte=1)
            .exclude(certificado_devolucion_monto__gt=0, certificado_devolucion_monto_uvi__gt=0)
            .filter(certificado_obra__obra_programa=programa)
        )

    def _obras_foprovi_qs(self):
        return Obra.objects.filter(obra_convenio="FO.PRO.VI.")

    # ------------------------------------------------------------------
    # --check: resumen rápido, de solo lectura
    # ------------------------------------------------------------------

    def _check(self):
        total = 0

        count = self._anticipos_res62_qs().count()
        self.stdout.write(f"[Res.62] Certificados a corregir (anticipo/dev.anticipo -> 0): {count}")
        total += count

        for programa in PROGRAMAS_A_ACHURAR:
            count = self._anticipos_programa_qs(programa).count()
            self.stdout.write(
                f"[Programa {programa}] Certificados de anticipo a reclasificar como obra: {count}"
            )
            total += count

        count = self._obras_foprovi_qs().count()
        self.stdout.write(f"[FO.PRO.VI.] Obras con convenio mal cargado: {count}")
        total += count

        self.stdout.write(self.style.SUCCESS(f"Total: {total} registro(s) a corregir."))

    # ------------------------------------------------------------------
    # Correcciones (respetan dry_run: calculan y muestran, pero no guardan)
    # ------------------------------------------------------------------

    def _fix_anticipos_res62(self, dry_run):
        anticipos_res62 = list(self._anticipos_res62_qs())
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
            if not dry_run:
                anticipo.save(update_fields=["certificado_rubro_anticipo", "certificado_rubro_devanticipo"])
        self.stdout.write(self.style.SUCCESS(f"[Res.62] {len(anticipos_res62)} certificados corregidos."))
        return len(anticipos_res62)

    def _fix_anticipos_villas_asentamientos(self, dry_run):
        total = 0
        for programa in PROGRAMAS_A_ACHURAR:
            anticipos = list(self._anticipos_programa_qs(programa))
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
                if not dry_run:
                    anticipo.save(
                        update_fields=[
                            "certificado_rubro_obra",
                            "certificado_rubro_anticipo",
                            "certificado_rubro_devanticipo",
                        ]
                    )
            total += len(anticipos)
        self.stdout.write(self.style.SUCCESS(f"[Villas/Asentamientos] {total} certificados reclasificados."))
        return total

    def _fix_obras_foprovi(self, dry_run):
        obras = list(self._obras_foprovi_qs())
        self.stdout.write(f"[FO.PRO.VI.] Obras con convenio mal cargado: {len(obras)}")
        for obra in obras:
            self.stdout.write(f"  Obra #{obra.pk} ({obra.obra_nombre}): convenio 'FO.PRO.VI.' -> None")
            obra.obra_convenio = None
            if not dry_run:
                obra.save(update_fields=["obra_convenio"])
        self.stdout.write(self.style.SUCCESS(f"[FO.PRO.VI.] {len(obras)} obras corregidas."))
        return len(obras)
