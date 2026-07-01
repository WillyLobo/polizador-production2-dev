"""
Django management command: sync UVI (Índice Unitario) data from BCRA API.

Fetches historical UVI values from the Central Bank of Argentina's REST API
and persists them in the local database, skipping duplicates.

Endpoints used:
  GET /estadisticas/v4.0/Monetarias?IdVariable=32        — metadata (primerFechaInformada, ultFechaInformada)
  GET /estadisticas/v4.0/Monetarias/32?Desde=&Hasta=&Offset=&Limit=  — historical values (max 3000/page)

Usage:
    python manage.py bcra_uvi
    python manage.py bcra_uvi --full-sync
    python manage.py bcra_uvi --verbosity 2   # INFO
    python manage.py bcra_uvi --verbosity 3   # DEBUG
"""
import logging
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError

from carga.bcra_api import BCAPI, BCRAError
from carga.models import Uvi

logger = logging.getLogger(__name__)

ID_VARIABLE_UVI = 32
PAGE_SIZE = 3000  # API máximo permitido


class Command(BaseCommand):
    """Sincroniza valores diarios de UVI desde la API pública del BCRA."""

    help = "Sincroniza valores UVI desde la API del BCRA (variable 32)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--full-sync",
            action="store_true",
            help=(
                "Descarga toda la serie histórica desde primerFechaInformada, "
                "ignorando los registros existentes en la DB (los duplicados se omiten)."
            ),
        )

    def handle(self, *args, **kwargs):
        verbosity = kwargs["verbosity"]
        self._configure_logging(verbosity)

        full_sync = kwargs["full_sync"]

        try:
            self._run(full_sync)
        except BCRAError as exc:
            raise CommandError(f"Error en la API del BCRA: {exc}") from exc

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------

    def _run(self, full_sync: bool) -> None:
        with BCAPI() as client:
            logger.debug("Consultando metadata de variable %d…", ID_VARIABLE_UVI)
            meta = client.get_variables(id_variable=ID_VARIABLE_UVI)

            try:
                var_info = meta["results"][0]
            except (KeyError, IndexError) as exc:
                raise BCRAError(f"Respuesta inesperada de /Monetarias: {meta}") from exc

            fecha_desde_api: str = var_info["primerFechaInformada"]
            fecha_hasta_api: str = var_info["ultFechaInformada"]

            logger.debug(
                "Variable %d — rango API: %s → %s",
                ID_VARIABLE_UVI,
                fecha_desde_api,
                fecha_hasta_api,
            )

            if full_sync:
                start_date = fecha_desde_api
                logger.info(
                    "Modo full-sync: descargando desde primerFechaInformada (%s).",
                    start_date,
                )
            else:
                last = Uvi.objects.order_by("uvi_fecha").last()
                if last:
                    # Empezamos desde el día siguiente al último registro para no re-insertar
                    start_date = (last.uvi_fecha + timedelta(days=1)).isoformat()
                    logger.info(
                        "Último registro en DB: %s — descargando desde %s.",
                        last.uvi_fecha,
                        start_date,
                    )
                else:
                    start_date = fecha_desde_api
                    logger.info(
                        "DB vacía — descargando desde primerFechaInformada (%s).",
                        start_date,
                    )

            if start_date > fecha_hasta_api:
                logger.info("La DB ya está al día (último valor API: %s).", fecha_hasta_api)
                self.stdout.write(self.style.SUCCESS("Sin datos nuevos que sincronizar."))
                return

            total_inserted, total_skipped = self._sync_pages(
                client, start_date, fecha_hasta_api
            )

        msg = f"UVI sincronizado: {total_inserted} insertados, {total_skipped} duplicados omitidos."
        logger.info(msg)
        self.stdout.write(self.style.SUCCESS(msg))

    def _sync_pages(self, client: BCAPI, desde: str, hasta: str) -> tuple[int, int]:
        """Descarga y persiste todas las páginas del rango dado. Retorna (insertados, omitidos)."""
        total_inserted = 0
        total_skipped = 0
        offset = 0
        page_num = 0

        while True:
            page_num += 1
            logger.debug(
                "Página %d — offset=%d, limit=%d, desde=%s, hasta=%s",
                page_num,
                offset,
                PAGE_SIZE,
                desde,
                hasta,
            )

            data = client.get_variable_historico(
                ID_VARIABLE_UVI,
                desde=desde,
                hasta=hasta,
                offset=offset,
                limit=PAGE_SIZE,
            )

            try:
                detalle = data["results"][0]["detalle"]
            except (KeyError, IndexError, TypeError) as exc:
                raise BCRAError(
                    f"Respuesta inesperada en página {page_num} (offset={offset}): {data}"
                ) from exc

            if not detalle:
                logger.debug("Página %d vacía — fin de datos.", page_num)
                break

            logger.debug("Página %d: %d registros recibidos.", page_num, len(detalle))

            detalle_sorted = sorted(detalle, key=lambda x: x["fecha"])
            inserted, skipped = self._persist(detalle_sorted)
            total_inserted += inserted
            total_skipped += skipped

            logger.info(
                "Página %d: %d insertados, %d omitidos (acumulado: %d / %d).",
                page_num,
                inserted,
                skipped,
                total_inserted,
                total_skipped,
            )

            if len(detalle) < PAGE_SIZE:
                logger.debug(
                    "Página %d incompleta (%d < %d) — última página.",
                    page_num,
                    len(detalle),
                    PAGE_SIZE,
                )
                break

            offset += PAGE_SIZE

        return total_inserted, total_skipped

    def _persist(self, detalle: list[dict]) -> tuple[int, int]:
        """Inserta registros UVI en la DB. Retorna (insertados, omitidos)."""
        inserted = 0
        skipped = 0
        for item in detalle:
            uvi_fecha = item["fecha"]
            uvi_valor = item["valor"]
            _, created = Uvi.objects.get_or_create(
                uvi_fecha=uvi_fecha,
                defaults={"uvi_valor": uvi_valor},
            )
            if created:
                inserted += 1
                logger.debug("  Insertado UVI %s = %s", uvi_fecha, uvi_valor)
            else:
                skipped += 1
                logger.debug("  Omitido (ya existe) UVI %s", uvi_fecha)
        return inserted, skipped

    # ------------------------------------------------------------------
    # Logging setup
    # ------------------------------------------------------------------

    def _configure_logging(self, verbosity: int) -> None:
        """Mapea --verbosity de Django a niveles de logging estándar.

        0 → ERROR  (solo errores críticos)
        1 → WARNING (default Django)
        2 → INFO
        3 → DEBUG
        """
        level_map = {
            0: logging.ERROR,
            1: logging.WARNING,
            2: logging.INFO,
            3: logging.DEBUG,
        }
        level = level_map.get(verbosity, logging.DEBUG)
        logging.getLogger("carga").setLevel(level)
        logger.setLevel(level)

        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            fmt = "%(levelname)s %(name)s: %(message)s"
            if verbosity >= 3:
                fmt = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
            handler.setFormatter(logging.Formatter(fmt))
            logger.addHandler(handler)
            logger.propagate = False
