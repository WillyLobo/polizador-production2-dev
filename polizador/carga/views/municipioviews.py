from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Municipio
from carga.forms.municipioforms import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class EliminarMunicipio(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_municipio"

	model = Municipio
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-municipios")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearMunicipio(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_municipio"

	model = Municipio
	template_name = "municipio/crear-municipio.html"
	form_class = MunicipioForm
	success_url = reverse_lazy("carga:crear-municipio")

	title = "Crear Municipio"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateMunicipio(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_municipio"

	model = Municipio
	template_name = "municipio/update-municipio.html"
	form_class = MunicipioForm
	success_url = reverse_lazy("carga:lista-municipios")

@method_decorator(login_required, name="dispatch")
class MunicipioObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_municipio"

	model = Municipio
	template_name = "municipio/municipio-obra.html"
	
@login_required
@permission_required("carga.view_municipio", raise_exception=True)
def PaginaListaMunicipio(request):
	template_name = "Lista-municipios.html"

	return render(request, template_name, {})

