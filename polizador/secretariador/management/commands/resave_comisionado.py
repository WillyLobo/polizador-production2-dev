import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from secretariador.models import (
    CAMPOS_DERIVADOS,
    COMISIONADO_PREFETCH_RELATED,
    COMISIONADO_SELECT_RELATED,
    ComisionadoSolicitud,
    _con_precision_guardada,
)

logger = logging.getLogger(__name__)

# Queda en history_change_reason de cada registro histórico que genera el comando.
CHANGE_REASON = "resave_comisionado: recálculo de campos derivados"


def _formatear(valor):
    if isinstance(valor, timedelta):
        return f"{valor.days} día(s)"
    return str(valor)


class Command(BaseCommand):
    """
    Management command: recalcula los campos derivados (dias, viatico
    computado, viatico total) de todos los ComisionadoSolicitud y los compara
    contra lo guardado, para detectar registros que quedaron desactualizados
    (p. ej. cargados por un camino que no pasó por save(), o cuya Solicitud se
    editó antes de que secretariador/signals.py los mantuviera sincronizados).

    El viático diario queda congelado (ver
    ComisionadoSolicitud.recalcular_campos_derivados): si la tarifa que dan hoy
    las reglas difiere de la guardada, solo se informa. Con --recalcular-diario
    se aplica también la tarifa actual.

    Solo se guardan los registros con diferencias, y únicamente esos campos:
    guardar uno sin cambios dejaría una entrada vacía en el historial y, vía
    secretariador/signals.py, invalidaría sin motivo el texto de la resolución
    editado a mano en su Solicitud/Incorporacion.

    Cada cambio aplicado queda en el historial del registro (simple_history,
    con history_change_reason=CHANGE_REASON) y en el log de la aplicación.

    Uso: python manage.py resave_comisionado [--check | --dry-run] [--recalcular-diario]
    """

    help = "Recalcula días y viáticos de los ComisionadoSolicitud y guarda solo los que difieren de lo guardado."

    def add_arguments(self, parser):
        modo = parser.add_mutually_exclusive_group()
        modo.add_argument(
            "--check",
            action="store_true",
            help="No modifica nada: solo cuenta cuántos registros tienen diferencias.",
        )
        modo.add_argument(
            "--dry-run",
            action="store_true",
            help="Muestra el detalle de las diferencias (registro por registro), sin guardarlas.",
        )
        parser.add_argument(
            "--recalcular-diario",
            action="store_true",
            help=(
                "Recalcula también el viático diario con las reglas actuales (ReglasViatico, "
                "escalafón, Directorio), en vez de mantener la tarifa congelada."
            ),
        )

    def handle(self, *args, **options):
        check = options["check"]
        dry_run = options["dry_run"]
        recalcular_diario = options["recalcular_diario"]
        aplicar = not check and not dry_run

        queryset = ComisionadoSolicitud.objects.select_related(
            *COMISIONADO_SELECT_RELATED
        ).prefetch_related(*COMISIONADO_PREFETCH_RELATED).order_by("pk")
        total = queryset.count()
        self.stdout.write(f"Se encontraron {total} ComisionadoSolicitud")

        con_diferencias = 0
        guardados = 0
        sin_cambios = 0
        tarifa_distinta = 0
        errores = 0

        with transaction.atomic():
            for comisionado in queryset.iterator(chunk_size=500):
                diario_guardado = comisionado.comisionadosolicitud_viatico_diario
                try:
                    diario_actual = _con_precision_guardada(
                        "comisionadosolicitud_viatico_diario", comisionado.valor_viatico_dia()
                    )
                    diferencias = comisionado.recalcular_campos_derivados(
                        recalcular_diario=recalcular_diario
                    )
                except Exception as e:
                    errores += 1
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error al recalcular ComisionadoSolicitud {comisionado.pk}: {e}"
                        )
                    )
                    continue

                if not recalcular_diario and diario_guardado is not None and diario_actual != diario_guardado:
                    tarifa_distinta += 1
                    if not check:
                        self.stdout.write(
                            f"  ComisionadoSolicitud #{comisionado.pk} ({comisionado}): "
                            f"tarifa congelada {diario_guardado}, con las reglas actuales sería "
                            f"{diario_actual} (no se modifica)"
                        )

                if not diferencias:
                    sin_cambios += 1
                    continue
                con_diferencias += 1
                if check:
                    continue

                detalle = self._describir(comisionado, diferencias)
                self.stdout.write(detalle)
                if not aplicar:
                    continue

                try:
                    with transaction.atomic():
                        comisionado._change_reason = CHANGE_REASON
                        comisionado.save(update_fields=CAMPOS_DERIVADOS, recalcular_derivados=False)
                except Exception as e:
                    errores += 1
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error al guardar ComisionadoSolicitud {comisionado.pk}: {e}"
                        )
                    )
                    continue
                guardados += 1
                logger.info("resave_comisionado guardó: %s", detalle.strip())

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry-run: no se guardó ningún cambio."))

        resumen = f"Resumen: {con_diferencias} con diferencias"
        if aplicar:
            resumen += f" ({guardados} guardado(s))"
        resumen += f", {sin_cambios} sin cambios, {errores} error(es)"
        if not recalcular_diario:
            resumen += f"; {tarifa_distinta} con tarifa congelada distinta de la actual (no se modifican)"
        self.stdout.write(self.style.SUCCESS(f"\n{resumen}"))
        if aplicar:
            logger.info("resave_comisionado: %s", resumen)

    def _describir(self, comisionado, diferencias):
        cambios = ", ".join(
            f"{ComisionadoSolicitud._meta.get_field(campo).verbose_name} "
            f"{_formatear(antes)} -> {_formatear(despues)}"
            for campo, antes, despues in diferencias
        )
        return f"  ComisionadoSolicitud #{comisionado.pk} ({comisionado}): {cambios}"
