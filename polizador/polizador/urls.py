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
    FormValidationErrorListView,
    KnowledgeBaseIndexView,
    KnowledgeBasePageView,
    ManagementCommandRunDetailView,
    ManagementCommandRunKillView,
    ManagementCommandRunLogView,
    ManagementCommandsView,
    SchemaDocsView,
    TodoCreateView,
    TodoDeleteView,
    TodoListView,
    TodoStatusUpdateView,
    TodoUpdateView,
    schema_docs_asset,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("accounts/", include('allauth.urls')),
    path("obra/", include("carga.urls")),
    path("viaticos/", include("secretariador.urls")),
    path("personal/", include("personalizador.urls")),
    #path("api/", include("api.urls")),
    path("v1/api/", include(("api.urls", "api"), namespace="api-1.0")),
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("home/", InspeccionHomeView.as_view(), name="home"),
    path("administracion/dashboard/", DashboardView.as_view(), name="dashboard"),
    path("administracion/errores-validacion/", FormValidationErrorListView.as_view(), name="form_validation_errors"),
    path("administracion/schema/", SchemaDocsView.as_view(), name="schema_docs"),
    path("administracion/schema/<path:path>", schema_docs_asset, name="schema_docs_asset"),
    path("administracion/comandos/", ManagementCommandsView.as_view(), name="management_commands"),
    path("administracion/conocimiento/", KnowledgeBaseIndexView.as_view(), name="knowledge_base"),
    path(
        "administracion/conocimiento/<path:page_path>/",
        KnowledgeBasePageView.as_view(),
        name="knowledge_base_page",
    ),
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
    path("administracion/tareas/", TodoListView.as_view(), name="todo_list"),
    path("administracion/tareas/nueva/", TodoCreateView.as_view(), name="todo_create"),
    path("administracion/tareas/<int:pk>/editar/", TodoUpdateView.as_view(), name="todo_update"),
    path("administracion/tareas/<int:pk>/eliminar/", TodoDeleteView.as_view(), name="todo_delete"),
    path("administracion/tareas/<int:pk>/estado/", TodoStatusUpdateView.as_view(), name="todo_status_update"),
]
debugpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    # Cambia MEDIA_URL y MEDIA_ROOT si debug=True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debugpatterns
