from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from django.views.static import serve

from django.conf import settings


class SchemaDocsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "schema_docs/index.html"

    def test_func(self):
        return self.request.user.is_superuser


@xframe_options_sameorigin
def schema_docs_asset(request, path):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied
    return serve(request, path, document_root=settings.SCHEMA_DOCS_ROOT)
