"""
Django management command: sync UVI (Índice Unitario) data from BCRA API.

Fetches historical UVI values from the Central Bank of Argentina's REST API and
persists them in the local database, skipping duplicates.

Usage:
    python manage.py bcra_uvi
"""
import logging

from django.core.management.base import BaseCommand, CommandError
from carga.models import Uvi
from carga.bcra_api import BCAPI

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Synchronize UVI data from BCRA API to the local database."""

    def handle(self, *args, **kwargs):
        with BCAPI() as client:
            idvariable=32
            vars = client.get_variables(idvariable)
            fecha_desde = vars["results"][0]["primerFechaInformada"]
            fecha_hasta = vars["results"][0]["ultFechaInformada"]
            # DB Objects
            last_db_object = Uvi.objects.last()
            last_db_object_date = last_db_object.uvi_fecha if last_db_object else fecha_desde
            data = client.get_variable_historico(idvariable, last_db_object_date, fecha_hasta)
            detalle = sorted(data["results"][0]["detalle"], key=lambda x: x["fecha"])
            for value in detalle:
                uvi_fecha = value["fecha"]
                uvi_valor = value["valor"]
                uvi, created = Uvi.objects.get_or_create(
                    uvi_fecha=uvi_fecha,
                    defaults={"uvi_valor": uvi_valor},
                )
                if created:
                    logger.info("Inserted UVI %s", uvi)