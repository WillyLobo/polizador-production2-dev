from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI

api = NinjaAPI(
    docs_decorator=staff_member_required,
    title="Polizador API",
    description="API para el sistema Polizador de gestión de viáticos y obras.",
    version="1.0.0",
    urls_namespace="api-1.0",
)


@api.get("__version__")
def get_version(request):
    return {"version": "1.0.0"}


# Import all view modules to register routes via api decorators
from api.views import carga_views, secretariador_views, personalizador_views, select2_views  # noqa: F401
