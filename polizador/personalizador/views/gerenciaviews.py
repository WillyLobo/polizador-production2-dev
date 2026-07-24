from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import Gerencia
from personalizador.forms.gerenciaforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarGerencia(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_gerencia"

	model = Gerencia
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-gerencias")


@method_decorator(login_required, name="dispatch")
class CrearGerencia(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_gerencia"

	model = Gerencia
	template_name = "gerencia/crear-gerencia.html"
	form_class = GerenciaForm
	success_url = reverse_lazy("personalizador:crear-gerencia")
	popup_form_partial = "partials/gerencia-form-partial.html"

	title = "Crear Gerencia"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateGerencia(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_gerencia"

	model = Gerencia
	template_name = "gerencia/update-gerencia.html"
	form_class = GerenciaForm
	success_url = reverse_lazy("personalizador:lista-gerencias")

@login_required
@permission_required('personalizador.view_gerencia', raise_exception=True)
def PaginaListaGerencias(request):
	template_name = "Lista-gerencias.html"

	return render(request, template_name, {})
