from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import GrupoCargo
from personalizador.forms.grupocargoforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarGrupoCargo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_grupocargo"

	model = GrupoCargo
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-grupocargos")


@method_decorator(login_required, name="dispatch")
class CrearGrupoCargo(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_grupocargo"

	model = GrupoCargo
	template_name = "grupocargo/crear-grupocargo.html"
	form_class = GrupoCargoForm
	success_url = reverse_lazy("personalizador:crear-grupocargo")
	popup_form_partial = "partials/grupocargo-form-partial.html"

	title = "Crear Grupo de Cargo"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateGrupoCargo(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_grupocargo"

	model = GrupoCargo
	template_name = "grupocargo/update-grupocargo.html"
	form_class = GrupoCargoForm
	success_url = reverse_lazy("personalizador:lista-grupocargos")

@login_required
@permission_required('personalizador.view_grupocargo', raise_exception=True)
def PaginaListaGrupoCargos(request):
	template_name = "Lista-grupocargos.html"

	return render(request, template_name, {})
