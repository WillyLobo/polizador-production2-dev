from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import DetailView, TemplateView, View
from django.views.static import serve

from django.conf import settings

from core import dashboard_data, management_runner
from core.management_commands_registry import COMMAND_REGISTRY
from core.models import ManagementCommandRun


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SchemaDocsView(SuperuserRequiredMixin, TemplateView):
    template_name = "schema_docs/index.html"


class DashboardView(SuperuserRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

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
        context["recent_logins"] = dashboard_data.recent_logins()
        context["sentry_health"] = dashboard_data.sentry_health()
        context["db_health"] = dashboard_data.db_health()
        context["db_performance"] = dashboard_data.db_performance()
        return context


@xframe_options_sameorigin
def schema_docs_asset(request, path):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied
    return serve(request, path, document_root=settings.SCHEMA_DOCS_ROOT)


class ManagementCommandsView(SuperuserRequiredMixin, TemplateView):
    template_name = "comandos/list.html"

    def get_selected(self):
        key = self.request.GET.get("command") or self.request.POST.get("command")
        return key, COMMAND_REGISTRY.get(key)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_command, selected_meta = self.get_selected()
        context["registry"] = COMMAND_REGISTRY
        context["selected_command"] = selected_command
        context["selected_meta"] = selected_meta
        if selected_meta:
            context.setdefault("form", selected_meta["form"]())
        context["recent_runs"] = ManagementCommandRun.objects.select_related("started_by")[:20]
        return context

    def post(self, request, *args, **kwargs):
        selected_command, selected_meta = self.get_selected()
        if not selected_meta:
            messages.error(request, "Comando inválido.")
            return redirect("management_commands")

        if ManagementCommandRun.objects.filter(status=ManagementCommandRun.Status.RUNNING).exists():
            messages.error(request, "Ya hay un comando en ejecución. Esperá a que termine antes de iniciar otro.")
            return redirect(f"{reverse('management_commands')}?command={selected_command}")

        form = selected_meta["form"](request.POST)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        run = management_runner.start_run(selected_command, form.to_argv(), request.user)
        return redirect("management_command_run_detail", pk=run.pk)


class ManagementCommandRunDetailView(SuperuserRequiredMixin, DetailView):
    model = ManagementCommandRun
    template_name = "comandos/detail.html"
    context_object_name = "run"


class ManagementCommandRunLogView(SuperuserRequiredMixin, View):
    def get(self, request, pk):
        run = get_object_or_404(ManagementCommandRun, pk=pk)
        offset = int(request.GET.get("offset", 0))
        return JsonResponse(
            {
                "chunk": run.log[offset:],
                "offset": len(run.log),
                "status": run.status,
                "status_label": run.get_status_display(),
                "duration_display": run.duration_display,
            }
        )


class ManagementCommandRunKillView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        run = get_object_or_404(ManagementCommandRun, pk=pk)
        management_runner.kill_run(run)
        return redirect("management_command_run_detail", pk=run.pk)
