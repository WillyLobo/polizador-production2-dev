from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Aseguradora
from carga.forms.aseguradoraforms import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class EliminarAseguradora(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_aseguradora"

	model = Aseguradora
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-aseguradoras")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearAseguradora(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_aseguradora"

	model = Aseguradora
	template_name = "aseguradora/crear-aseguradora.html"
	form_class = AseguradoraForm
	success_url = reverse_lazy("carga:crear-aseguradora")

	title = "Crear Aseguradora"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateAseguradora(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_aseguradora"

	model = Aseguradora
	template_name = "aseguradora/update-aseguradora.html"
	form_class = AseguradoraForm
	success_url = reverse_lazy("carga:lista-aseguradoras")

@login_required
@permission_required('carga.view_aseguradora', raise_exception=True)
def PaginaListaAseguradoras(request):
	template_name = "Lista-aseguradoras.html"

	return render(request, template_name, {})

