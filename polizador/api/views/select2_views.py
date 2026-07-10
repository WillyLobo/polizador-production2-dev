# select2 autocomplete endpoints (used by report forms across carga/secretariador)
from django.db.models import Q
from ninja import Router
from api.schemas.select2_schemas import Select2ResponseSchema

router = Router(tags=["select2"])

# --- Comisionados ---
@router.get("/select2_comisionado/", response=Select2ResponseSchema)
def select2_comisionados(request, q: str = None):
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
@router.get("/select2_localidad/", response=Select2ResponseSchema)
def select2_localidad(request, q: str = None):
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
@router.get("/select2_empresa/", response=Select2ResponseSchema)
def select2_empresa(request, q: str = None):
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
@router.get("/select2_programa/", response=Select2ResponseSchema)
def select2_programa(request, q: str = None):
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

# --- Obras ---
@router.get("/select2_obra/", response=Select2ResponseSchema)
def select2_obra(request, q: str = None):
    from carga.models import Obra

    queryset = Obra.objects.all()

    if q:
        queryset = queryset.filter(
            Q(obra_nombre__icontains=q)
        )
    # Limit results to keep payloads fast and responsive
    results_limit = queryset[:20]

    formatted_results = [
        {"id": item.id, "text": item.obra_nombre} for item in results_limit
    ]

    return {"results": formatted_results}

# --- Rubros de Obra ---
@router.get("/select2_rubro_obra/", response=Select2ResponseSchema)
def select2_rubro_obra(request, q: str = None):
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
@router.get("/select2_rubro_certificado/", response=Select2ResponseSchema)
def select2_rubro_certificado(request, q: str = None):
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