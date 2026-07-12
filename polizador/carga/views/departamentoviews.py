from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from carga.models import Departamento
from carga.forms.departamentoforms import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class EliminarDepartamento(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_departamento"

	model = Departamento
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-departamentos")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearDepartamento(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_departamento"

	model = Departamento
	template_name = "departamento/crear-departamento.html"
	form_class = DepartamentoForm
	success_url = reverse_lazy("carga:crear-departamento")

	title = "Crear Departamento"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateDepartamento(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_departamento"

	model = Departamento
	template_name = "departamento/update-departamento.html"
	form_class = DepartamentoForm
	success_url = reverse_lazy("carga:lista-departamentos")

@method_decorator(login_required, name="dispatch")
class DepartamentoObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_departamento"

	model = Departamento
	template_name = "departamento/departamento-obra.html"

@login_required
def PaginaListaDepartamentos(request):
	template_name = "Lista-departamentos.html"

	return render(request, template_name, {})


