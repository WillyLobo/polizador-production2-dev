# secretariador app API views
from django.db.models import Q
from django.views.decorators.cache import cache_page
import datetime
from api.router import api
from api.permissions import require_auth, get_group_perms
from api.schemas.select2_schemas import Select2ResponseSchema


def _parse_date(s):
    if not s:
        return None
    try:
        return datetime.date.fromisoformat(s)
    except (ValueError, TypeError):
        return None

# --- Comisionados ---
@api.get("/select2_comisionado/", response=Select2ResponseSchema, tags=["select2"])
def select2_comisionados(request, q: str = None):
    user = require_auth(request)
    from personalizador.models import Agente

    queryset = Agente.objects.all()

    if q:
        queryset = queryset.filter(
            Q(agente_nombreyapellido__icontains=q)
        )
    # Limit results to keep payloads fast and responsive
    results_limit = queryset[:20]

    formatted_results = [
        {"id": item.id, "text": item.agente_nombreyapellido} for item in results_limit
    ]

    return {"results": formatted_results}

# --- Localidades ---
@api.get("/select2_localidad/", response=Select2ResponseSchema, tags=["select2"])
def select2_localidad(request, q: str = None):
    user = require_auth(request)
    from carga.models import Localidad

    queryset = Localidad.objects.all()

    if q:
        queryset = queryset.filter(
            Q(localidad_nombre__icontains=q)
        )
    # Limit results to keep payloads fast and responsive
    results_limit = queryset[:20]

    formatted_results = [
        {"id": item.id, "text": item.localidad_nombre} for item in results_limit
    ]

    return {"results": formatted_results}

# --- Empresas ---
@api.get("/select2_empresa/", response=Select2ResponseSchema, tags=["select2"])
def select2_empresa(request, q: str = None):
    user = require_auth(request)
    from carga.models import Empresa

    queryset = Empresa.objects.all()

    if q:
        queryset = queryset.filter(
            Q(empresa_nombre__icontains=q)
        )
    # Limit results to keep payloads fast and responsive
    results_limit = queryset[:20]

    formatted_results = [
        {"id": item.id, "text": item.empresa_nombre} for item in results_limit
    ]

    return {"results": formatted_results}

# --- Programa ---
@api.get("/select2_programa/", response=Select2ResponseSchema, tags=["select2"])
def select2_programa(request, q: str = None):
    user = require_auth(request)
    from carga.models import Programa

    queryset = Programa.objects.all()

    if q:
        queryset = queryset.filter(
            Q(programa_nombre__icontains=q)
        )
    # Limit results to keep payloads fast and responsive
    results_limit = queryset[:20]

    formatted_results = [
        {"id": item.id, "text": item.programa_nombre} for item in results_limit
    ]

    return {"results": formatted_results}

# --- Rubros de Obra ---
@api.get("/select2_rubro_obra/", response=Select2ResponseSchema, tags=["select2"])
def select2_rubro_obra(request, q: str = None):
    user = require_auth(request)
    from carga.models import ContratoRubro

    queryset = ContratoRubro.objects.all()

    if q:
        queryset = queryset.filter(
            Q(contratorubro_tipo__icontains=q)
        )
    # Limit results to keep payloads fast and responsive
    results_limit = queryset[:20]

    formatted_results = [
        {"id": item.id, "text": item.contratorubro_tipo} for item in results_limit
    ]

    return {"results": formatted_results}

# --- Rubros de Certificado ---
@api.get("/select2_rubro_certificado/", response=Select2ResponseSchema, tags=["select2"])
def select2_rubro_certificado(request, q: str = None):
    user = require_auth(request)
    from carga.models import CertificadoRubro

    queryset = CertificadoRubro.objects.all()

    if q:
        queryset = queryset.filter(
            Q(certificadorubro_nombre__icontains=q)
        )
    # Limit results to keep payloads fast and responsive
    results_limit = queryset[:20]

    formatted_results = [
        {"id": item.id, "text": item.certificadorubro_nombre} for item in results_limit
    ]

    return {"results": formatted_results}