from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import DenominacionCargo
from personalizador.forms.denominacioncargoforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarDenominacionCargo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_denominacioncargo"

	model = DenominacionCargo
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-denominacioncargos")


@method_decorator(login_required, name="dispatch")
class CrearDenominacionCargo(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_denominacioncargo"

	model = DenominacionCargo
	template_name = "denominacioncargo/crear-denominacioncargo.html"
	form_class = DenominacionCargoForm
	success_url = reverse_lazy("personalizador:crear-denominacioncargo")
	popup_form_partial = "partials/denominacioncargo-form-partial.html"

	title = "Crear Denominación de Cargo"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateDenominacionCargo(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_denominacioncargo"

	model = DenominacionCargo
	template_name = "denominacioncargo/update-denominacioncargo.html"
	form_class = DenominacionCargoForm
	success_url = reverse_lazy("personalizador:lista-denominacioncargos")

@login_required
@permission_required('personalizador.view_denominacioncargo', raise_exception=True)
def PaginaListaDenominacionCargos(request):
	template_name = "Lista-denominacioncargos.html"

	return render(request, template_name, {})
