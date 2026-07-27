import json
import logging
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from personalizador.models import (
    ActividadEspecifica,
    Agente,
    ApartadoCargo,
    CEIC,
    Categoria,
    Departamento,
    DenominacionCargo,
    Direccion,
    Directorio,
    Gerencia,
    GeneroAgente,
    GrupoCargo,
    Oficina,
)

logger = logging.getLogger(__name__)

DEFAULT_PATH = settings.BASE_DIR.parent / "env" / ".snipets" / "agentes_padron.json"


class Command(BaseCommand):
    help = (
        "Aplica sobre esta base de datos (pensado para produccion) el JSON generado "
        "por exportar_agentes_padron: crea los Agente que falten (por D.N.I.) y "
        "actualiza los existentes, resolviendo cada catalogo (Categoria, Oficina, "
        "DenominacionCargo, etc.) por su clave de negocio en ESTA base, no por el PK "
        "de origen. Un campo ausente en un registro del JSON no se toca; un valor de "
        "catalogo que no exista en esta base se informa y se saltea solo ese campo, "
        "sin descartar el resto del registro."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file", default=str(DEFAULT_PATH),
            help="Ruta al JSON a importar (default: %(default)s)",
        )
        parser.add_argument(
            "--dry-run", action="store_true",
            help="No guarda cambios en la base de datos, solo informa.",
        )

    def handle(self, *args, **options):
        path = Path(options["file"])
        dry_run = options["dry_run"]
        verbosity = options.get("verbosity", 1)

        try:
            registros = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise CommandError(f"No se encontro el archivo: {path}")

        stats = {"creados": 0, "actualizados": 0, "sin_cambios": 0, "errores": 0}
        avisos = []

        with transaction.atomic():
            for registro in registros:
                self._procesar(registro, stats, avisos, verbosity)

            if dry_run:
                transaction.set_rollback(True)

        if verbosity >= 1:
            self.stdout.write("")
            if dry_run:
                self.stdout.write(self.style.NOTICE("Modo dry-run: no se guardo ningun cambio en la base de datos."))
            self.stdout.write(self.style.MIGRATE_HEADING("Resumen:"))
            self.stdout.write(self.style.SUCCESS(f"    Agentes creados: {stats['creados']}"))
            self.stdout.write(self.style.SUCCESS(f"    Agentes actualizados: {stats['actualizados']}"))
            self.stdout.write(f"    Agentes sin cambios: {stats['sin_cambios']}")
            self.stdout.write(self.style.ERROR(f"    Errores: {stats['errores']}"))

        if avisos and verbosity >= 1:
            self.stdout.write("")
            self.stdout.write(self.style.MIGRATE_HEADING(f"Avisos ({len(avisos)}):"))
            for aviso in avisos:
                self.stdout.write(f"    {self.style.WARNING(aviso)}")

    def _procesar(self, registro, stats, avisos, verbosity):
        dni = registro["dni"]

        try:
            agente = Agente.objects.get(dni=dni)
            creado = False
        except Agente.DoesNotExist:
            agente, ok = self._crear(registro, dni, avisos)
            if not ok:
                stats["errores"] += 1
                return
            creado = True

        changed_fields = []

        def _set(field, value):
            if getattr(agente, field) != value:
                setattr(agente, field, value)
                if field not in changed_fields:
                    changed_fields.append(field)

        if not creado and registro.get("agente_verificado_contra_padron"):
            _set("agente_nombres", registro["agente_nombres"])
            _set("agente_apellidos", registro["agente_apellidos"])
            _set("agente_verificado_contra_padron", True)
            if "domicilio_direccion" in registro:
                _set("domicilio_direccion", registro["domicilio_direccion"])

        if "n_legajo" in registro:
            _set("n_legajo", registro["n_legajo"])

        if "fecha_nacimiento" in registro:
            _set("fecha_nacimiento", date.fromisoformat(registro["fecha_nacimiento"]))

        if "activdad_central" in registro:
            _set("activdad_central", registro["activdad_central"])

        if "categoria_codigo" in registro:
            categoria = Categoria.objects.filter(categoria_codigo=registro["categoria_codigo"]).first()
            if categoria:
                _set("categoria", categoria)
            else:
                avisos.append(f"DNI {dni}: no existe Categoria con codigo {registro['categoria_codigo']!r}, se salteo el campo.")

        if "denominacion_cargo" in registro:
            denominacion = DenominacionCargo.objects.filter(denominacion__iexact=registro["denominacion_cargo"]).first()
            if denominacion:
                _set("denominacion_cargo", denominacion)
            else:
                avisos.append(f"DNI {dni}: no existe DenominacionCargo {registro['denominacion_cargo']!r}, se salteo el campo.")

        if "apartado" in registro:
            apartado = ApartadoCargo.objects.filter(apartadocargo_denominacion=registro["apartado"]).first()
            if apartado:
                _set("apartado", apartado)
            else:
                avisos.append(f"DNI {dni}: no existe ApartadoCargo {registro['apartado']!r}, se salteo el campo.")

        if "ceic" in registro:
            ceic = CEIC.objects.filter(ceic=registro["ceic"]).first()
            if ceic:
                _set("ceic", ceic)
            else:
                avisos.append(f"DNI {dni}: no existe CEIC {registro['ceic']!r}, se salteo el campo.")

        if "grupo" in registro:
            grupo = GrupoCargo.objects.filter(grupo_numero=registro["grupo"]).first()
            if grupo:
                _set("grupo", grupo)
            else:
                avisos.append(f"DNI {dni}: no existe GrupoCargo {registro['grupo']!r}, se salteo el campo.")

        if "actividad_especifica_codigo" in registro:
            actividad = ActividadEspecifica.objects.filter(actividad_especifica_codigo=registro["actividad_especifica_codigo"]).first()
            if actividad:
                _set("actividad_especifica", actividad)
            else:
                avisos.append(f"DNI {dni}: no existe ActividadEspecifica con codigo {registro['actividad_especifica_codigo']!r}, se salteo el campo.")

        if "oficina" in registro:
            oficina = self._resolver_oficina(registro["oficina"], dni, avisos)
            if oficina:
                _set("oficina", oficina)

        if creado:
            agente.save()
            stats["creados"] += 1
            if verbosity >= 2:
                self.stdout.write(f"DNI {dni}: creado ({agente.agente_apellidos}, {agente.agente_nombres})")
        elif changed_fields:
            agente.save()
            stats["actualizados"] += 1
            if verbosity >= 2:
                self.stdout.write(f"DNI {dni}: actualizados {', '.join(changed_fields)}")
        else:
            stats["sin_cambios"] += 1

    def _crear(self, registro, dni, avisos):
        """Crea el Agente base (dni, nombre, apellido, cuil, sexo) cuando no existe
        en esta base; el resto de los campos se completa despues en _procesar."""
        faltan = [campo for campo in ("agente_nombres", "agente_apellidos", "cuil", "sexo") if campo not in registro]
        if faltan:
            avisos.append(
                f"DNI {dni}: no existe en esta base y el registro no trae {', '.join(faltan)}; "
                f"no se pudo crear el Agente."
            )
            return None, False

        genero = GeneroAgente.objects.filter(generoagente_nombre=registro["sexo"]).first()
        if genero is None:
            avisos.append(f"DNI {dni}: no existe GeneroAgente {registro['sexo']!r} en esta base; no se pudo crear el Agente.")
            return None, False

        agente = Agente(
            dni=dni,
            agente_nombres=registro["agente_nombres"],
            agente_apellidos=registro["agente_apellidos"],
            cuil=registro["cuil"],
            sexo=genero,
        )
        return agente, True

    def _resolver_oficina(self, oficina_key, dni, avisos):
        nivel = oficina_key.get("nivel")
        cuof = oficina_key.get("cuof")

        if nivel == "departamento":
            departamento = Departamento.objects.filter(departamento_cuof=cuof).first()
            oficina = Oficina.objects.filter(cargo_departamento=departamento).first() if departamento else None
        elif nivel == "direccion":
            direccion = Direccion.objects.filter(direccion_cuof=cuof).first()
            oficina = (
                Oficina.objects.filter(cargo_direccion=direccion, cargo_departamento__isnull=True).first()
                if direccion else None
            )
        elif nivel == "gerencia":
            gerencia = Gerencia.objects.filter(gerencia_cuof=cuof).first()
            oficina = (
                Oficina.objects.filter(
                    cargo_gerencia=gerencia, cargo_direccion__isnull=True, cargo_departamento__isnull=True,
                ).first()
                if gerencia else None
            )
        elif nivel == "directorio":
            directorio = Directorio.objects.filter(directorio_cuof=cuof).first()
            oficina = (
                Oficina.objects.filter(
                    cargo_directorio=directorio, cargo_gerencia__isnull=True,
                    cargo_direccion__isnull=True, cargo_departamento__isnull=True,
                ).first()
                if directorio else None
            )
        else:
            avisos.append(f"DNI {dni}: nivel de oficina desconocido {nivel!r}, se salteo oficina.")
            return None

        if oficina is None:
            avisos.append(f"DNI {dni}: no existe ninguna Oficina con nivel {nivel!r} y CUOF {cuof!r} en esta base, se salteo oficina.")
        return oficina
