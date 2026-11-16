"""
Páginas GeoJSON de OAPIF armadas por PostGIS.

django-oapif arma cada objeto en Python: lee la geometría como WKB, la pasa a un diccionario
y valida los atributos de cada fila con el esquema de ninja (campo por campo). Para una
página de 50.000 parcelas de catastro eso tardaba ~3,5 s de servidor, de los que la consulta
era ~0,3 s. Acá cada objeto lo arma PostGIS con json_build_object y Python solo une los
textos.

La página la sigue eligiendo la consulta de django-oapif (con su orden, su OFFSET/LIMIT, su
filtro de zona y CQL2 y sus campos anotados), y el JSON se arma en una consulta de afuera:
dentro de la misma, Postgres calculaba el JSON también de las filas que saltea el OFFSET (en
la última página de catastro, de 430.000 filas para devolver 30.000).

La cabecera de la página (bbox, links, numberReturned, numberMatched) la sigue serializando
pydantic como en django-oapif, así que solo cambia cómo se escribe cada objeto; los tests
comparan el resultado con el de django-oapif colección por colección.
"""
from django.core.exceptions import FieldDoesNotExist
from django.db import connections
from django.db.models import (
    DateTimeField, DecimalField, DurationField, F, FloatField, GeneratedField, Subquery, TimeField,
)
from django_oapif.geojson import FeatureCollection

# dígitos decimales de las coordenadas: con 15, ST_AsGeoJSON escribe los mismos números que
# django-oapif (que pasa los double de PostGIS a JSON tal cual)
DECIMALES = 15
FEATURES_VACIO = '"features":[]'

# un timestamptz como lo escribe django-oapif (DjangoJSONEncoder): en UTC, con "Z", y con la
# fracción de segundo truncada a milisegundos si la tiene ("2023-06-14T00:59:48.900Z")
SQL_FECHA_HORA = (
    "CASE WHEN {c} IS NULL THEN NULL"
    " WHEN mod(date_part('microseconds', {c})::bigint, 1000000) = 0"
    " THEN to_char({c} AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"')"
    " ELSE to_char({c} AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS.MS\"Z\"') END"
)
SQL_HORA = (
    "CASE WHEN {c} IS NULL THEN NULL"
    " WHEN mod(date_part('microseconds', {c})::bigint, 1000000) = 0"
    " THEN to_char({c}, 'HH24:MI:SS') ELSE to_char({c}, 'HH24:MI:SS.MS') END"
)
# str(Decimal), con todos sus decimales ("100.00000"), igual que numeric::text
SQL_DECIMAL = "{c}::text"


class SinFormatoEquivalente(Exception):
    """Un campo que PostGIS no escribe igual que django-oapif: la colección sigue por django-oapif."""


def formato_sql(modelo, nombre):
    """La plantilla SQL ({c}: la columna) del valor de la propiedad `nombre`, con el formato de django-oapif."""
    try:
        campo = modelo._meta.get_field(nombre)
    except FieldDoesNotExist:
        return "{c}"  # una anotación de la colección (p. ej. parcela_nomenclatura)
    if isinstance(campo, GeneratedField):
        campo = campo.output_field
    if isinstance(campo, DateTimeField):
        return SQL_FECHA_HORA
    if isinstance(campo, TimeField):
        return SQL_HORA
    if isinstance(campo, DecimalField):
        return SQL_DECIMAL
    if isinstance(campo, (FloatField, DurationField)):
        # los float que Python escribe "1.0" Postgres los escribe "1"; las duraciones, en ISO
        raise SinFormatoEquivalente(nombre)
    return "{c}"


class PaginaGeoJSON:
    """
    Una página ya serializada. get_items de django-oapif solo le pide model_dump_json() (para la
    respuesta, o para la página HTML) y links; no es un JsonFgDocument, así que se sirve como
    GeoJSON.
    """

    def __init__(self, texto, links):
        self.texto = texto
        self.links = links

    def model_dump_json(self, **_):
        return self.texto


def sin_offset(qs):
    """
    La misma página sin OFFSET, si está ordenada solo por la PK (catastro, parcelas, UF: las
    grandes): "pk >= el de la fila N", con N buscado en el índice de la PK. Con OFFSET, Postgres
    lee y descarta las N filas anteriores enteras (geometría incluida); en la última página de
    catastro eso eran 400.000. Con otro orden la página queda como está.
    """
    consulta = qs.query
    if not consulta.low_mark or tuple(consulta.order_by) != ("pk",):
        return qs
    base = qs._chain()
    base.query.clear_limits()
    desde = base.values_list("pk", flat=True)[consulta.low_mark:consulta.low_mark + 1]
    # fuera de rango, la subconsulta da NULL y la página sale vacía, como con OFFSET
    pagina = base.filter(pk__gte=Subquery(desde))
    if consulta.high_mark is not None:
        pagina = pagina[:consulta.high_mark - consulta.low_mark]
    return pagina


def pagina_geojson(coleccion, request, qs, *, number_matched, links, crs):
    """La página de `qs` (como la arma query() de django-oapif, en `crs`) en GeoJSON."""
    qs = sin_offset(qs)
    FeatureSchema = coleccion.get_feature_output_schema(request)
    propiedades = list(FeatureSchema.model_fields["properties"].annotation.model_fields)
    formatos = [formato_sql(coleccion.model, nombre) for nombre in propiedades]

    # adentro, la consulta de django-oapif con columnas de nombre propio (una propiedad "id" no
    # choca con la PK); afuera, el JSON de cada fila de la página
    columnas = {"_gdu_pk": F("pk"), **{f"_gdu_p{i}": F(nombre) for i, nombre in enumerate(propiedades)}}
    if coleccion.geometry_field:
        # la misma geometría que lee django-oapif (en el CRS pedido)
        columnas["_gdu_geom"] = coleccion._geometry_in(crs)
    interna = qs.annotate(**columnas).values(*columnas)
    sql_interna, params = interna.query.sql_with_params()

    qn = connections[interna.db].ops.quote_name
    pares = ", ".join(
        "%s, " + formato.format(c="s." + qn(f"_gdu_p{i}")) for i, formato in enumerate(formatos)
    )
    if coleccion.geometry_field:
        # Django selecciona las geometrías como EWKB (bytea): se lee una vez por fila
        geometria = f"ST_AsGeoJSON(g.geom, {DECIMALES})::json"
        limites = "ST_XMin(g.geom), ST_YMin(g.geom), ST_XMax(g.geom), ST_YMax(g.geom)"
        lateral = " CROSS JOIN LATERAL (SELECT ST_GeomFromEWKB(s._gdu_geom) AS geom) g"
    else:
        geometria = "NULL"
        limites = "NULL, NULL, NULL, NULL"
        lateral = ""
    # sin ORDER BY afuera: Postgres entrega las filas de la subconsulta en su orden (la proyección
    # no las reordena); el test de equivalencia lo verifica
    sql = (
        f"SELECT json_build_object('type', 'Feature', 'id', s._gdu_pk::text, 'geometry', {geometria},"
        f" 'properties', json_build_object({pares}))::text, {limites}"
        f" FROM ({sql_interna}) s{lateral}"
    )

    with connections[interna.db].cursor() as cursor:
        cursor.execute(sql, [*propiedades, *params])
        filas = cursor.fetchall()

    textos = [fila[0] for fila in filas]
    cajas = [fila[1:] for fila in filas if fila[1] is not None]
    bbox = None
    if cajas:
        xmins, ymins, xmaxs, ymaxs = zip(*cajas)
        bbox = (min(xmins), min(ymins), max(xmaxs), max(ymaxs))

    cabecera = FeatureCollection[FeatureSchema].model_construct(
        type="FeatureCollection",
        features=[],
        bbox=bbox,
        links=links or [],
        numberReturned=len(textos),
        numberMatched=len(textos) if number_matched is None else number_matched,
    ).model_dump_json()
    if cabecera.count(FEATURES_VACIO) != 1:
        raise AssertionError(f"no se encuentra {FEATURES_VACIO} en la cabecera de la página")
    texto = cabecera.replace(FEATURES_VACIO, '"features":[' + ",".join(textos) + "]")
    return PaginaGeoJSON(texto, links or [])
