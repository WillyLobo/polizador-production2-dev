from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Region
from carga.forms.regionforms import *
from core.mixins import DeleteRelatedObjectsMixin

@method_decorator(login_required, name="dispatch")
class EliminarRegion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "carga.delete_region"

	model = Region
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-regiones")


@method_decorator(login_required, name="dispatch")
class CrearRegion(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_region"

	model = Region
	template_name = "region/crear-region.html"
	form_class = RegionForm
	success_url = reverse_lazy("carga:crear-region")

	title = "Crear Región"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateRegion(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_region"

	model = Region
	template_name = "region/update-region.html"
	form_class = RegionForm
	success_url = reverse_lazy("carga:lista-regiones")

@method_decorator(login_required, name="dispatch")
class RegionObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_region"

	model = Region
	template_name = "region/region-obra.html"

@login_required
@permission_required('carga.view_region', raise_exception=True)
def PaginaListaRegiones(request):
	template_name = "Lista-regiones.html"

	return render(request, template_name, {})

