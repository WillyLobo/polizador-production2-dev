"""
Teselas vectoriales (Mapbox Vector Tiles) de las capas grandes de solo lectura, para QGIS.

Por OAPIF, QGIS baja los objetos en páginas: ver catastro urbano entero (430.000 parcelas,
~270 MB de GeoJSON) tardaba ~35 s de servidor y la tabla de atributos más todavía. Con
teselas, PostGIS arma solo lo que se ve (ST_AsMVT): una tesela de zoom 14 en el centro de
Resistencia (~7.400 parcelas) sale en ~50 ms y ~450 KB. El sistema heredado resolvía lo
mismo dibujando en el servidor (QGIS Server, WMS).

Autenticación: la misma que OAPIF (Basic cacheada, que es lo que manda QGIS con el authcfg
gduoapf, o la sesión de Django). Sin credenciales responde 401 con WWW-Authenticate, no una
redirección al login: QGIS no la seguiría.
"""
from django.db import connection
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET

from gdu.models import Catastrourbano
from gdu.models.base import SRID_GDU
from gdu.oapif import BasicAuthCacheada

CONTENT_TYPE = "application/vnd.mapbox-vector-tile"
# QGIS guarda las teselas en su caché de red; catastro solo cambia al reimportarlo
DURACION_CACHE = 60 * 60 * 24

# capa -> modelo, campos que viajan en la tesela (los que muestra "Identificar") y zooms.
# Debajo de zmin una tesela tiene demasiadas parcelas (zoom 13 en Resistencia: ~30.000,
# ~1,8 MB); arriba de zmax QGIS reusa las de zmax (a zoom 17 la grilla es de ~4 cm).
CAPAS = {
    "catastro_urbano": {
        "modelo": Catastrourbano,
        "campos": (
            "id_nomencl", "plano_apro", "dpto", "circ", "secc", "ch", "qta", "fracc", "mz", "parc",
            "matric", "tomo", "folio", "finca", "anio", "municipio",
        ),
        "zmin": 14,
        "zmax": 17,
    },
}

SQL = """
WITH limites AS (SELECT ST_TileEnvelope(%(z)s, %(x)s, %(y)s) AS env),
objetos AS (
    SELECT t.id, {campos}, ST_AsMVTGeom(ST_Transform(t.geom, 3857), limites.env, 4096, 64, true) AS geom
    FROM {tabla} t, limites
    WHERE t.geom && ST_Transform(limites.env, {srid})
)
SELECT ST_AsMVT(objetos, %(capa)s, 4096, 'geom', 'id') FROM objetos WHERE geom IS NOT NULL
"""


def generar_tesela(capa, z, x, y):
    """Los bytes de la tesela (b"" si no hay objetos)."""
    config = CAPAS[capa]
    modelo = config["modelo"]
    qn = connection.ops.quote_name
    sql = SQL.format(
        campos=", ".join(f"t.{qn(modelo._meta.get_field(c).column)}" for c in config["campos"]),
        tabla=qn(modelo._meta.db_table),
        srid=SRID_GDU,
    )
    with connection.cursor() as cursor:
        cursor.execute(sql, {"z": z, "x": x, "y": y, "capa": capa})
        fila = cursor.fetchone()
    return bytes(fila[0]) if fila and fila[0] is not None else b""


def no_autorizado():
    respuesta = HttpResponse("Se requieren credenciales", status=401, content_type="text/plain; charset=utf-8")
    respuesta["WWW-Authenticate"] = 'Basic realm="GDU"'
    return respuesta


@require_GET
def tesela(request, capa, z, x, y):
    config = CAPAS.get(capa)
    if config is None:
        raise Http404
    BasicAuthCacheada()(request)
    if not request.user.is_authenticated:
        return no_autorizado()
    modelo = config["modelo"]
    if not request.user.has_perm(f"{modelo._meta.app_label}.view_{modelo._meta.model_name}"):
        return HttpResponse(status=403)
    if not config["zmin"] <= z <= config["zmax"] or not (0 <= x < 2 ** z and 0 <= y < 2 ** z):
        raise Http404

    contenido = generar_tesela(capa, z, x, y)
    # 204: tesela vacía, QGIS no dibuja nada y no lo toma como error
    respuesta = HttpResponse(contenido, status=200 if contenido else 204, content_type=CONTENT_TYPE)
    respuesta["Cache-Control"] = f"private, max-age={DURACION_CACHE}"
    return respuesta
