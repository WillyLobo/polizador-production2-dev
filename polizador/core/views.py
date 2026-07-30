from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from django.views.static import serve

from django.conf import settings

from core import dashboard_data


class SchemaDocsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "schema_docs/index.html"

    def test_func(self):
        return self.request.user.is_superuser


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/index.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apps"] = [
            {
                "app_label": app_label,
                "display": dashboard_data.APP_DISPLAY_NAMES[app_label],
                "model_labels": [label for _, _, label in dashboard_data.TRACKED_MODELS[app_label]],
                "changes": dashboard_data.changes_feed(app_label),
            }
            for app_label in dashboard_data.TRACKED_MODELS
        ]
        context["login_summary"] = dashboard_data.login_summary()
        context["sentry_health"] = dashboard_data.sentry_health()
        context["db_health"] = dashboard_data.db_health()
        return context


@xframe_options_sameorigin
def schema_docs_asset(request, path):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied
    return serve(request, path, document_root=settings.SCHEMA_DOCS_ROOT)
