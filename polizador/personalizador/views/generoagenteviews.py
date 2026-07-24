from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import GeneroAgente
from personalizador.forms.generoagenteforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarGeneroAgente(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_generoagente"

	model = GeneroAgente
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-generoagentes")


@method_decorator(login_required, name="dispatch")
class CrearGeneroAgente(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_generoagente"

	model = GeneroAgente
	template_name = "generoagente/crear-generoagente.html"
	form_class = GeneroAgenteForm
	success_url = reverse_lazy("personalizador:crear-generoagente")
	popup_form_partial = "partials/generoagente-form-partial.html"

	title = "Crear Género"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateGeneroAgente(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_generoagente"

	model = GeneroAgente
	template_name = "generoagente/update-generoagente.html"
	form_class = GeneroAgenteForm
	success_url = reverse_lazy("personalizador:lista-generoagentes")

@login_required
@permission_required('personalizador.view_generoagente', raise_exception=True)
def PaginaListaGeneroAgentes(request):
	template_name = "Lista-generoagentes.html"

	return render(request, template_name, {})
