from collections import defaultdict
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from personalizador.licencias import (
    LICENCIA_ANUAL_ADELANTADA_NOMBRE, LICENCIA_ANUAL_INVIERNO_NOMBRE, LICENCIA_ANUAL_ORDINARIA_NOMBRE,
    get_or_create_periodo_agente, get_periodo, periodo_objetivo,
)
from personalizador.models import LicenciaPermiso, PeriodoLicencia, TipoLicenciaPermiso


class Command(BaseCommand):
    help = (
        "Backfillea licenciapermiso_periodo en LicenciaPermiso existentes de los 3 "
        "tipos año-vencido (Anual, Anual Proporcional, Anual de Invierno) que todavia "
        "no lo tengan, resolviendo el PeriodoLicencia via personalizador.licencias."
        "periodo_objetivo. Para categoria LOR_ANUAL, si el PeriodoLicencia no existe "
        "se autocrea con la formula legal (apertura 15/12, limite 31/03 del año "
        "siguiente); para LOR_INVIERNO (turnos por decreto, sin formula fija) NO se "
        "autocrea -- las licencias de años sin ese periodo se saltean y quedan "
        "reportadas, para cargarlo a mano en Licencias > Periodos y re-correr el "
        "comando (es idempotente: solo procesa licenciapermiso_periodo__isnull=True). "
        "No revalida el registro completo (no llama full_clean()): solo completa el "
        "FK, para no rechazar datos historicos contra reglas de negocio nuevas (ej. el "
        "bloqueo de adelanto por saldo de corte pendiente) que no regian cuando esos "
        "registros se cargaron."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="No guarda cambios en la base de datos, solo informa.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        verbosity = options.get("verbosity", 1)

        tipos = list(TipoLicenciaPermiso.objects.filter(
            tipolicenciapermiso_categoria="LOR",
            tipolicenciapermiso_nombre__in=[
                LICENCIA_ANUAL_ORDINARIA_NOMBRE, LICENCIA_ANUAL_ADELANTADA_NOMBRE, LICENCIA_ANUAL_INVIERNO_NOMBRE,
            ],
        ))

        stats = defaultdict(int)
        periodos_lor_invierno_faltantes = set()

        with transaction.atomic():
            queryset = LicenciaPermiso.objects.filter(
                licenciapermiso_tipo__in=tipos, licenciapermiso_periodo__isnull=True,
            ).select_related("licenciapermiso_agente", "licenciapermiso_tipo")

            for licencia in queryset:
                resultado = periodo_objetivo(
                    licencia.licenciapermiso_tipo.tipolicenciapermiso_nombre,
                    licencia.licenciapermiso_fecha_desde.year,
                )
                if resultado is None:
                    continue
                categoria, anio = resultado

                periodo = get_periodo(categoria, anio)
                if periodo is None:
                    if categoria == "LOR_ANUAL":
                        periodo = PeriodoLicencia(
                            periodolicencia_categoria="LOR_ANUAL", periodolicencia_anio=anio,
                            periodolicencia_apertura=date(anio, 12, 15),
                            periodolicencia_fecha_limite_solicitud=date(anio + 1, 3, 31),
                        )
                        periodo.full_clean()
                        periodo.save()
                        stats["periodos_lor_anual_creados"] += 1
                    else:
                        periodos_lor_invierno_faltantes.add(anio)
                        stats["salteados_falta_periodo_invierno"] += 1
                        continue

                if periodo.periodolicencia_categoria == "LOR_ANUAL":
                    get_or_create_periodo_agente(licencia.licenciapermiso_agente, periodo)

                licencia.licenciapermiso_periodo = periodo
                licencia.save(update_fields=["licenciapermiso_periodo"])
                stats["actualizados"] += 1

            if dry_run:
                transaction.set_rollback(True)

        if verbosity >= 1:
            self.stdout.write("")
            if dry_run:
                self.stdout.write(self.style.NOTICE("Modo dry-run: no se guardo ningun cambio en la base de datos."))
            self.stdout.write(self.style.MIGRATE_HEADING("Resumen:"))
            self.stdout.write(self.style.SUCCESS(f"    LicenciaPermiso actualizadas: {stats['actualizados']}"))
            self.stdout.write(self.style.SUCCESS(f"    PeriodoLicencia LOR_ANUAL autocreados: {stats['periodos_lor_anual_creados']}"))
            if periodos_lor_invierno_faltantes:
                anios = ", ".join(str(a) for a in sorted(periodos_lor_invierno_faltantes))
                self.stdout.write(self.style.WARNING(
                    f"    Salteadas ({stats['salteados_falta_periodo_invierno']}) por falta de PeriodoLicencia "
                    f"'Anual de Invierno' de los años: {anios}. Cargarlos a mano en Licencias > Periodos "
                    "(4 campos de turno) y re-correr el comando."
                ))
