from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import Departamento
from personalizador.forms.departamentoforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarDepartamento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_departamento"

	model = Departamento
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-departamentos")


@method_decorator(login_required, name="dispatch")
class CrearDepartamento(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_departamento"

	model = Departamento
	template_name = "departamento-personal/crear-departamento.html"
	form_class = DepartamentoForm
	success_url = reverse_lazy("personalizador:crear-departamento")
	popup_form_partial = "partials/departamento-personal-form-partial.html"

	title = "Crear Departamento"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateDepartamento(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_departamento"

	model = Departamento
	template_name = "departamento-personal/update-departamento.html"
	form_class = DepartamentoForm
	success_url = reverse_lazy("personalizador:lista-departamentos")

@login_required
@permission_required('personalizador.view_departamento', raise_exception=True)
def PaginaListaDepartamentos(request):
	template_name = "Lista-departamentos-personal.html"

	return render(request, template_name, {})
