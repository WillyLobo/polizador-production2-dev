from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import CEIC
from personalizador.forms.ceicforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarCEIC(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_ceic"

	model = CEIC
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-ceics")


@method_decorator(login_required, name="dispatch")
class CrearCEIC(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_ceic"

	model = CEIC
	template_name = "ceic/crear-ceic.html"
	form_class = CEICForm
	success_url = reverse_lazy("personalizador:crear-ceic")
	popup_form_partial = "partials/ceic-form-partial.html"

	title = "Crear CEIC"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateCEIC(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_ceic"

	model = CEIC
	template_name = "ceic/update-ceic.html"
	form_class = CEICForm
	success_url = reverse_lazy("personalizador:lista-ceics")

@login_required
@permission_required('personalizador.view_ceic', raise_exception=True)
def PaginaListaCEICs(request):
	template_name = "Lista-ceics.html"

	return render(request, template_name, {})
