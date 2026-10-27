"""
Capas del visor y de la ficha imprimible, sobre los modelos de gdu. Reemplazan a las vistas
SQL visualizador.* del piloto (viviendas, barrios, expropiaciones, vivienda_dispersa, ...):
cada capa es un queryset y una función que arma los datos de un elemento para el panel de
selección del visor y para la ficha.

El slug de cada capa es el de las URLs gdu:detalle_capa y gdu:ficha, y el `capa` de
gdu/templates/gdu/mapa.html.
"""
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable

from django.db.models import CharField, Prefetch, Q, QuerySet, Value
from django.db.models.functions import Cast, Coalesce, Concat

from gdu.models import (
    Barrio, Catastrourbano, ParcelaExpropiada, PlanoMensura, PlanoMensuraIntervencion, Uf, ViviendaPunto,
)

# relaciones de una intervención que muestran el visor y la ficha
_DE_INTERVENCION = ("contratacion__actuacion__programa", "localidad", "adjudicacion")


def _intervencion_relacionada(qs, ruta):
    """select_related + prefetch de los planos de la intervención a la que llega `ruta`."""
    return qs.select_related(*(f"{ruta}__{r}" for r in _DE_INTERVENCION)).prefetch_related(
        Prefetch(f"{ruta}__planos", queryset=PlanoMensuraIntervencion.objects.select_related("plano")),
    )


def _datos_intervencion(intervencion):
    """Lo que las vistas heredadas sacaban de la intervención: obra, localidad, programa,
    adjudicación y planos (con el formato "depto-nro-año/tipo" que lee gdu:plano)."""
    adjudicacion = intervencion.adjudicacion
    return {
        "obra": intervencion.nombre,
        "localidad": intervencion.localidad.localidad_nombre,
        "programa": intervencion.contratacion.actuacion.programa.nombre,
        "adjudicacion": f"{adjudicacion.nro}/{adjudicacion.ano} - {adjudicacion.tipo}" if adjudicacion else None,
        "planos": ", ".join(f"{v.plano}/{v.tipo}" for v in intervencion.planos.all()),
    }


def obras_vinculadas(contratacion_ids):
    """{contratacion_id: [{"id", "nombre"}]} de las obras de carga vinculadas.

    El vínculo vive todavía en gdu_piloto.ObraContratacion: sus contratacion_id son las PK
    heredadas, que gdu.Contratacion conserva. Se resuelve qué hacer con él en la fase 6."""
    from gdu_piloto.models import ObraContratacion

    resultado = defaultdict(list)
    for contratacion_id, obra_id, nombre in ObraContratacion.objects.filter(
        contratacion_id__in=set(contratacion_ids),
    ).values_list("contratacion_id", "obra_id", "obra__obra_nombre"):
        resultado[contratacion_id].append({"id": obra_id, "nombre": nombre})
    return resultado


@dataclass
class Capa:
    titulo: str  # de un elemento, para la ficha
    nombre: str  # de la capa, en el visor
    permiso: str
    queryset: Callable[[], QuerySet]
    # datos de un elemento para el panel y la ficha: (etiqueta de la ficha, clave, función)
    campos: list
    # el elemento -> su intervención, para las obras vinculadas (None si la capa no tiene)
    intervencion: Callable | None = None
    # parámetro de la búsqueda avanzada -> lookup
    filtros: dict = field(default_factory=dict)
    # suma al queryset lo que leen `campos` (select_related/prefetch); el GeoJSON del visor no lo usa
    relacionar: Callable[[QuerySet], QuerySet] = lambda qs: qs

    def detalle_queryset(self):
        return self.relacionar(self.queryset()).defer("geom")

    def datos(self, obj, obras=None):
        """{clave: valor} de un elemento; `obras` es el resultado de obras_vinculadas()."""
        datos = {"id": obj.pk}
        for _etiqueta, clave, valor in self.campos:
            datos[clave] = valor(obj)
        if self.intervencion is not None:
            intervencion = self.intervencion(obj)
            datos["obras"] = (obras or {}).get(intervencion.contratacion_id, [])
        return datos


def _nomenclatura(obj):
    return obj.nomenclatura or "-".join(
        getattr(obj, parte) or "" for parte in ("dpto", "circ", "secc", "ch", "qta", "fracc", "mz", "parc")
    )


def nro_adjudicatario(uf):
    """El del Sistema 3450, o el heredado que el ETL no pudo clasificar. El 0 es un número
    válido del 3450 ("crédito desadjudicado"), no un vacío."""
    return uf.adjudicatario_id if uf.adjudicatario_id is not None else uf.nro_adjudicatario_legacy


_INTERVENCION_UF = "parcela__intervencion"


def _ufs_relacionadas(qs):
    return _intervencion_relacionada(qs.select_related("parcela"), _INTERVENCION_UF)


def _uf_intervencion(uf):
    return uf.parcela.intervencion


CAMPOS_VIVIENDA = [
    # la vista heredada mostraba como "uf" el polígono (p. ej. "00-01")
    ("UF", "uf", lambda u: u.poligono or u.uf),
    ("Obra", "obra", lambda u: _datos_intervencion(_uf_intervencion(u))["obra"]),
    ("Localidad", "localidad", lambda u: _datos_intervencion(_uf_intervencion(u))["localidad"]),
    ("Adjudicación", "adjudicacion", lambda u: _datos_intervencion(_uf_intervencion(u))["adjudicacion"]),
    ("Nº adjudicatario", "nro_adjudicatario", lambda u: nro_adjudicatario(u)),
    ("DNI", "dni", lambda u: u.dni),
    ("Estado dominial", "estado_dominial", lambda u: u.get_estado_dominial_display()),
    ("Planos", "planos", lambda u: _datos_intervencion(_uf_intervencion(u))["planos"]),
]


def _filtros_proyecto(ruta):
    return {
        "programa": f"{ruta}__contratacion__actuacion__programa__nombre",
        "actuacion": f"{ruta}__contratacion__actuacion__nombre",
        "grupo": f"{ruta}__grupo",
        "plan": f"{ruta}__plan",
    }


def _expropiaciones():
    # "ley" con el formato de la vista heredada (nro + letra / año), que usa la búsqueda avanzada
    return ParcelaExpropiada.objects.annotate(ley=Concat(
        Cast("expropiacion__nro_ley", CharField()), "expropiacion__letra_ley", Value("/"),
        Coalesce(Cast("expropiacion__ano_ley", CharField()), Value("0")), output_field=CharField(),
    ))


def _relacionar_intervencion(qs):
    return _intervencion_relacionada(qs, "intervencion")


CAPAS = {
    "viviendas": Capa(
        "Vivienda", "Viviendas", "gdu.ver_viviendas", Uf.objects.all, CAMPOS_VIVIENDA,
        intervencion=_uf_intervencion, filtros=_filtros_proyecto(_INTERVENCION_UF), relacionar=_ufs_relacionadas,
    ),
    "barrios": Capa(
        "Barrio", "Barrios", "gdu.ver_barrios", Barrio.objects.all,
        [
            ("Barrio", "barrio", lambda b: b.nombre),
            ("Localidad", "localidad", lambda b: _datos_intervencion(b.intervencion)["localidad"]),
            ("Programa", "programa", lambda b: _datos_intervencion(b.intervencion)["programa"]),
        ],
        intervencion=lambda b: b.intervencion,
        filtros={k: v for k, v in _filtros_proyecto("intervencion").items() if k in ("programa", "actuacion")},
        relacionar=_relacionar_intervencion,
    ),
    "expropiaciones": Capa(
        "Expropiación", "Expropiaciones", "gdu.ver_expropiaciones", _expropiaciones,
        [
            ("Ley", "ley", lambda p: p.ley),
            ("Localidad", "localidad", lambda p: p.expropiacion.localidad.localidad_nombre),
            ("Nomenclatura", "nomenclatura", _nomenclatura),
            ("Objeto", "objeto", lambda p: p.objeto.nombre),
            # la vista heredada mostraba como "propietario expropiado" el propietario actual
            ("Propietario expropiado", "propietario_expropiado", lambda p: p.propietario_expropiado),
            ("Estado", "estado", lambda p: p.estado_gestion.nombre),
        ],
        filtros={"ley": "ley", "estado_gestion": "expropiacion__gestion"},
        relacionar=lambda qs: qs.select_related("expropiacion__localidad", "objeto", "estado_gestion"),
    ),
    "viviendas-dispersas": Capa(
        "Vivienda dispersa", "Viviendas Dispersas", "gdu.ver_viviendas_dispersas", ViviendaPunto.objects.all,
        [
            ("Obra", "obra", lambda v: _datos_intervencion(v.intervencion)["obra"]),
            ("Localidad", "localidad", lambda v: _datos_intervencion(v.intervencion)["localidad"]),
            ("Adjudicación", "adjudicacion", lambda v: _datos_intervencion(v.intervencion)["adjudicacion"]),
            ("Planos", "planos", lambda v: _datos_intervencion(v.intervencion)["planos"]),
        ],
        intervencion=lambda v: v.intervencion, filtros=_filtros_proyecto("intervencion"),
        relacionar=_relacionar_intervencion,
    ),
    "planos-mensura": Capa(
        "Plano de mensura", "Planos de Mensura", "gdu.ver_plano_mensura", PlanoMensura.objects.all,
        [
            ("Plano", "plano", lambda p: p.pm_antecedente or str(p)),
            ("En GDU", "en_gdu", lambda p: p.en_gdu),
            ("Sup. parcelas", "sup_parcelas", lambda p: p.sup_parcelas),
            ("Sup. calles", "sup_calles", lambda p: p.sup_calles),
            ("Sup. reserva", "sup_reserva", lambda p: p.sup_reserva),
        ],
    ),
    "catastro-urbano": Capa(
        "Catastro urbano", "Catastro Urbano", "gdu.ver_catastro_urbano", Catastrourbano.objects.all,
        [
            ("Nomenclatura", "nomenclatura", lambda c: c.id_nomencl),
            ("Plano aprobado", "plano_aprobado", lambda c: c.plano_apro),
            ("Matrícula", "matricula", lambda c: c.matric),
            ("Municipio", "municipio", lambda c: c.municipio),
            ("Año", "anio", lambda c: c.anio),
        ],
        filtros={"municipio": "municipio"},
    ),
    "para-escriturar": Capa(
        "Vivienda para escriturar", "Para Escriturar", "gdu.ver_escriturar",
        lambda: Uf.objects.filter(Q(adjudicatario__escritura=False)), CAMPOS_VIVIENDA,
        intervencion=_uf_intervencion, filtros=_filtros_proyecto(_INTERVENCION_UF), relacionar=_ufs_relacionadas,
    ),
}
PERMISOS_CAPAS = [capa.permiso for capa in CAPAS.values()]


def filtros_de(request, capa):
    """kwargs de filter() con los criterios de la búsqueda avanzada presentes en la query string."""
    filtros = {}
    for parametro, lookup in capa.filtros.items():
        valor = (request.GET.get(parametro) or "").strip()
        if not valor:
            continue
        if parametro == "plan":
            try:
                valor = int(valor)
            except ValueError:
                continue
        filtros[lookup] = valor
    return filtros
