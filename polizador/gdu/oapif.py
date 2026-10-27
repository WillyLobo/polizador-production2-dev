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
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import AutoField, BigAutoField, CharField, ProtectedError, RestrictedError, TextField
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_oapif import OAPIF, OapifCollection
from django_oapif.auth import BasicAuth, DjangoAuth
from django_oapif.crs import CRS84
from ninja.errors import AuthorizationError, HttpError, ValidationError

from gdu.models import Barrio, Intervencion, PlanoMensura, PlanoMensuraIntervencion

api = OAPIF(
    title="GDU",
    description="Capas de la Gerencia de Desarrollo Urbano (IPDUV)",
    urls_namespace="gdu-oapif",
    auth=[BasicAuth(), DjangoAuth()],
)

MENSAJES_VALIDACION = {
    "string_too_long": lambda e: f"admite como máximo {e.get('ctx', {}).get('max_length')} caracteres",
    "missing": lambda e: "es obligatorio",
    "int_parsing": lambda e: "tiene que ser un número entero",
    "float_parsing": lambda e: "tiene que ser un número",
    "bool_parsing": lambda e: "tiene que ser verdadero o falso",
    "extra_forbidden": lambda e: "no es un campo de la capa",
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
            raise ValidationError([
                {"loc": ["body", "feature", "properties", campo], "msg": " ".join(mensajes), "type": "value_error"}
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


@api.register(Barrio)
class Barrios(ColeccionGdu):
    id = "barrios"
    title = "Barrios"


@api.register(PlanoMensura)
class PlanosMensura(ColeccionGdu):
    id = "planos_mensura"
    title = "Planos de mensura"


@api.register(PlanoMensuraIntervencion)
class PlanosMensuraIntervencion(ColeccionGdu):
    id = "planos_mensura_intervencion"
    title = "Planos de mensura por intervención"


@api.register(Intervencion)
class Intervenciones(ColeccionSoloLectura):
    # sin geometría: la usan los formularios de QGIS como lista de valores (FK intervencion)
    id = "intervenciones"
    title = "Intervenciones"
    fields = ("id", "nombre", "contratacion", "localidad", "tipo", "estado", "plan", "grupo")


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
    BasicAuth()(request)
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
