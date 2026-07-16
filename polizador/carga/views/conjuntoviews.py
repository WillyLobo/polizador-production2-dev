from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import ConjuntoLicitado
from carga.forms.conjuntoforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarConjunto(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "carga.delete_conjuntolicitado"

	model = ConjuntoLicitado
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-conjuntos")

@method_decorator(login_required, name="dispatch")
class CrearConjunto(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_conjuntolicitado"

	model = ConjuntoLicitado
	template_name = "conjunto/crear-conjunto.html"
	form_class = ConjuntoForm
	success_url = reverse_lazy("carga:crear-conjunto")
	popup_form_partial = "partials/conjunto-form-partial.html"

	title = "Crear Conjunto"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

@method_decorator(login_required, name="dispatch")
class UpdateConjunto(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_conjuntolicitado"

	model = ConjuntoLicitado
	template_name = "conjunto/update-conjunto.html"
	form_class = ConjuntoForm
	success_url = reverse_lazy("carga:lista-conjuntos")

@method_decorator(login_required, name="dispatch")
class ConjuntoObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_conjuntolicitado"

	model = ConjuntoLicitado
	template_name = "conjunto/conjunto-obra.html"

@login_required
@permission_required('carga.view_conjuntolicitado', raise_exception=True)
def PaginaListaConjuntos(request):
	template_name = "Lista-conjuntos.html"

	return render(request, template_name, {})

