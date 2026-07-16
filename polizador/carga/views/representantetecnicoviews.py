from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from personalizador.models import RepresentanteTecnico
from carga.forms.representantetecnicoforms import *
from core.mixins import DeleteRelatedObjectsMixin

@method_decorator(login_required, name="dispatch")
class EliminarRepresentanteTecnico(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_representantetecnico"

	model = RepresentanteTecnico
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-representantetecnicos")


@method_decorator(login_required, name="dispatch")
class CrearRepresentanteTecnico(PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_representantetecnico"

	model = RepresentanteTecnico
	template_name = "representantetecnico/crear-representantetecnico.html"
	form_class = RepresentanteTecnicoForm
	success_url = reverse_lazy("carga:crear-representantetecnico")

	title = "Crear Representante Técnico"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateRepresentanteTecnico(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_representantetecnico"

	model = RepresentanteTecnico
	template_name = "representantetecnico/update-representantetecnico.html"
	form_class = RepresentanteTecnicoForm
	success_url = reverse_lazy("carga:lista-representantetecnicos")

@method_decorator(login_required, name="dispatch")
class RepresentanteTecnicoObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "personalizador.view_representantetecnico"

	model = RepresentanteTecnico
	template_name = "representantetecnico/representantetecnico-obra.html"

@login_required
@permission_required("personalizador.view_representantetecnico", raise_exception=True)
def PaginaListaRepresentantesTecnicos(request):
	template_name = "Lista-representantetecnicos.html"

	return render(request, template_name, {})


