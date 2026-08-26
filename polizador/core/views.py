import posixpath
import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from django.views.static import serve

from django.conf import settings

from core import dashboard_data, knowledge_base, management_runner
from core.forms import TodoForm
from core.management_commands_registry import COMMAND_REGISTRY
from core.models import ManagementCommandRun, Todo


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SchemaDocsView(SuperuserRequiredMixin, TemplateView):
    template_name = "schema_docs/index.html"


class FormValidationErrorListView(SuperuserRequiredMixin, TemplateView):
    template_name = "errores_validacion/list.html"


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


_MD_LINK_RE = re.compile(r'href="([^"#?]+)\.md"')


def _rewrite_doc_links(html: str, page_path: str) -> str:
    """Reescribe los links relativos `../modulo/Simbolo.md` que las páginas autoradas usan
    en "Ver también" (ver knowledge_base/README.md) a la URL real de knowledge_base_page."""
    base_dir = posixpath.dirname(page_path)

    def repl(match):
        relative = match.group(1)
        if relative.startswith(("http://", "https://")):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(base_dir, relative))
        return f'href="{reverse("knowledge_base_page", kwargs={"page_path": resolved})}"'

    return _MD_LINK_RE.sub(repl, html)


class KnowledgeBaseIndexView(SuperuserRequiredMixin, TemplateView):
    template_name = "knowledge_base/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tree = knowledge_base.load_tree()
        all_symbols = [s for modules in tree.values() for symbols in modules.values() for s in symbols]
        context["tree"] = tree
        context["total_symbols"] = len(all_symbols)
        context["authored_symbols"] = sum(1 for s in all_symbols if s["authored"])
        return context


class KnowledgeBasePageView(SuperuserRequiredMixin, TemplateView):
    template_name = "knowledge_base/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_path = kwargs["page_path"].strip("/")
        symbol = knowledge_base.resolve_page_path(page_path)
        if symbol is None:
            raise Http404(f"No se conoce la página de base de conocimiento '{page_path}'.")

        html_file = knowledge_base.html_path(page_path)
        content_html = None
        if html_file.exists():
            content_html = _rewrite_doc_links(html_file.read_text(encoding="utf-8"), page_path)

        parts = page_path.split("/")
        context["tree"] = knowledge_base.load_tree()
        context["symbol"] = symbol
        context["page_path"] = page_path
        context["content_html"] = content_html
        context["breadcrumbs"] = parts
        context["current_app"] = parts[0]
        context["current_module"] = "/".join(parts[1:-1])
        return context


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


class TodoListView(SuperuserRequiredMixin, ListView):
    model = Todo
    template_name = "todo/list.html"
    context_object_name = "todos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TodoForm()
        context["status_choices"] = Todo.Status.choices
        return context


class TodoCreateView(SuperuserRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "todo/form.html"
    success_url = reverse_lazy("todo_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TodoUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "todo/form.html"
    success_url = reverse_lazy("todo_list")


class TodoDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Todo
    template_name = "todo/confirm_delete.html"
    success_url = reverse_lazy("todo_list")


class TodoStatusUpdateView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        status = request.POST.get("status")
        if status not in Todo.Status.values:
            messages.error(request, "Estado inválido.")
            return redirect("todo_list")
        todo.status = status
        todo.save(update_fields=["status", "updated_at"])
        return redirect("todo_list")
