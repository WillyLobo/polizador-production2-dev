import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from personalizador.models import (
    ActividadEspecifica,
    ApartadoCargo,
    CargoTipo,
    Categoria,
    CEIC,
    DenominacionCargo,
    GeneroAgente,
    GrupoCargo,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Carga los valores fijos (catalogos) de personalizador a partir de listas "
        "hardcodeadas: DenominacionCargo, GeneroAgente, Categoria, CEIC, GrupoCargo, "
        "CargoTipo y ApartadoCargo. Es re-ejecutable: los valores que ya existen se "
        "saltean, asi que se puede correr de nuevo sin duplicar datos."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Solo informa cuantos registros se crearian, sin guardar nada.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        DENOMINACIONCARGO = [
            "Administrativo 1",
            "Administrativo 4",
            "Administrativo 5",
            "Administrativo 6",
            "Director",
            "Obrero y Maestranza 5",
            "Profesional 1",
            "Profesional 3",
            "Profesional 4",
            "Profesional 5",
            "Profesional 6",
            "Profesional 7",
            "Profesional 8",
            "Profesional 9",
            "Servicios 4",
            "Servicios 5",
            "Servicios 6",
        ]
        GENEROAGENTE = [
            "Masculino",
            "Femenino",
            "No binario",
        ]
        CATEGORIA = {"3": "Personal Administrativo y Técnico", "7": "Personal de Servicio"}  # categoria_codigo : categoria_nombre
        CEIC_LIST = [
            "1018",
            "1025",
            "1024",
            "1042",
            "1035",
            "1043",
            "1017",
            "1040",
            "1041",
            "1051",
            "1026",
            "1019",
            "1016",
            "1030",
            "1036",
            "1029",
            "1022",
            "1020",
        ]
        GRUPOCARGO = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ]
        CARGOTIPO = [
            "Personal de Planta Permanente",
            "Personal Transitorio",
            "Contrato de Servicio",
        ]
        APARTADO = [
            "A",
            "C",
            "D",
        ]
        ACTIVIDADESPECIFICA = {
            "01":"CONDUCCION SUPERIOR",
            "02":"ADMINISTRACION Y RECURSOS HUMANOS",
            "03":"PROGRAMACION Y PROYECTO",
            "04":"DIRECCION Y CONTROL DE OBRA",
            "05":"GESTION DE LA DEMANDA SOCIAL",
        }

        counts = {}

        with transaction.atomic():
            counts["DenominacionCargo"] = self._fill(
                DenominacionCargo, DENOMINACIONCARGO, "denominacion", dry_run,
            )
            counts["GeneroAgente"] = self._fill(
                GeneroAgente, GENEROAGENTE, "generoagente_nombre", dry_run,
            )
            counts["CEIC"] = self._fill(
                CEIC, CEIC_LIST, "ceic", dry_run,
            )
            counts["GrupoCargo"] = self._fill(
                GrupoCargo, GRUPOCARGO, "grupo_numero", dry_run,
            )
            counts["CargoTipo"] = self._fill(
                CargoTipo, CARGOTIPO, "cargotipo", dry_run,
            )
            counts["ApartadoCargo"] = self._fill(
                ApartadoCargo, APARTADO, "apartadocargo_denominacion", dry_run,
            )
            counts["Categoria"] = self._fill_codigo_nombre(
                Categoria, CATEGORIA, "categoria_codigo", "categoria_nombre", dry_run,
            )
            counts["ActividadEspecifica"] = self._fill_codigo_nombre(
                ActividadEspecifica, ACTIVIDADESPECIFICA,
                "actividad_especifica_codigo", "actividad_especifica_nombre", dry_run,
            )

            if dry_run:
                transaction.set_rollback(True)

        verbo = "se crearian" if dry_run else "creados"
        for modelo, creados in counts.items():
            self.stdout.write(self.style.SUCCESS(f"{modelo}: {creados} registros {verbo}"))

    def _fill(self, model, values, field_name, dry_run):
        creados = 0
        vistos = set()
        for valor in values:
            if valor in vistos:
                continue
            vistos.add(valor)

            existe = model.objects.filter(**{field_name: valor}).exists()
            if existe:
                continue
            creados += 1
            if not dry_run:
                model.objects.create(**{field_name: valor})
        return creados

    def _fill_codigo_nombre(self, model, valores, codigo_field, nombre_field, dry_run):
        creados = 0
        for codigo, nombre in valores.items():
            existe = model.objects.filter(**{codigo_field: codigo}).exists()
            if existe:
                continue
            creados += 1
            if not dry_run:
                model.objects.create(**{codigo_field: codigo, nombre_field: nombre})
        return creados
