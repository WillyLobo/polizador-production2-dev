import logging
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import models, transaction
from secretariador.models import ComisionadoSolicitud

logger = logging.getLogger(__name__)

# Relaciones que get_origin()/valor_viatico_dia()/__str__ recorren por registro:
# precargarlas evita N+1 queries sobre Solicitud/Incorporacion/Agente.
SELECT_RELATED = (
    "comisionadosolicitud_foreign__solicitud_decreto_viaticos",
    "comisionadosolicitud_foreign__solicitud_provincia",
    "comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_decreto_viaticos",
    "comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_provincia",
    "comisionadosolicitud_nombre",
    "comisionadosolicitud_externo",
)
PREFETCH_RELATED = ("comisionadosolicitud_nombre__directorio_set",)

# Los únicos campos que ComisionadoSolicitud.recalcular_campos_derivados() pisa.
CAMPOS_DERIVADOS = (
    "comisionadosolicitud_cantidad_de_dias",
    "comisionadosolicitud_viatico_diario",
    "comisionadosolicitud_viatico_computado",
    "comisionadosolicitud_viatico_total",
)

# Queda en history_change_reason de cada registro histórico que genera el comando.
CHANGE_REASON = "resave_comisionado: recálculo de campos derivados"


def _normalizar(campo, valor):
    """Lleva el valor recalculado a la misma precisión con la que queda guardado
    (decimal_places del DecimalField), para que una diferencia de redondeo que la
    base igual descartaría no se reporte como cambio."""
    field = ComisionadoSolicitud._meta.get_field(campo)
    if valor is not None and isinstance(field, models.DecimalField):
        return Decimal(str(valor)).quantize(Decimal(1).scaleb(-field.decimal_places))
    return valor


def _formatear(valor):
    if isinstance(valor, timedelta):
        return f"{valor.days} día(s)"
    return str(valor)


class Command(BaseCommand):
    """
    Management command: recalcula los campos derivados (dias, viatico diario,
    viatico computado, viatico total) de todos los ComisionadoSolicitud y los
    compara contra lo guardado, para detectar registros que quedaron
    desactualizados (p. ej. cargados por un camino que no pasó por save()).

    Solo se guardan los registros con diferencias, y únicamente esos campos:
    guardar uno sin cambios dejaría una entrada vacía en el historial y, vía
    secretariador/signals.py, invalidaría sin motivo el texto de la resolución
    editado a mano en su Solicitud/Incorporacion.

    Cada cambio aplicado queda en el historial del registro (simple_history,
    con history_change_reason=CHANGE_REASON) y en el log de la aplicación.

    Uso: python manage.py resave_comisionado [--check | --dry-run]
    """

    help = "Recalcula los viáticos de los ComisionadoSolicitud y guarda solo los que difieren de lo guardado."

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

    def handle(self, *args, **options):
        check = options["check"]
        dry_run = options["dry_run"]
        aplicar = not check and not dry_run

        queryset = ComisionadoSolicitud.objects.select_related(
            *SELECT_RELATED
        ).prefetch_related(*PREFETCH_RELATED).order_by("pk")
        total = queryset.count()
        self.stdout.write(f"Se encontraron {total} ComisionadoSolicitud")

        con_diferencias = 0
        guardados = 0
        sin_cambios = 0
        errores = 0

        with transaction.atomic():
            for comisionado in queryset.iterator(chunk_size=500):
                guardado = {campo: getattr(comisionado, campo) for campo in CAMPOS_DERIVADOS}
                try:
                    comisionado.recalcular_campos_derivados()
                except Exception as e:
                    errores += 1
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error al recalcular ComisionadoSolicitud {comisionado.pk}: {e}"
                        )
                    )
                    continue

                diferencias = []
                for campo in CAMPOS_DERIVADOS:
                    recalculado = _normalizar(campo, getattr(comisionado, campo))
                    if guardado[campo] != recalculado:
                        diferencias.append((campo, guardado[campo], recalculado))

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
                        comisionado.save(update_fields=CAMPOS_DERIVADOS)
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
