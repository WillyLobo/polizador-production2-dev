from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import InstrumentoAgente
from personalizador.forms.instrumentoagenteforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarInstrumentoAgente(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_instrumentoagente"

	model = InstrumentoAgente
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-instrumentoagentes")
	protected_error_message = "No se puede eliminar: el instrumento está vinculado a uno o más agentes."


@method_decorator(login_required, name="dispatch")
class CrearInstrumentoAgente(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_instrumentoagente"

	model = InstrumentoAgente
	template_name = "instrumentoagente/crear-instrumentoagente.html"
	form_class = InstrumentoAgenteForm
	success_url = reverse_lazy("personalizador:crear-instrumentoagente")
	popup_form_partial = "partials/instrumentoagente-form-partial.html"

	title = "Crear Instrumento Externo"

	def get_title(self):
		return self.title

	def get_form_class(self):
		return InstrumentoAgentePopupForm if self.is_popup() else super().get_form_class()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateInstrumentoAgente(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_instrumentoagente"

	model = InstrumentoAgente
	template_name = "instrumentoagente/update-instrumentoagente.html"
	form_class = InstrumentoAgenteForm
	success_url = reverse_lazy("personalizador:lista-instrumentoagentes")

@login_required
@permission_required('personalizador.view_instrumentoagente', raise_exception=True)
def PaginaListaInstrumentoAgentes(request):
	template_name = "Lista-instrumentoagentes.html"

	return render(request, template_name, {})
