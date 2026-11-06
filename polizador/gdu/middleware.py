"""
Deja que QGIS cachee los metadatos de OGC API - Features.

Al abrir el proyecto, QGIS inicializa las capas de a una y cada capa pide, en serie, la
landing page, openapi.json, conformance, la colección, sus queryables y su schema. Las tres
primeras son las mismas para todas las capas; sin cabeceras de caché QGIS las pedía de
nuevo para cada una, y con ~0,3 s de ida y vuelta por pedido (Cloudflare) abrir el proyecto
tardaba minutos. Con Cache-Control, QGIS las resuelve desde su caché de red (la usa por
defecto) y, en las aperturas siguientes, también los metadatos de cada colección.

Solo metadatos y solo respuestas 200: los datos (items) no se cachean nunca. "private"
porque la respuesta depende del usuario autenticado. Un cambio de schema (un deploy) se nota
a lo sumo en DURACION.
"""
from django.utils.cache import patch_cache_control

DURACION = 60 * 60
NAMESPACE = "gdu-oapif"
VISTAS_METADATOS = {"root", "openapi-json", "conformance", "get_collection", "get_queryables", "get_schema"}


class CacheMetadatosOapifMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        match = request.resolver_match
        if (
            request.method == "GET"
            and response.status_code == 200
            and match is not None
            and match.namespace == NAMESPACE
            and match.url_name in VISTAS_METADATOS
            and not response.has_header("Cache-Control")
        ):
            patch_cache_control(response, private=True, max_age=DURACION)
        return response
