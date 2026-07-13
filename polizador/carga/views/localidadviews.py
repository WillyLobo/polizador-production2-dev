from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Localidad
from carga.forms.localidadforms import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class EliminarLocalidad(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_localidad"

	model = Localidad
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-localidades")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearLocalidad(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_localidad"

	model = Localidad
	template_name = "localidad/crear-localidad.html"
	form_class = LocalidadForm
	success_url = reverse_lazy("carga:crear-localidad")
	
	title = "Crear Localidad"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateLocalidad(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_localidad"

	model = Localidad
	template_name = "localidad/update-localidad.html"
	form_class = LocalidadForm
	success_url = reverse_lazy("carga:lista-localidades")

@method_decorator(login_required, name="dispatch")
class LocalidadObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_localidad"

	model = Localidad
	template_name = "localidad/localidad-obra.html"

@login_required
@permission_required("carga.view_localidad", raise_exception=True)
def PaginaListaLocalidad(request):
	template_name = "Lista-localidades.html"

	return render(request, template_name, {})

