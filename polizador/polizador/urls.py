from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from carga.views.inspeccionviews import InspeccionHomeView
from django.contrib.auth.decorators import login_required
from core.views import (
    DashboardView,
    ManagementCommandRunDetailView,
    ManagementCommandRunKillView,
    ManagementCommandRunLogView,
    ManagementCommandsView,
    SchemaDocsView,
    schema_docs_asset,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("accounts/", include('allauth.urls')),
    path("obra/", include("carga.urls")),
    path("viaticos/", include("secretariador.urls")),
    path("personal/", include("personalizador.urls")),
    path("gdu/", include("gdu.urls")),
    #path("api/", include("api.urls")),
    path("v1/api/", include(("api.urls", "api"), namespace="api-1.0")),
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("home/", InspeccionHomeView.as_view(), name="home"),
    path("administracion/dashboard/", DashboardView.as_view(), name="dashboard"),
    path("administracion/schema/", SchemaDocsView.as_view(), name="schema_docs"),
    path("administracion/schema/<path:path>", schema_docs_asset, name="schema_docs_asset"),
    path("administracion/comandos/", ManagementCommandsView.as_view(), name="management_commands"),
    path(
        "administracion/comandos/<int:pk>/",
        ManagementCommandRunDetailView.as_view(),
        name="management_command_run_detail",
    ),
    path(
        "administracion/comandos/<int:pk>/log/",
        ManagementCommandRunLogView.as_view(),
        name="management_command_run_log",
    ),
    path(
        "administracion/comandos/<int:pk>/kill/",
        ManagementCommandRunKillView.as_view(),
        name="management_command_run_kill",
    ),
]
debugpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    # Cambia MEDIA_URL y MEDIA_ROOT si debug=True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debugpatterns
