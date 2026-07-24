import re
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from personalizador.models import (
    Agente,
    ActividadEspecifica,
    ApartadoCargo,
    CEIC,
    Categoria,
    Departamento,
    DenominacionCargo,
    Direccion,
    Directorio,
    Gerencia,
    GrupoCargo,
    Oficina,
)

logger = logging.getLogger(__name__)

DEFAULT_PATH = settings.BASE_DIR.parent / "env" / ".snipets" / "informe_ipduv.xlsx"

SHEET_NAME = "PLANTA PERMANENTE"

# Columnas de la hoja "PLANTA PERMANENTE" (0-indexadas). El header de la hoja
# fue renombrado a mano para que coincida con los nombres de campo del modelo
# Agente, pero tiene dos columnas "cuof" (una para el nivel gerencia, otra
# para el nivel departamento/direccion) asi que no se puede armar un dict
# desde la fila de encabezado sin perder una: se hardcodean las posiciones.
COL_N_LEGAJO = 0
COL_DNI = 2
COL_FECHA_NACIMIENTO = 3
COL_CATEGORIA = 5
COL_DENOMINACION_CARGO = 6
COL_APARTADO = 7
COL_CEIC = 8
COL_GRUPO = 9
COL_ACTIVIDAD_CENTRAL = 10
COL_ACTIVIDAD_ESPECIFICA = 11
COL_CUOF_DEPARTAMENTO = 14
COL_DEPARTAMENTO_NOMBRE = 15

FIRST_DATA_ROW = 4


def _blank(raw):
    return raw is None or (isinstance(raw, str) and raw.strip() == "")


def _parse_codigo_nombre(raw):
    """'02 - ADMINISTRACION Y RECURSOS HUMANOS' -> (2, 'ADMINISTRACION Y RECURSOS HUMANOS')"""
    texto = str(raw).strip()
    codigo_str, _, nombre_str = texto.partition("-")
    codigo_str = codigo_str.strip()
    if not codigo_str.isdigit():
        return None, None
    return int(codigo_str), nombre_str.strip()


def _normalize_text(raw):
    return " ".join(str(raw).split())


def _parse_dni(raw):
    if _blank(raw):
        return None
    digitos = re.sub(r"\D", "", str(raw))
    return int(digitos) if digitos else None


def _parse_leading_int(raw):
    if _blank(raw):
        return None
    match = re.match(r"\d+", str(raw).strip())
    return match.group() if match else None


class Command(BaseCommand):
    help = (
        "Importa la hoja 'PLANTA PERMANENTE' de informe_ipduv.xlsx: matchea "
        "Agentes existentes por DNI y completa fecha_nacimiento, n_legajo, "
        "categoria, denominacion_cargo, apartado, ceic, grupo, "
        "activdad_central, actividad_especifica y oficina (esta ultima "
        "resuelta a partir del C.U.O.F. de departamento/direccion contra el "
        "organigrama cargado por fill_data.py + crear_oficinas.py). No crea "
        "Agentes nuevos ni filas de catalogo faltantes (Categoria, "
        "DenominacionCargo, ApartadoCargo, CEIC, GrupoCargo, "
        "ActividadEspecifica, Oficina): si un valor del xlsx no tiene "
        "correspondencia en la base, se salta ese campo puntual para ese "
        "agente y se informa por consola para revision manual. Los campos "
        "vacios en el xlsx tambien se saltean (no se pisan datos existentes "
        "por una celda en blanco)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file", default=str(DEFAULT_PATH),
            help="Ruta al xlsx a importar (default: %(default)s)",
        )
        parser.add_argument(
            "--dry-run", action="store_true",
            help="No guarda cambios en la base de datos, solo informa.",
        )

    def handle(self, *args, **options):
        import openpyxl

        path = options["file"]
        dry_run = options["dry_run"]
        verbosity = options.get("verbosity", 1)

        try:
            wb = openpyxl.load_workbook(path, data_only=True)
        except FileNotFoundError:
            raise CommandError(f"No se encontro el archivo: {path}")

        if SHEET_NAME not in wb.sheetnames:
            raise CommandError(f"La hoja '{SHEET_NAME}' no existe en {path}.")
        ws = wb[SHEET_NAME]

        stats = {"actualizados": 0, "sin_cambios": 0, "no_encontrados": 0, "dni_invalido": 0}
        avisos = []

        with transaction.atomic():
            for row in ws.iter_rows(min_row=FIRST_DATA_ROW, values_only=True):
                if row[COL_N_LEGAJO] is None and row[COL_DNI] is None:
                    continue

                dni = _parse_dni(row[COL_DNI])
                if dni is None:
                    stats["dni_invalido"] += 1
                    avisos.append(f"Fila con N={row[COL_N_LEGAJO]!r}: D.N.I. invalido ({row[COL_DNI]!r}), fila salteada.")
                    continue

                try:
                    agente = Agente.objects.get(dni=dni)
                except Agente.DoesNotExist:
                    stats["no_encontrados"] += 1
                    avisos.append(f"DNI {dni}: no existe ningun Agente con ese DNI, fila salteada.")
                    continue

                updates = self._resolver_campos(row, dni, avisos)

                changed_fields = []
                for field, value in updates.items():
                    if getattr(agente, field) != value:
                        setattr(agente, field, value)
                        changed_fields.append(field)

                if changed_fields:
                    stats["actualizados"] += 1
                    if not dry_run:
                        agente.save()
                    if verbosity >= 2:
                        self.stdout.write(f"DNI {dni}: actualizados {', '.join(changed_fields)}")
                else:
                    stats["sin_cambios"] += 1

            if dry_run:
                transaction.set_rollback(True)

        if verbosity >= 1:
            self.stdout.write("")
            if dry_run:
                self.stdout.write(self.style.NOTICE("Modo dry-run: no se guardo ningun cambio en la base de datos."))
            self.stdout.write(self.style.MIGRATE_HEADING("Resumen:"))
            self.stdout.write(self.style.SUCCESS(f"    Agentes actualizados: {stats['actualizados']}"))
            self.stdout.write(f"    Agentes sin cambios: {stats['sin_cambios']}")
            self.stdout.write(self.style.WARNING(f"    DNI no encontrado en la base: {stats['no_encontrados']}"))
            self.stdout.write(self.style.WARNING(f"    D.N.I. invalido en el xlsx: {stats['dni_invalido']}"))

        if avisos and verbosity >= 1:
            self.stdout.write("")
            self.stdout.write(self.style.MIGRATE_HEADING(f"Avisos ({len(avisos)}):"))
            for aviso in avisos:
                self.stdout.write(f"    {self.style.WARNING(aviso)}")

    def _resolver_campos(self, row, dni, avisos):
        updates = {}

        if not _blank(row[COL_N_LEGAJO]):
            try:
                updates["n_legajo"] = int(row[COL_N_LEGAJO])
            except (TypeError, ValueError):
                avisos.append(f"DNI {dni}: N de legajo invalido ({row[COL_N_LEGAJO]!r}), se salteo el campo.")

        if not _blank(row[COL_FECHA_NACIMIENTO]):
            valor = row[COL_FECHA_NACIMIENTO]
            fecha = valor.date() if hasattr(valor, "date") else valor
            updates["fecha_nacimiento"] = fecha

        if not _blank(row[COL_CATEGORIA]):
            codigo, _nombre = _parse_codigo_nombre(row[COL_CATEGORIA])
            categoria = Categoria.objects.filter(categoria_codigo=codigo).first() if codigo is not None else None
            if categoria:
                updates["categoria"] = categoria
            else:
                avisos.append(f"DNI {dni}: no existe Categoria con codigo {codigo!r} (xlsx: {row[COL_CATEGORIA]!r}), se salteo el campo.")

        if not _blank(row[COL_DENOMINACION_CARGO]):
            normalizado = _normalize_text(row[COL_DENOMINACION_CARGO])
            denominacion = DenominacionCargo.objects.filter(denominacion__iexact=normalizado).first()
            if denominacion:
                updates["denominacion_cargo"] = denominacion
            else:
                avisos.append(f"DNI {dni}: no existe DenominacionCargo '{normalizado}', se salteo el campo.")

        if not _blank(row[COL_APARTADO]):
            valor = str(row[COL_APARTADO]).strip().upper()
            apartado = ApartadoCargo.objects.filter(apartadocargo_denominacion=valor).first()
            if apartado:
                updates["apartado"] = apartado
            else:
                avisos.append(f"DNI {dni}: no existe ApartadoCargo '{valor}', se salteo el campo.")

        if not _blank(row[COL_CEIC]):
            valor = _parse_leading_int(row[COL_CEIC])
            ceic = CEIC.objects.filter(ceic=valor).first() if valor else None
            if ceic:
                updates["ceic"] = ceic
            else:
                avisos.append(f"DNI {dni}: no existe CEIC '{row[COL_CEIC]!r}', se salteo el campo.")

        if not _blank(row[COL_GRUPO]):
            try:
                valor = int(row[COL_GRUPO])
            except (TypeError, ValueError):
                valor = None
            grupo = GrupoCargo.objects.filter(grupo_numero=valor).first() if valor is not None else None
            if grupo:
                updates["grupo"] = grupo
            else:
                avisos.append(f"DNI {dni}: no existe GrupoCargo '{row[COL_GRUPO]!r}', se salteo el campo.")

        if not _blank(row[COL_ACTIVIDAD_CENTRAL]):
            try:
                updates["activdad_central"] = str(int(row[COL_ACTIVIDAD_CENTRAL]))
            except (TypeError, ValueError):
                avisos.append(f"DNI {dni}: ACT. CENTRAL invalida ({row[COL_ACTIVIDAD_CENTRAL]!r}), se salteo el campo.")

        if not _blank(row[COL_ACTIVIDAD_ESPECIFICA]):
            codigo, _nombre = _parse_codigo_nombre(row[COL_ACTIVIDAD_ESPECIFICA])
            actividad = ActividadEspecifica.objects.filter(actividad_especifica_codigo=codigo).first() if codigo is not None else None
            if actividad:
                updates["actividad_especifica"] = actividad
            else:
                avisos.append(f"DNI {dni}: no existe ActividadEspecifica con codigo {codigo!r} (xlsx: {row[COL_ACTIVIDAD_ESPECIFICA]!r}), se salteo el campo.")

        if not _blank(row[COL_CUOF_DEPARTAMENTO]):
            oficina = self._resolver_oficina(row, dni, avisos)
            if oficina is not None:
                updates["oficina"] = oficina

        return updates

    def _resolver_oficina(self, row, dni, avisos):
        try:
            numero = int(row[COL_CUOF_DEPARTAMENTO])
        except (TypeError, ValueError):
            avisos.append(f"DNI {dni}: C.U.O.F. de departamento/direccion invalido ({row[COL_CUOF_DEPARTAMENTO]!r}), se salteo oficina.")
            return None
        cuof = f"10-{numero}-0"
        nombre_xlsx = row[COL_DEPARTAMENTO_NOMBRE]

        departamento = Departamento.objects.filter(departamento_cuof=cuof).first()
        if departamento:
            oficina = Oficina.objects.filter(cargo_departamento=departamento).first()
            nivel, unidad = "Departamento", departamento.departamento_nombre
        else:
            direccion = Direccion.objects.filter(direccion_cuof=cuof).first()
            if direccion:
                oficina = Oficina.objects.filter(cargo_direccion=direccion, cargo_departamento__isnull=True).first()
                nivel, unidad = "Direccion", direccion.direccion_nombre
            else:
                gerencia = Gerencia.objects.filter(gerencia_cuof=cuof).first()
                if gerencia:
                    oficina = Oficina.objects.filter(
                        cargo_gerencia=gerencia, cargo_direccion__isnull=True, cargo_departamento__isnull=True,
                    ).first()
                    nivel, unidad = "Gerencia", gerencia.gerencia_nombre
                else:
                    directorio = Directorio.objects.filter(directorio_cuof=cuof).first()
                    if directorio:
                        oficina = Oficina.objects.filter(
                            cargo_directorio=directorio, cargo_gerencia__isnull=True,
                            cargo_direccion__isnull=True, cargo_departamento__isnull=True,
                        ).first()
                        nivel, unidad = "Directorio", directorio.directorio_nombre
                    else:
                        avisos.append(
                            f"DNI {dni}: no existe ninguna unidad organizativa con C.U.O.F. {cuof} "
                            f"(xlsx: '{nombre_xlsx}'), se salteo oficina."
                        )
                        return None

        if oficina is None:
            avisos.append(
                f"DNI {dni}: existe {nivel} '{unidad}' (C.U.O.F. {cuof}) pero no tiene una Oficina "
                f"asociada; correr 'crear_oficinas' y reintentar. Se salteo oficina."
            )
        return oficina
