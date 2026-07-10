from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI
from ninja.security import SessionAuth

api = NinjaAPI(
    auth=SessionAuth(),
    docs_decorator=staff_member_required,
    title="Polizador API",
    description="API para el sistema Polizador de gestión de viáticos y obras.",
    version="1.0.0",
    urls_namespace="api-1.0",
)


@api.get("__version__", auth=None)
def get_version(request):
    return {"version": "1.0.0"}


# Each app owns its own Router; mounted here at the API root so URL paths are unchanged.
from api.views.carga_views import router as carga_router
from api.views.secretariador_views import router as secretariador_router
from api.views.personalizador_views import router as personalizador_router
from api.views.select2_views import router as select2_router

api.add_router("", carga_router)
api.add_router("", secretariador_router)
api.add_router("", personalizador_router)
api.add_router("", select2_router)
