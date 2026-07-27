from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import ApartadoCargo
from personalizador.forms.apartadocargoforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarApartadoCargo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_apartadocargo"

	model = ApartadoCargo
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-apartadocargos")


@method_decorator(login_required, name="dispatch")
class CrearApartadoCargo(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_apartadocargo"

	model = ApartadoCargo
	template_name = "apartadocargo/crear-apartadocargo.html"
	form_class = ApartadoCargoForm
	success_url = reverse_lazy("personalizador:crear-apartadocargo")
	popup_form_partial = "partials/apartadocargo-form-partial.html"

	title = "Crear Apartado"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateApartadoCargo(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_apartadocargo"

	model = ApartadoCargo
	template_name = "apartadocargo/update-apartadocargo.html"
	form_class = ApartadoCargoForm
	success_url = reverse_lazy("personalizador:lista-apartadocargos")

@login_required
@permission_required('personalizador.view_apartadocargo', raise_exception=True)
def PaginaListaApartadoCargos(request):
	template_name = "Lista-apartadocargos.html"

	return render(request, template_name, {})
