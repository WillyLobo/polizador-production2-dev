"""
Capas de gdu publicadas como OGC API - Features (django-oapif), para editarlas desde
QGIS sin GeoServer: las escrituras pasan por el ORM, así que valen los permisos de
Django, la validación de los modelos, updated_by y simple_history.

Autenticación: HTTP Basic contra los AUTHENTICATION_BACKENDS (LDAP incluido), que es
lo que manda QGIS con un authcfg; la sesión de Django queda para navegar la API.
Permisos: los de modelo (view/add/change/delete) de cada colección.

CRS: las geometrías se publican solo en CRS84 (lon, lat) y QGIS las reproyecta. django-oapif
no invierte ejes, así que ofrecer EPSG:22175 (cuyo orden EPSG es norte, este) hacía que
QGIS dibujara todo cruzado y guardara las geometrías corridas sin dar error.
"""
import hashlib
import hmac
import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.gis.geos import GEOSGeometry
from django.core.cache import cache
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError as DjangoValidationError
from django.db.models import AutoField, BigAutoField, CharField, ProtectedError, Q, RestrictedError, TextField
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_oapif import OAPIF, OapifCollection
from django_oapif.auth import BasicAuth, DjangoAuth
from django_oapif.crs import CRS84
from ninja.errors import AuthorizationError, HttpError, ValidationError
from ninja.renderers import JSONRenderer

from carga.models import Localidad
from gdu.models import (
    Actuacion, AdjudicacionBeneficiario, Adjudicatario3450, Barrio, Calle, Catastrourbano, Contratacion,
    DestinoParcela, Ejecutor, EstadoGestionExpropiacion, Expropiacion, Inspector, Intervencion,
    IntervencionEjecutor, IntervencionInspector, Manzana, ObjetoExpropiacion, Parcela, ParcelaExpropiada,
    PlanoMensura, PlanoMensuraIntervencion, PlanoMensuraTierra, PreAdjudicatarioDispersa, Programa,
    ResolucionCostos, Tierra, TierraConsulta, TierraDestino, TipoContratacion, TipoDocProbatoria, TipoEjecutor,
    TipoIntervencion, Uf, ViviendaPunto, ZonaParcelas,
)
from gdu.models.base import SRID_GDU


class JSONSinEscapar(JSONRenderer):
    # QGIS muestra literal el cuerpo de los errores: con el escape por defecto se veía "m\u00e1ximo"
    json_dumps_params = {"ensure_ascii": False}


class BasicAuthCacheada(BasicAuth):
    """
    Basic Auth no abre sesión: QGIS manda usuario y clave en cada pedido, y verificarlos
    (hash PBKDF2 de la clave, o un bind contra LDAP) costaba ~160 ms por pedido; abrir el
    proyecto, con ~7 pedidos en serie por capa, tardaba dos minutos. Un par usuario/clave ya
    verificado se recuerda unos minutos. La clave de la caché es un HMAC del par: la clave
    del usuario no se guarda. Un cambio de clave o una baja se notan a lo sumo en DURACION.
    """
    DURACION = 10 * 60

    def authenticate(self, request, username, password):
        clave = "gdu-oapif-auth:" + hmac.new(
            settings.SECRET_KEY.encode(), f"{username}\0{password}".encode(), hashlib.sha256,
        ).hexdigest()
        if (usuario_id := cache.get(clave)) is not None:
            usuario = get_user_model().objects.filter(pk=usuario_id, is_active=True).first()
            if usuario is not None:
                request.user = usuario
                return usuario
        if usuario := authenticate(request, username=username, password=password):
            cache.set(clave, usuario.pk, self.DURACION)
            request.user = usuario
        return request.user


api = OAPIF(
    title="GDU",
    description="Capas de la Gerencia de Desarrollo Urbano (IPDUV)",
    urls_namespace="gdu-oapif",
    auth=[BasicAuthCacheada(), DjangoAuth()],
    renderer=JSONSinEscapar(),
)

MENSAJES_VALIDACION = {
    "string_too_long": lambda e: f"admite como máximo {e.get('ctx', {}).get('max_length')} caracteres",
    "missing": lambda e: "es obligatorio",
    "int_parsing": lambda e: "tiene que ser un número entero",
    "float_parsing": lambda e: "tiene que ser un número",
    "bool_parsing": lambda e: "tiene que ser verdadero o falso",
    "extra_forbidden": lambda e: "no es un campo de la capa",
    "model_attributes_type": lambda e: "falta o no es válida",
    "model_type": lambda e: "falta o no es válida",
}


@api.api.exception_handler(ValidationError)
def _validacion(request, exc):
    """422 con un mensaje legible (es lo que QGIS le muestra al usuario), sin repetir los
    valores enviados ni los enlaces de pydantic."""
    partes = []
    for error in exc.errors:
        loc = [str(x) for x in error.get("loc", []) if x not in ("body", "feature", "properties")]
        traducir = MENSAJES_VALIDACION.get(error.get("type"))
        mensaje = traducir(error) if traducir else error.get("msg", "valor inválido")
        if mensaje == "Foreign key not found":
            mensaje = "no existe el registro referenciado"
        partes.append(f"{'.'.join(loc)}: {mensaje}" if loc else mensaje)
    return api.api.create_response(request, {"detail": "; ".join(partes)}, status=422)


class ColeccionGdu(OapifCollection):
    """Base de las colecciones editables de gdu."""

    def resolve_item_id(self, request, item_id):
        # un id no numérico en una PK entera daba 500 en django-oapif (ValueError del ORM)
        if isinstance(self.opts.pk, (AutoField, BigAutoField)) and not item_id.isdigit():
            raise Http404
        return item_id

    def storage_crs(self):
        return CRS84 if self.geometry_field else None

    def supported_crs(self):
        return (CRS84,) if self.geometry_field else ()

    def get_readonly_fields(self, request, obj=None):
        # además de los que django-oapif ya trata como de solo lectura (GeneratedField,
        # archivos): la PK, la auditoría y lo que el modelo marca editable=False
        no_editables = {f.name for f in self.model._meta.concrete_fields if not f.editable or f.primary_key}
        return tuple(set(super().get_readonly_fields(request, obj)) | no_editables)

    def get_json_schema(self, request):
        # lo que no se escribe no es obligatorio al escribir (QGIS lo exigiría en el formulario)
        schema = super().get_json_schema(request)
        solo_lectura = set(self.get_readonly_fields(request))
        if "required" in schema:
            schema["required"] = [campo for campo in schema["required"] if campo not in solo_lectura]
        # django-oapif publica solo los valores de las choices (Part 5 no tiene palabra para
        # las etiquetas); el armado del proyecto QGIS las usa para los combos
        for nombre, propiedades in schema["properties"].items():
            if "enum" in propiedades:
                campo = self.opts.get_field(nombre)
                propiedades["x-gdu-etiquetas"] = {str(valor): str(etiqueta) for valor, etiqueta in campo.flatchoices}
        return schema

    def validate_feature_or_raise(self, request, schema, feature):
        # sin permiso de alta, 403 antes que cualquier error de validación del cuerpo
        if request.method == "POST" and not self.has_add_permission(request):
            raise AuthorizationError()
        # QGIS manda en el alta (y en el PUT) todos los campos de la capa, también los de
        # solo lectura y el id en null: se ignoran en vez de rechazar el pedido
        if isinstance(feature.properties, dict):
            solo_lectura = set(self.get_readonly_fields(request))
            feature.properties = {k: v for k, v in feature.properties.items() if k not in solo_lectura}
        return super().validate_feature_or_raise(request, schema, feature)

    def save_model(self, request, obj, change):
        if hasattr(obj, "updated_by_id"):
            obj.updated_by = request.user
        # un texto vacío llega como null: en Django los CharField no nulos se guardan como
        # "" (full_clean no lo valida por ser blank=True y el INSERT fallaba con 500)
        for campo in self.model._meta.concrete_fields:
            if isinstance(campo, (CharField, TextField)) and not campo.null and getattr(obj, campo.attname) is None:
                setattr(obj, campo.attname, "")
        try:
            obj.full_clean()
        except DjangoValidationError as e:
            # 422 con el detalle por campo, en vez de un 500
            # los errores de unicidad o de clean() vienen sin campo (NON_FIELD_ERRORS)
            raise ValidationError([
                {
                    "loc": ["body", "feature", "properties", *([] if campo == NON_FIELD_ERRORS else [campo])],
                    "msg": " ".join(mensajes),
                    "type": "value_error",
                }
                for campo, mensajes in e.message_dict.items()
            ])
        obj.save()

    def delete_model(self, request, obj):
        # 409 en vez de un 500 si otras filas lo referencian (on_delete=PROTECT); ninja
        # responde {"detail": ...}, que QGIS muestra como respuesta del servidor
        try:
            return obj.delete()
        except ProtectedError as e:
            referencias = e.protected_objects
        except RestrictedError as e:
            referencias = e.restricted_objects
        modelos = sorted({str(o._meta.verbose_name_plural) for o in referencias})
        raise HttpError(409, f"No se puede borrar: lo referencian {', '.join(modelos)}")


class ColeccionSoloLectura(ColeccionGdu):
    """Capas de referencia: se leen (con view_<modelo>) pero no se editan desde QGIS."""

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def coleccion(modelo, id, title, base=ColeccionGdu, **atributos):
    """Registra una colección; la mayoría no necesita más que su id y su título."""
    clase = type(f"Coleccion_{id}", (base,), {"id": id, "title": title, **atributos})
    api.register(modelo)(clase)
    return clase


# Proyecto: programa -> actuación -> contratación -> intervención, y sus tablas de tipos
coleccion(Programa, "programas", "Programas")
coleccion(Actuacion, "actuaciones", "Actuaciones")
coleccion(TipoContratacion, "tipos_contratacion", "Tipos de contratación")
coleccion(Contratacion, "contrataciones", "Contrataciones")
coleccion(TipoIntervencion, "tipos_intervencion", "Tipos de intervención")
coleccion(Intervencion, "intervenciones", "Intervenciones")
coleccion(AdjudicacionBeneficiario, "adjudicaciones_beneficiario", "Adjudicaciones a beneficiarios")
coleccion(ResolucionCostos, "resoluciones_costos", "Resoluciones de costos")
coleccion(TipoEjecutor, "tipos_ejecutor", "Tipos de ejecutor")
coleccion(Ejecutor, "ejecutores", "Ejecutores")
coleccion(Inspector, "inspectores", "Inspectores")
coleccion(IntervencionEjecutor, "intervenciones_ejecutores", "Ejecutores por intervención")
coleccion(IntervencionInspector, "intervenciones_inspectores", "Inspectores por intervención")

# Territorio
coleccion(Barrio, "barrios", "Barrios")
coleccion(Manzana, "manzanas", "Manzanas")
coleccion(Calle, "calles", "Calles")
coleccion(DestinoParcela, "destinos_parcela", "Destinos de parcela")
# la completa primero: al validar una FK a parcela se busca en las colecciones en este orden
coleccion(Parcela, "parcelas", "Parcelas (completa)")


class ParcelasDeZona(ColeccionGdu):
    """Parcelas que tocan una zona fija (un departamento o un cuarto de Resistencia).
    El proyecto QGIS viejo lo hacía con un filtro SQL en cada capa; acá lo define el
    servidor, porque QGIS pierde la autenticación de las capas OAPIF filtradas."""
    zona = None

    def get_queryset(self, request):
        return super().get_queryset(request).filter(geom__intersects=self.zona)


with open(Path(__file__).parent / "data" / "zonas_parcelas.json", encoding="utf-8") as archivo:
    # polígonos copiados de los filtros del proyecto QGIS heredado, en EPSG:22175
    ZONAS_PARCELAS = json.load(archivo)
for _zona in ZONAS_PARCELAS:
    coleccion(Parcela, _zona["id"], _zona["titulo"], ParcelasDeZona, zona=GEOSGeometry(_zona["wkt"], srid=SRID_GDU))


class Ufs(ColeccionGdu):
    def get_readonly_fields(self, request, obj=None):
        # permisos por campo heredados del visualizador
        solo_lectura = set(super().get_readonly_fields(request, obj))
        if not request.user.has_perm("gdu.editar_dominio"):
            solo_lectura.add("estado_dominial")
        if not request.user.has_perm("gdu.editar_nro_adjudicatario"):
            solo_lectura |= {"dni", "adjudicatario"}
        return tuple(solo_lectura)


coleccion(Uf, "ufs", "Unidades funcionales", Ufs)
coleccion(ViviendaPunto, "viviendas_punto", "Viviendas dispersas")
coleccion(PreAdjudicatarioDispersa, "pre_adjudicatarios_dispersa", "Pre-adjudicatarios de vivienda dispersa")
coleccion(ZonaParcelas, "zonas_parcelas", "Zonificación de Resistencia")


class ViviendasFiltradas(ColeccionSoloLectura):
    """Reemplazan a las vistas vistas.viviendas_* del proyecto heredado: son UF filtradas;
    los datos del Sistema 3450 se suman en QGIS uniendo con adjudicatarios_3450."""
    filtro = Q()

    def get_queryset(self, request):
        return super().get_queryset(request).filter(self.filtro)


_sin_plan_o_grupo = Q(parcela__intervencion__plan__isnull=True) | Q(parcela__intervencion__grupo="")
coleccion(Uf, "viviendas_sin_plan_grupo", "Viviendas sin plan o grupo", ViviendasFiltradas, filtro=_sin_plan_o_grupo)
coleccion(
    Uf, "viviendas_con_plan_grupo_sin_adjudicatario", "Viviendas con plan y grupo sin adjudicatario",
    ViviendasFiltradas,
    filtro=~_sin_plan_o_grupo & Q(dni__isnull=True, adjudicatario__isnull=True, nro_adjudicatario_legacy__isnull=True),
)
coleccion(
    Uf, "viviendas_para_escriturar", "Viviendas para escriturar", ViviendasFiltradas,
    filtro=Q(adjudicatario__escritura=False),
)

# Planos y tierras
coleccion(PlanoMensura, "planos_mensura", "Planos de mensura")
coleccion(PlanoMensuraIntervencion, "planos_mensura_intervencion", "Planos de mensura por intervención")
coleccion(TierraDestino, "tierra_destinos", "Destinos de tierra")
coleccion(TipoDocProbatoria, "tipos_doc_probatoria", "Tipos de documentación probatoria")
coleccion(Tierra, "tierras", "Tierras")
coleccion(TierraConsulta, "tierras_consultas", "Consultas sobre tierras")
coleccion(PlanoMensuraTierra, "planos_mensura_tierra", "Planos de mensura por tierra")

# Expropiaciones
coleccion(EstadoGestionExpropiacion, "estados_gestion_expropiacion", "Estados de gestión de expropiación")
coleccion(ObjetoExpropiacion, "objetos_expropiacion", "Objetos de expropiación")
coleccion(Expropiacion, "expropiaciones", "Expropiaciones")
coleccion(ParcelaExpropiada, "parcelas_expropiadas", "Parcelas expropiadas")

# Referencia, sin edición desde QGIS
coleccion(Catastrourbano, "catastro_urbano", "Catastro urbano", ColeccionSoloLectura)
# las mantiene importar_3450; las UF las referencian por FK
coleccion(Adjudicatario3450, "adjudicatarios_3450", "Adjudicatarios (Sistema 3450)", ColeccionSoloLectura)
# compartidas con carga, que es quien las edita
coleccion(
    Localidad, "localidades", "Localidades", ColeccionSoloLectura,
    fields=("id", "localidad_nombre", "localidad_departamento", "localidad_municipio"),
)


@csrf_exempt
def opciones_item_desconocido(request, collection_id):
    """
    OPTIONS /collections/{id}/items/unknown_id. Sobre una colección vacía, QGIS pregunta
    los permisos de edición con ese id ficticio (no tiene un feature real que usar) y si no
    recibe Allow deja la capa sin poder modificar ni borrar. django-oapif lo busca como un
    item real y responde 404, así que se contesta acá con los permisos de la colección.
    """
    if request.method != "OPTIONS":
        raise Http404
    coleccion = api.collections.get(collection_id)
    if coleccion is None:
        raise Http404
    BasicAuthCacheada()(request)
    if not coleccion.has_view_permission(request):
        raise Http404
    permitidos = ["OPTIONS", "GET"]
    if coleccion.has_change_permission(request):
        permitidos += ["PUT", "PATCH"]
    if coleccion.has_delete_permission(request):
        permitidos.append("DELETE")
    respuesta = HttpResponse()
    respuesta["Allow"] = ", ".join(permitidos)
    return respuesta
