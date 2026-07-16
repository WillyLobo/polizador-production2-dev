from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from secretariador.models import Vehiculo
from secretariador.forms.vehiculoform import VehiculoForm
from core.mixins import DeleteRelatedObjectsMixin

@method_decorator(login_required, name="dispatch")
class CrearVehiculo(PermissionRequiredMixin, generic.CreateView):
	permission_required = "secretariador.add_vehiculo"

	model = Vehiculo
	template_name = "vehiculo/crear-vehiculo.html"
	form_class = VehiculoForm
	success_url = reverse_lazy("secretariador:crear-vehiculo")
	
	title = "Crear Vehiculo"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

@method_decorator(login_required, name="dispatch")
class UpdateVehiculo(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "secretariador.change_vehiculo"

	model = Vehiculo
	template_name = "vehiculo/update-vehiculo.html"
	form_class = VehiculoForm
	success_url = reverse_lazy("secretariador:crear-vehiculo")

@method_decorator(login_required, name="dispatch")
class EliminarVehiculo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "secretariador.delete_vehiculo"

	model = Vehiculo
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-vehiculos")

@login_required
@permission_required("secretariador.view_vehiculo", raise_exception=True)
def PaginaListaVehiculos(request):
	template_name = "Lista-vehiculos.html"

	return render(request, template_name, {})

