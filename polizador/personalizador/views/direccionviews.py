from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import Direccion
from personalizador.forms.direccionforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarDireccion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_direccion"

	model = Direccion
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-direcciones")


@method_decorator(login_required, name="dispatch")
class CrearDireccion(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_direccion"

	model = Direccion
	template_name = "direccion/crear-direccion.html"
	form_class = DireccionForm
	success_url = reverse_lazy("personalizador:crear-direccion")
	popup_form_partial = "partials/direccion-form-partial.html"

	title = "Crear Dirección"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateDireccion(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_direccion"

	model = Direccion
	template_name = "direccion/update-direccion.html"
	form_class = DireccionForm
	success_url = reverse_lazy("personalizador:lista-direcciones")

@login_required
@permission_required('personalizador.view_direccion', raise_exception=True)
def PaginaListaDirecciones(request):
	template_name = "Lista-direcciones.html"

	return render(request, template_name, {})
