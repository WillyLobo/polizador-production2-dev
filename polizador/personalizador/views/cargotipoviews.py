from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import CargoTipo
from personalizador.forms.cargotipoforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarCargoTipo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_cargotipo"

	model = CargoTipo
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-cargotipos")


@method_decorator(login_required, name="dispatch")
class CrearCargoTipo(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_cargotipo"

	model = CargoTipo
	template_name = "cargotipo/crear-cargotipo.html"
	form_class = CargoTipoForm
	success_url = reverse_lazy("personalizador:crear-cargotipo")
	popup_form_partial = "partials/cargotipo-form-partial.html"

	title = "Crear Tipo de Cargo"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateCargoTipo(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_cargotipo"

	model = CargoTipo
	template_name = "cargotipo/update-cargotipo.html"
	form_class = CargoTipoForm
	success_url = reverse_lazy("personalizador:lista-cargotipos")

@login_required
@permission_required('personalizador.view_cargotipo', raise_exception=True)
def PaginaListaCargoTipos(request):
	template_name = "Lista-cargotipos.html"

	return render(request, template_name, {})
