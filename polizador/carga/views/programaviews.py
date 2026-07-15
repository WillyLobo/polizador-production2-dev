from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Programa
from carga.forms.programaforms import *
from carga.views.generics import get_deleted_objects, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarPrograma(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_programa"

	model = Programa
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-programas")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearPrograma(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_programa"

	model = Programa
	template_name = "programa/crear-programa.html"
	form_class = ProgramaForm
	success_url = reverse_lazy("carga:crear-programa")
	popup_form_partial = "partials/programa-form-partial.html"

	title = "Crear Programa"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

@method_decorator(login_required, name="dispatch")
class UpdatePrograma(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_programa"

	model = Programa
	template_name = "programa/update-programa.html"
	form_class = ProgramaForm
	success_url = reverse_lazy("carga:lista-programas")

@method_decorator(login_required, name="dispatch")
class ProgramaObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_programa"

	model = Programa
	template_name = "programa/programa-obra.html"

@login_required
@permission_required('carga.view_programa', raise_exception=True)
def PaginaListaProgramas(request):
	template_name = "Lista-programas.html"

	return render(request, template_name, {})

