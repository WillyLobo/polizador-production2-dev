"""Catálogo de columnas seleccionables de los reportes de Obras y de Certificados.

Cada reporte declara qué columnas puede mostrar (campos del modelo, de la Obra padre
en el caso de Certificados, y columnas calculadas). La vista recibe las claves elegidas
por GET (?col=...), y solo precarga/anota lo que esas columnas necesitan.
"""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Callable, Optional

from django.db.models import Count, DecimalField, IntegerField, Max, OuterRef, Prefetch, Q, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.formats import date_format, number_format
from django.utils.html import format_html
from django.utils.text import capfirst

from carga.models import Certificado
from personalizador.models import RepresentanteTecnico

GRUPO_OBRA = "Obra"
GRUPO_CERTIFICADO = "Certificado"
GRUPO_CALCULADOS = "Calculados"

# Formatos con valor numérico/fecha: la celda lleva data-order con el valor crudo, para
# ordenar y sumar en el cliente sin parsear el texto localizado.
FORMATOS_ORDENABLES = {"decimal", "fecha", "periodo"}


@dataclass(frozen=True)
class Celda:
    texto: Any
    orden: Optional[str] = None


@dataclass(frozen=True)
class Columna:
    clave: str
    etiqueta: str
    grupo: str
    valor: Callable[[Any], Any]
    formato: str = "texto"  # texto | decimal | fecha | periodo | bool
    decimales: int = 2
    select_related: tuple = ()
    prefetch_related: tuple = ()
    # Callable sin argumentos que devuelve un dict {nombre: expresión} para queryset.annotate().
    anotaciones: Optional[Callable[[], dict]] = None
    sumable: bool = False
    # Callable(obj) -> URL: la celda se muestra como link.
    enlace: Optional[Callable[[Any], str]] = None

    def celda(self, obj):
        crudo = self.valor(obj)
        orden = None
        if self.formato in FORMATOS_ORDENABLES:
            orden = "" if crudo is None else (crudo.isoformat() if self.formato != "decimal" else str(crudo))
        if crudo is None or crudo == "":
            texto = "-"
        elif self.formato == "decimal":
            texto = number_format(crudo, self.decimales, use_l10n=True, force_grouping=True)
        elif self.formato == "fecha":
            texto = date_format(crudo, "d/m/Y")
        elif self.formato == "periodo":
            texto = capfirst(date_format(crudo, "F/Y"))
        elif self.formato == "bool":
            texto = "Sí" if crudo else "No"
        else:
            texto = crudo
        if self.enlace and crudo not in (None, ""):
            texto = format_html('<a href="{}">{}</a>', self.enlace(obj), texto)
        return Celda(texto=texto, orden=orden)


@dataclass
class Reporte:
    columnas: list
    defaults: list
    # (clave, "asc"|"desc"): orden inicial de la tabla, si esa columna fue elegida.
    orden_inicial: tuple
    _por_clave: dict = field(init=False, repr=False)

    def __post_init__(self):
        # Orden del catálogo: primero las columnas por defecto en su orden histórico,
        # luego el resto en el orden en que se declararon.
        por_clave = {c.clave: c for c in self.columnas}
        primero = [por_clave[c] for c in self.defaults]
        self.columnas = primero + [c for c in self.columnas if c.clave not in self.defaults]
        self._por_clave = por_clave

    def seleccionar(self, claves):
        """Columnas elegidas, en el orden del catálogo. Las claves desconocidas se
        ignoran; si no queda ninguna válida, se usan las columnas por defecto."""
        elegidas = {c for c in claves if c in self._por_clave}
        if not elegidas:
            elegidas = set(self.defaults)
        return [c for c in self.columnas if c.clave in elegidas]

    def preparar_queryset(self, qs, columnas):
        select_related, prefetch_related, anotaciones = [], [], {}
        for c in columnas:
            select_related += [s for s in c.select_related if s not in select_related]
            for p in c.prefetch_related:
                lookup = p.prefetch_to if isinstance(p, Prefetch) else p
                if lookup not in [getattr(x, "prefetch_to", x) for x in prefetch_related]:
                    prefetch_related.append(p)
            if c.anotaciones:
                anotaciones.update(c.anotaciones())
        if select_related:
            qs = qs.select_related(*select_related)
        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)
        if anotaciones:
            qs = qs.annotate(**anotaciones)
        return qs

    def grupos(self, columnas):
        """[(grupo, [(columna, elegida)])] para el selector, en el orden del catálogo."""
        elegidas = {c.clave for c in columnas}
        resultado = {}
        for c in self.columnas:
            resultado.setdefault(c.grupo, []).append((c, c.clave in elegidas))
        return list(resultado.items())

    def indice_orden_inicial(self, columnas):
        clave, _ = self.orden_inicial
        for i, c in enumerate(columnas):
            if c.clave == clave:
                return i
        return None


def _display(campo):
    return lambda o: getattr(o, f"get_{campo}_display")()


def _lista(relacion):
    # .all() reutiliza el prefetch_related declarado en la columna.
    return lambda o: ", ".join(str(x) for x in getattr(o, relacion).all()) or None


def _columnas_obra(prefijo, obra_de, en_certificado):
    """Columnas de Obra. prefijo es el path ORM desde el modelo base del reporte hasta
    Obra ("" en el reporte de Obras, "certificado_obra__" en el de Certificados), y
    obra_de(obj) devuelve la Obra de cada fila."""
    p = prefijo
    sr_obra = (prefijo.rstrip("_"),) if prefijo else ()

    def col(clave, etiqueta, valor, select_related=(), prefetch_related=(), **kwargs):
        return Columna(
            clave=clave,
            etiqueta=etiqueta,
            grupo=GRUPO_OBRA,
            valor=lambda o: valor(obra_de(o)),
            select_related=sr_obra + tuple(p + s for s in select_related),
            prefetch_related=tuple(
                Prefetch(p + x.prefetch_through, queryset=x.queryset) if isinstance(x, Prefetch) else p + x
                for x in prefetch_related
            ),
            **kwargs,
        )

    def campo(nombre):
        return lambda obra: getattr(obra, nombre)

    expediente = "Expediente de Obra" if en_certificado else "Expediente"
    return [
        col("obra_id", "ID Obra" if en_certificado else "ID#", lambda obra: str(obra.pk)),
        col("obra_nombre", "Obra", campo("obra_nombre")),
        col("obra_soluciones", "Soluciones", campo("obra_soluciones"), formato="decimal", decimales=0, sumable=not en_certificado),
        col("obra_empresa", "Empresa", lambda o: o.obra_empresa.empresa_nombre, select_related=("obra_empresa",)),
        col("obra_region", "Región", lambda o: o.obra_region, select_related=("obra_region",)),
        col("obra_departamento_m", "Departamento", _lista("obra_departamento_m"), prefetch_related=("obra_departamento_m",)),
        col("obra_municipio_m", "Municipio", _lista("obra_municipio_m"), prefetch_related=("obra_municipio_m",)),
        col("obra_localidad_m", "Localidad", _lista("obra_localidad_m"), prefetch_related=("obra_localidad_m",)),
        col("obra_conjunto", "Conjunto Licitado", lambda o: o.obra_conjunto, select_related=("obra_conjunto",)),
        col("obra_grupo", "Grupo", campo("obra_grupo")),
        col("obra_plazo", "Plazo de Ejecución", campo("obra_plazo")),
        col("obra_programa", "Programa", lambda o: o.obra_programa, select_related=("obra_programa",)),
        col("obra_convenio", "Convenio", campo("obra_convenio")),
        col("obra_expediente", expediente, campo("obra_expediente")),
        col("obra_resolucion_display", "Resolución de Adjudicación", campo("obra_resolucion_display"), select_related=("obra_resolucion_fk",)),
        col("obra_resolucion_tipo", "Resolución - Tipo", _display("obra_resolucion_tipo")),
        col("obra_resolucion_ano", "Resolución - Año", campo("obra_resolucion_ano")),
        col("obra_resolucion_numero", "Resolución - Número", campo("obra_resolucion_numero")),
        col("obra_resolucion_jurisdiccion", "Resolución - Jurisdicción", campo("obra_resolucion_jurisdiccion")),
        col("obra_resolucion_acta", "Resolución - Acta", campo("obra_resolucion_acta")),
        col("obra_licitacion_tipo", "Compulsa", _display("obra_licitacion_tipo")),
        col("obra_licitacion_numero", "Número de Licitación", campo("obra_licitacion_numero"), formato="decimal", decimales=0),
        col("obra_licitacion_ano", "Año de Licitación", lambda o: o.obra_licitacion_ano and int(o.obra_licitacion_ano)),
        col("obra_nomenclatura", "Nomenclatura Catastral", campo("obra_nomenclatura")),
        col("obra_nomenclatura_plano", "Número de Plano", campo("obra_nomenclatura_plano")),
        col("obra_fecha_entrega", "Fecha de Entrega", campo("obra_fecha_entrega"), formato="fecha"),
        col("obra_fecha_contrato", "Fecha de Firma de Contrato", campo("obra_fecha_contrato"), formato="fecha"),
        col("obra_fecha_inicio", "Fecha de Inicio", campo("obra_fecha_inicio"), formato="fecha"),
        col("obra_expediente_costo", "Expediente de Costos", campo("obra_expediente_costo")),
        col("obra_inspector", "Inspector", _lista("obra_inspector"), prefetch_related=("obra_inspector",)),
        col(
            "obra_representantetecnico", "Representante Técnico", _lista("obra_representantetecnico"),
            prefetch_related=(Prefetch(
                "obra_representantetecnico",
                queryset=RepresentanteTecnico.objects.select_related("representantetecnico_profesion"),
            ),),
        ),
        col("obra_contrato_nacion_pesos", "Monto Nación Pesos", campo("obra_contrato_nacion_pesos"), formato="decimal", sumable=not en_certificado),
        col("obra_contrato_nacion_uvi", "Monto Nación UVI", campo("obra_contrato_nacion_uvi"), formato="decimal", sumable=not en_certificado),
        col("obra_contrato_nacion_uvi_fecha", "Fecha UVI Nación", campo("obra_contrato_nacion_uvi_fecha"), formato="fecha"),
        col("obra_contrato_provincia_pesos", "Monto Provincia Pesos", campo("obra_contrato_provincia_pesos"), formato="decimal", sumable=not en_certificado),
        col("obra_contrato_provincia_uvi", "Monto Provincia UVI", campo("obra_contrato_provincia_uvi"), formato="decimal", sumable=not en_certificado),
        col("obra_contrato_provincia_uvi_fecha", "Fecha UVI Provincia", campo("obra_contrato_provincia_uvi_fecha"), formato="fecha"),
        col("obra_contrato_terceros_pesos", "Monto Terceros Pesos", campo("obra_contrato_terceros_pesos"), formato="decimal", sumable=not en_certificado),
        col("obra_contrato_terceros_uvi", "Monto Terceros UVI", campo("obra_contrato_terceros_uvi"), formato="decimal", sumable=not en_certificado),
        col("obra_contrato_terceros_uvi_fecha", "Fecha UVI Terceros", campo("obra_contrato_terceros_uvi_fecha"), formato="fecha"),
        col("obra_contrato_total_pesos", "Monto Contrato Pesos", campo("obra_contrato_total_pesos"), formato="decimal", sumable=not en_certificado),
        col("obra_contrato_total_uvi", "Monto Contrato UVI", campo("obra_contrato_total_uvi"), formato="decimal", sumable=not en_certificado),
        col("obra_principal", "Obra Madre", lambda o: ", ".join(x.obra_nombre for x in o.obra_principal.all()) or None, prefetch_related=("obra_principal",)),
        col("obra_georeferencia", "Georeferencia", lambda o: o.dd_to_dms() or None),
    ]


# --- Agregados de certificados por obra (solo reporte de Obras) ------------------- #

def _certificados_de_la_obra():
    return Certificado.objects.filter(certificado_obra=OuterRef("pk")).order_by().values("certificado_obra")


def _suma_certificados(campo):
    return Coalesce(
        Subquery(_certificados_de_la_obra().annotate(s=Sum(campo)).values("s")[:1]),
        Value(Decimal("0")),
        output_field=DecimalField(max_digits=16, decimal_places=2),
    )


def _ultimo_avance(campo):
    # Mismo criterio que Obra.ultimo_certificado_avance(): los Anticipos no llevan % de avance.
    ultimo = Certificado.objects.filter(
        Q(certificado_tipo__in=("PARCIAL", "HECHO_CONSUMADO", "ETAPA"))
        | Q(certificado_tipo="LEGACY", certificado_rubro_obra__gt=0),
        certificado_obra=OuterRef("pk"),
    ).order_by("-certificado_fecha", "-pk").values(campo)[:1]
    return Subquery(ultimo, output_field=DecimalField(max_digits=6, decimal_places=3))


def _anot_acum_pesos():
    return {"rep_acum_pesos": _suma_certificados("certificado_monto_cobrar")}


def _anot_acum_uvi():
    return {"rep_acum_uvi": _suma_certificados("certificado_monto_cobrar_uvi")}


def _columnas_agregados_obra():
    def col(clave, etiqueta, valor, anotaciones, **kwargs):
        return Columna(clave=clave, etiqueta=etiqueta, grupo=GRUPO_CALCULADOS, valor=valor, anotaciones=anotaciones, **kwargs)

    return [
        col("saldo_uvi", "Saldo UVI", lambda o: (o.obra_contrato_total_uvi or 0) - o.rep_acum_uvi,
            _anot_acum_uvi, formato="decimal", sumable=True),
        col("ultimo_mes_pct", "% Último Mes", lambda o: o.rep_ultimo_mes_pct,
            lambda: {"rep_ultimo_mes_pct": _ultimo_avance("certificado_mes_pct")}, formato="decimal", decimales=3),
        col("acum_pct", "% Acumulado", lambda o: o.rep_acum_pct,
            lambda: {"rep_acum_pct": _ultimo_avance("certificado_acum_pct")}, formato="decimal", decimales=3),
        col("acum_pesos", "Acumulado en Pesos", lambda o: o.rep_acum_pesos, _anot_acum_pesos, formato="decimal", sumable=True),
        col("acum_uvi", "Acumulado en UVI", lambda o: o.rep_acum_uvi, _anot_acum_uvi, formato="decimal", sumable=True),
        col("cantidad_certificados", "Cantidad de Certificados", lambda o: o.rep_cantidad_certificados,
            lambda: {"rep_cantidad_certificados": Coalesce(
                Subquery(_certificados_de_la_obra().annotate(c=Count("pk")).values("c")[:1]),
                Value(0), output_field=IntegerField(),
            )}, formato="decimal", decimales=0, sumable=True),
        col("fecha_ultimo_certificado", "Fecha del Último Certificado", lambda o: o.rep_fecha_ultimo_certificado,
            lambda: {"rep_fecha_ultimo_certificado": Subquery(
                _certificados_de_la_obra().annotate(f=Max("certificado_fecha")).values("f")[:1]
            )}, formato="fecha"),
    ]


# --- Columnas de Certificado ------------------------------------------------------ #

def _numero_certificado(c):
    return format_html(
        "Anticipo N°: {}<br>Obra N°: {}<br>Dev. Anticipo N°: {}",
        c.certificado_rubro_anticipo, c.certificado_rubro_obra, c.certificado_rubro_devanticipo,
    )


def _columnas_certificado():
    def col(clave, etiqueta, valor=None, grupo=GRUPO_CERTIFICADO, **kwargs):
        return Columna(clave=clave, etiqueta=etiqueta, grupo=grupo, valor=valor or (lambda o: getattr(o, clave)), **kwargs)

    def monto(clave, etiqueta):
        return col(clave, etiqueta, formato="decimal", sumable=True)

    def pct(clave, etiqueta):
        return col(clave, etiqueta, formato="decimal", decimales=3)

    def entero(clave, etiqueta):
        return col(clave, etiqueta, formato="decimal", decimales=0)

    return [
        col("certificado_id", "ID Certificado", lambda o: str(o.pk)),
        col("certificado_tipo", "Tipo de Certificado", _display("certificado_tipo")),
        col("certificado_contrato_origen", "Contrato de Origen",
            lambda o: o.certificado_contrato_origen and o.certificado_contrato_origen.contrato_descripcion,
            select_related=("certificado_contrato_origen",)),
        col("certificado_financiamiento", "Financiamiento", _display("certificado_financiamiento")),
        col("certificado_rubro_db", "Rubro", lambda o: o.certificado_rubro_db, select_related=("certificado_rubro_db",)),
        col("certificado_numero", "Certificado", _numero_certificado, grupo=GRUPO_CALCULADOS),
        entero("certificado_rubro_anticipo", "Anticipo N°"),
        entero("certificado_rubro_obra", "Obra N°"),
        entero("certificado_rubro_devanticipo", "Devolución de Anticipo N°"),
        col("certificado_expediente", "Expediente",
            enlace=lambda o: reverse("carga:update-certificado", args=[o.pk])),
        col("certificado_periodo", "Periodo (texto)"),
        col("certificado_periodo_mes", "Período", lambda o: o.certificado_fecha, grupo=GRUPO_CALCULADOS, formato="periodo"),
        col("certificado_fecha", "Fecha", formato="fecha"),
        col("certificado_fecha_carga", "Fecha de Carga", formato="fecha"),
        # % de Anticipo, de Etapa o del Mes según el tipo (ver Certificado.certificado_pct_principal).
        col("certificado_pct_principal", "Mes %", grupo=GRUPO_CALCULADOS, formato="decimal", decimales=3),
        pct("certificado_mes_pct", "% Mes (avance)"),
        pct("certificado_ante_pct", "Anterior %"),
        pct("certificado_acum_pct", "Acum %"),
        pct("certificado_anticipo_pct", "% de Anticipo"),
        pct("certificado_anticipo_anterior", "% de Anticipo Anterior"),
        pct("certificado_anticipo_acumulado", "% de Anticipo Acumulado"),
        pct("certificado_anticipo_saldo_pct", "% Saldo Pendiente de Anticipo"),
        col("certificado_contrato_tramo", "Tramo de Contrato",
            lambda o: o.certificado_contrato_tramo and f"Tramo {o.certificado_contrato_tramo.tramo_numero} ({o.certificado_contrato_tramo.tramo_pct_pago}%)",
            select_related=("certificado_contrato_tramo",)),
        pct("certificado_etapa_pct", "% de Etapa"),
        monto("certificado_monto_pesos", "Monto en Pesos"),
        monto("certificado_monto_uvi", "Monto en UVI"),
        col("certificado_devolucion_expte", "Expediente Devolución"),
        monto("certificado_devolucion_monto", "Monto Devolución en Pesos"),
        monto("certificado_devolucion_monto_uvi", "Monto Devolución en UVI"),
        monto("certificado_descuento_anticipo_pesos", "Descuento de Anticipo en Pesos"),
        monto("certificado_descuento_anticipo_uvi", "Descuento de Anticipo en UVI"),
        pct("certificado_descuento_anticipo_pct", "Descuento de Anticipo %"),
        col("certificado_fondoreparo_pct", "Fondo de Reparo %", formato="decimal", decimales=2),
        monto("certificado_monto_cobrar", "Monto a Cobrar($)"),
        monto("certificado_monto_cobrar_uvi", "Monto a Cobrar(UVI)"),
        col("certificado_foja", "Foja de Medición",
            lambda o: o.certificado_foja_id and f"Foja N° {o.certificado_foja.foja_numero}",
            select_related=("certificado_foja",)),
    ]


REPORTE_OBRAS = Reporte(
    columnas=_columnas_obra("", lambda o: o, en_certificado=False) + _columnas_agregados_obra(),
    defaults=[
        "obra_id", "obra_nombre", "obra_soluciones", "obra_localidad_m", "obra_empresa", "obra_programa",
        "obra_convenio", "obra_expediente", "obra_contrato_total_pesos", "obra_contrato_total_uvi",
        "saldo_uvi", "ultimo_mes_pct", "acum_pct", "acum_pesos", "acum_uvi",
    ],
    orden_inicial=("obra_nombre", "desc"),
)

REPORTE_CERTIFICADOS = Reporte(
    columnas=_columnas_obra("certificado_obra__", lambda o: o.certificado_obra, en_certificado=True) + _columnas_certificado(),
    defaults=[
        "obra_programa", "obra_convenio", "obra_empresa", "obra_nombre", "obra_localidad_m",
        "certificado_expediente", "certificado_numero", "certificado_periodo_mes", "certificado_pct_principal",
        "certificado_acum_pct", "certificado_monto_cobrar", "certificado_monto_cobrar_uvi",
    ],
    orden_inicial=("certificado_periodo_mes", "desc"),
)
