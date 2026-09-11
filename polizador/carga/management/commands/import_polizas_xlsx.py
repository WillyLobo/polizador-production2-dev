"""
Django management command: importa pólizas y sus movimientos desde una planilla
Excel (.xlsx) hacia los modelos Poliza / Poliza_Movimiento.

Formato esperado de la planilla (una fila por movimiento; varias filas pueden
corresponder a la misma póliza, repitiendo sus datos, cuando el mismo Recibo/
Póliza se envía a distintas áreas/receptores en distintas fechas):

    Fecha | Receptor | Area | Expediente | Concepto de Poliza | N de poliza |
    Anexo de Poliza | Recibo de Pago | Entidad Aseguradora | Obra |
    Convenio Especifico | Expediente Madre | Empresa-Tomador |
    Monto Sustituido | Monto Letra | UVI | UVI Letra

Reglas de importación:
  - Las filas se agrupan por (Expediente, N de poliza): cada grupo produce un
    único Poliza y un Poliza_Movimiento por fila del grupo.
  - Poliza.poliza_fecha se toma como la fecha mínima entre los movimientos del
    grupo (la planilla no trae una fecha de póliza separada de la de cada
    movimiento).
  - La Obra se vincula por "Expediente Madre" (Obra.obra_expediente), nunca
    por nombre de obra, salvo como desempate cuando el expediente madre
    coincide con más de una Obra (ver _resolve_obra) — en la base hay Obras
    con obra_expediente="0" (placeholder sin valor real) y algunos
    expedientes repetidos entre una obra y sus "Reconocimiento de
    gastos/trabajos" asociados.
  - Aseguradora/Empresa se resuelven por nombre normalizado (sin acentos,
    mayúsculas, espacios colapsados). Los alias conocidos que no matchean así
    están en ASEGURADORA_ALIASES; completar ahí si aparecen nuevos.
  - Por defecto NO se crean Empresas nuevas si el tomador no existe; pasar
    --create-empresas para crearlas automáticamente (quedan igual auditadas
    en el reporte).
  - Corre en modo dry-run por defecto: no persiste nada. Pasar --commit para
    grabar los cambios.
  - Se genera siempre un CSV con el detalle de lo creado/omitido (ver
    --report).

Uso:
    python manage.py import_polizas_xlsx ruta/Polizas.xlsx
    python manage.py import_polizas_xlsx ruta/Polizas.xlsx --commit
    python manage.py import_polizas_xlsx ruta/Polizas.xlsx --commit --create-empresas --report import_polizas.csv
"""
import csv
import difflib
import re
import unicodedata
from collections import OrderedDict, defaultdict
from datetime import date, datetime

import openpyxl
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from carga.models import Area, Aseguradora, Empresa, Obra, Poliza, Poliza_Movimiento, Receptor

EXPECTED_HEADERS = [
    "Fecha",
    "Receptor",
    "Area",
    "Expediente",
    "Concepto de Poliza",
    "N de poliza",
    "Anexo de Poliza",
    "Recibo de Pago",
    "Entidad Aseguradora",
    "Obra",
    "Convenio Especifico",
    "Expediente Madre",
    "Empresa-Tomador",
    "Monto Sustituido",
    "Monto Letra",
    "UVI",
    "UVI Letra",
]

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}

DATE_RE = re.compile(r"^\s*(\d{1,2})\s+de\s+([a-zñ]+)\s+de\s+(\d{4})\s*$", re.IGNORECASE)

# Alias manuales para razones sociales que no matchean ni siquiera normalizadas
# (mayúsculas/acentos/espacios) con lo cargado en la base. Completar antes de
# correr en producción si el reporte marca nuevas ASEGURADORA_NO_ENCONTRADA /
# EMPRESA_NO_ENCONTRADA que en realidad son alguna de estas con otro nombre.
ASEGURADORA_ALIASES = {
    "ASEGURADORES DE CAUCIONES S.A.": "Aseguradores de Cauciones S.A. Compañía de Seguros",
    # "CAUCIONES SEGUROS": "???",  # ambiguo entre las dos aseguradoras de "Cauciones" -> definir a mano
}

EMPRESA_ALIASES = {
    # "NOMBRE EN PLANILLA": "Nombre exacto en la base",
}

# Valores de obra_expediente que existen en la base como placeholder y nunca
# deben interpretarse como un vínculo real a una Obra.
OBRA_EXPEDIENTE_PLACEHOLDERS = {"", "0"}


def strip_accents(value):
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()


def normalize(value):
    """Clave insensible a acentos/mayúsculas/espacios, para matchear por nombre."""
    if value is None:
        return ""
    value = strip_accents(str(value))
    value = re.sub(r"\s+", " ", value).strip().upper().rstrip(".")
    return value


def parse_fecha(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    match = DATE_RE.match(str(value or ""))
    if not match:
        return None
    day, month_name, year = match.groups()
    month = MESES.get(strip_accents(month_name).lower())
    if not month:
        return None
    try:
        return date(int(year), month, int(day))
    except ValueError:
        return None


def concepto_code(text):
    n = normalize(text)
    if "ANTICIPO" in n:
        return "A"
    if "REPARO" in n or "FONDO" in n:
        return "F"
    if "CONTRATO" in n:
        return "C"
    return None


def first_non_empty(values):
    for v in values:
        if v not in (None, ""):
            return v
    return None


class ImportRow:
    __slots__ = ("fecha_raw", "receptor", "area", "expediente", "concepto", "numero",
                 "anexo", "recibo", "aseguradora", "obra_nombre", "exp_madre",
                 "tomador", "monto", "uvi", "excel_row")

    def __init__(self, values, excel_row):
        (self.fecha_raw, self.receptor, self.area, self.expediente, self.concepto,
         self.numero, self.anexo, self.recibo, self.aseguradora, self.obra_nombre,
         _convenio, self.exp_madre, self.tomador, self.monto, _monto_letra,
         self.uvi, _uvi_letra) = values
        self.excel_row = excel_row


class Command(BaseCommand):
    help = "Importa pólizas y movimientos desde una planilla .xlsx hacia Poliza/Poliza_Movimiento."

    def add_arguments(self, parser):
        parser.add_argument("xlsx_path", type=str, help="Ruta al archivo .xlsx")
        parser.add_argument("--sheet", type=str, default=None, help="Nombre de la hoja (default: la primera)")
        parser.add_argument("--commit", action="store_true", help="Graba los cambios. Sin esta opción corre en dry-run.")
        parser.add_argument(
            "--create-empresas",
            action="store_true",
            help="Crea automáticamente las Empresas (tomador) que no existan en la base.",
        )
        parser.add_argument(
            "--report",
            type=str,
            default="import_polizas_report.csv",
            help="Ruta del CSV de reporte (default: import_polizas_report.csv)",
        )

    def handle(self, *args, **options):
        xlsx_path = options["xlsx_path"]
        commit = options["commit"]
        create_empresas = options["create_empresas"]
        report_path = options["report"]

        rows = self._read_rows(xlsx_path, options["sheet"])
        groups = self._group_rows(rows)

        report_lines = []
        stats = defaultdict(int)

        aseguradora_cache = {normalize(a.aseguradora_nombre): a for a in Aseguradora.objects.all()}
        empresa_cache = {normalize(e.empresa_nombre): e for e in Empresa.objects.all()}
        receptor_cache = {normalize(r.receptor_nombre): r for r in Receptor.objects.all()}
        area_cache = {normalize(a.area_nombre): a for a in Area.objects.all()}

        numero_a_expedientes = defaultdict(set)
        for (expediente, numero) in groups:
            numero_a_expedientes[numero].add(expediente)
        numeros_reutilizados = {n for n, exps in numero_a_expedientes.items() if len(exps) > 1}

        with transaction.atomic():
            for (expediente, numero), grp_rows in groups.items():
                self._process_group(
                    expediente, numero, grp_rows,
                    aseguradora_cache, empresa_cache, receptor_cache, area_cache,
                    numeros_reutilizados, create_empresas, report_lines, stats,
                )

            if not commit:
                transaction.set_rollback(True)

        self._write_report(report_path, report_lines)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Grupos (pólizas) procesados: {len(groups)}"))
        self.stdout.write(f"  Pólizas creadas:        {stats['poliza_creada']}")
        self.stdout.write(f"  Pólizas ya existentes:  {stats['poliza_existente']}")
        self.stdout.write(f"  Movimientos creados:    {stats['movimiento_creado']}")
        self.stdout.write(f"  Movimientos existentes: {stats['movimiento_existente']}")
        self.stdout.write(f"  Empresas creadas:       {stats['empresa_creada']}")
        self.stdout.write(self.style.WARNING(f"  Grupos omitidos:        {stats['grupo_omitido']}"))
        self.stdout.write(f"Reporte detallado: {report_path}")
        if not commit:
            self.stdout.write(self.style.WARNING("Dry-run: no se grabó ningún cambio. Repetir con --commit para persistir."))

    # ------------------------------------------------------------------
    # Lectura / parsing de la planilla
    # ------------------------------------------------------------------
    def _read_rows(self, xlsx_path, sheet_name):
        try:
            wb = openpyxl.load_workbook(xlsx_path, data_only=True)
        except FileNotFoundError as exc:
            raise CommandError(f"No se encontró el archivo: {xlsx_path}") from exc

        ws = wb[sheet_name] if sheet_name else wb[wb.sheetnames[0]]

        header_row = None
        header_row_idx = None
        for idx, row in enumerate(ws.iter_rows(min_row=1, max_row=5, values_only=True), start=1):
            normalized = {normalize(c) for c in row if c}
            if normalize("Fecha") in normalized and normalize("N de poliza") in normalized:
                header_row = row
                header_row_idx = idx
                break
        if header_row is None:
            raise CommandError("No se encontró la fila de encabezados esperada en las primeras 5 filas de la hoja.")

        col_index = {normalize(c): i for i, c in enumerate(header_row) if c}
        missing = [h for h in EXPECTED_HEADERS if normalize(h) not in col_index]
        if missing:
            raise CommandError(f"Faltan columnas esperadas en la planilla: {', '.join(missing)}")

        order = [col_index[normalize(h)] for h in EXPECTED_HEADERS]

        rows = []
        for excel_row_idx, raw in enumerate(ws.iter_rows(min_row=header_row_idx + 1, values_only=True), start=header_row_idx + 1):
            values = [raw[i] if i < len(raw) else None for i in order]
            expediente, numero = values[3], values[5]
            if expediente is None or numero is None:
                continue
            rows.append(ImportRow(values, excel_row_idx))
        return rows

    def _group_rows(self, rows):
        groups = OrderedDict()
        for row in rows:
            key = (str(row.expediente).strip(), int(row.numero))
            groups.setdefault(key, []).append(row)
        return groups

    # ------------------------------------------------------------------
    # Procesamiento por grupo (= una póliza)
    # ------------------------------------------------------------------
    def _process_group(self, expediente, numero, grp_rows, aseguradora_cache, empresa_cache,
                        receptor_cache, area_cache, numeros_reutilizados, create_empresas,
                        report_lines, stats):

        def skip(reason, detail=""):
            stats["grupo_omitido"] += 1
            report_lines.append({
                "expediente": expediente, "numero": numero, "estado": "OMITIDO",
                "motivo": reason, "detalle": detail,
                "filas_excel": ",".join(str(r.excel_row) for r in grp_rows),
            })

        if numero in numeros_reutilizados:
            skip("NUMERO_POLIZA_REUTILIZADO", f"N° {numero} aparece con expedientes distintos en la planilla")
            return

        # Consistencia de los campos que deberían ser constantes dentro del grupo.
        for field, label in (
            ("aseguradora", "aseguradora"), ("tomador", "tomador"), ("exp_madre", "expediente madre"),
            ("concepto", "concepto"), ("monto", "monto"), ("anexo", "anexo"), ("recibo", "recibo"),
        ):
            values = {getattr(r, field) for r in grp_rows if getattr(r, field) not in (None, "")}
            if len(values) > 1:
                skip("CONFLICTO_DATOS", f"{label} varía entre filas del grupo: {values}")
                return

        recibo = first_non_empty(r.recibo for r in grp_rows)
        if recibo is None:
            skip("RECIBO_FALTANTE")
            return

        concepto = concepto_code(first_non_empty(r.concepto for r in grp_rows))
        if concepto is None:
            skip("CONCEPTO_DESCONOCIDO", repr(first_non_empty(r.concepto for r in grp_rows)))
            return

        exp_madre = first_non_empty(r.exp_madre for r in grp_rows)
        obra, obra_reason = self._resolve_obra(exp_madre, first_non_empty(r.obra_nombre for r in grp_rows))
        if obra is None:
            skip(obra_reason, exp_madre or "")
            return

        aseguradora_raw = first_non_empty(r.aseguradora for r in grp_rows)
        aseguradora = self._resolve_aseguradora(aseguradora_raw, aseguradora_cache)
        if aseguradora is None:
            skip("ASEGURADORA_NO_ENCONTRADA", aseguradora_raw or "")
            return

        tomador_raw = first_non_empty(r.tomador for r in grp_rows)
        tomador = self._resolve_empresa(tomador_raw, empresa_cache, create_empresas, stats)
        if tomador is None:
            skip("EMPRESA_NO_ENCONTRADA", tomador_raw or "")
            return

        fechas = [parse_fecha(r.fecha_raw) for r in grp_rows]
        fechas_validas = [f for f in fechas if f]
        if not fechas_validas:
            skip("FECHA_INVALIDA", repr([r.fecha_raw for r in grp_rows]))
            return
        poliza_fecha = min(fechas_validas)

        anexo = first_non_empty(r.anexo for r in grp_rows)
        monto = first_non_empty(r.monto for r in grp_rows)
        uvi = first_non_empty(r.uvi for r in grp_rows)

        poliza, created = Poliza.objects.get_or_create(
            poliza_fecha=poliza_fecha,
            poliza_numero=numero,
            poliza_aseguradora=aseguradora,
            poliza_tomador=tomador,
            defaults={
                "poliza_expediente": expediente,
                "poliza_concepto": concepto,
                "poliza_anexo": anexo,
                "poliza_recibo": str(recibo),
                "poliza_obra": obra,
                "poliza_monto_pesos": monto,
                "poliza_monto_uvi": uvi,
            },
        )
        stats["poliza_creada" if created else "poliza_existente"] += 1
        report_lines.append({
            "expediente": expediente, "numero": numero,
            "estado": "CREADA" if created else "YA_EXISTIA",
            "motivo": "", "detalle": f"poliza_id={poliza.pk} obra_id={obra.pk}",
            "filas_excel": ",".join(str(r.excel_row) for r in grp_rows),
        })

        for row in grp_rows:
            fecha_mov = parse_fecha(row.fecha_raw)
            receptor = receptor_cache.get(normalize(row.receptor))
            area = area_cache.get(normalize(row.area))
            if not (fecha_mov and receptor and area):
                report_lines.append({
                    "expediente": expediente, "numero": numero, "estado": "MOVIMIENTO_OMITIDO",
                    "motivo": "RECEPTOR_AREA_O_FECHA_INVALIDA",
                    "detalle": f"fecha={row.fecha_raw!r} receptor={row.receptor!r} area={row.area!r}",
                    "filas_excel": str(row.excel_row),
                })
                continue

            movimiento, mov_created = Poliza_Movimiento.objects.get_or_create(
                poliza_movimiento_numero=poliza,
                poliza_movimiento_receptor=receptor,
                poliza_movimiento_area=area,
                poliza_movimiento_fecha=fecha_mov,
            )
            stats["movimiento_creado" if mov_created else "movimiento_existente"] += 1

    # ------------------------------------------------------------------
    # Resolución de entidades relacionadas
    # ------------------------------------------------------------------
    def _resolve_obra(self, exp_madre, obra_nombre_planilla):
        if not exp_madre or exp_madre.strip() in OBRA_EXPEDIENTE_PLACEHOLDERS:
            return None, "EXPEDIENTE_MADRE_FALTANTE"

        candidatos = list(Obra.objects.filter(obra_expediente__iexact=exp_madre.strip()))
        if not candidatos:
            return None, "OBRA_NO_ENCONTRADA"
        if len(candidatos) == 1:
            return candidatos[0], None

        # Más de una Obra comparte el mismo expediente madre (frecuente con
        # "Reconocimiento de gastos/trabajos" asociados a la obra principal).
        # Desempatar por similitud con el nombre de obra de la planilla —
        # nunca al revés (el expediente madre sigue siendo la clave primaria).
        objetivo = normalize(obra_nombre_planilla)
        ranked = sorted(
            candidatos,
            key=lambda c: difflib.SequenceMatcher(None, objetivo, normalize(c.obra_nombre)).ratio(),
            reverse=True,
        )
        best, second = ranked[0], ranked[1]
        best_ratio = difflib.SequenceMatcher(None, objetivo, normalize(best.obra_nombre)).ratio()
        second_ratio = difflib.SequenceMatcher(None, objetivo, normalize(second.obra_nombre)).ratio()
        if best_ratio >= 0.5 and (best_ratio - second_ratio) >= 0.1:
            return best, None
        return None, "OBRA_AMBIGUA"

    def _resolve_aseguradora(self, raw, cache):
        if not raw:
            return None
        key = normalize(raw)
        if key in cache:
            return cache[key]
        alias = ASEGURADORA_ALIASES.get(raw.strip()) or ASEGURADORA_ALIASES.get(key)
        if alias:
            return cache.get(normalize(alias))
        return None

    def _resolve_empresa(self, raw, cache, create_empresas, stats):
        if not raw:
            return None
        key = normalize(raw)
        if key in cache:
            return cache[key]
        alias = EMPRESA_ALIASES.get(raw.strip()) or EMPRESA_ALIASES.get(key)
        if alias and normalize(alias) in cache:
            return cache[normalize(alias)]
        if not create_empresas:
            return None
        empresa = Empresa.objects.create(empresa_nombre=raw.strip())
        cache[key] = empresa
        stats["empresa_creada"] += 1
        return empresa

    # ------------------------------------------------------------------
    def _write_report(self, path, report_lines):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["expediente", "numero", "estado", "motivo", "detalle", "filas_excel"])
            writer.writeheader()
            writer.writerows(report_lines)
