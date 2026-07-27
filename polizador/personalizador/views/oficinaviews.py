from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import Oficina
from personalizador.forms.oficinaforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarOficina(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_oficina"

	model = Oficina
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-oficinas")


@method_decorator(login_required, name="dispatch")
class CrearOficina(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_oficina"

	model = Oficina
	template_name = "oficina/crear-oficina.html"
	form_class = OficinaForm
	success_url = reverse_lazy("personalizador:crear-oficina")
	popup_form_partial = "partials/oficina-form-partial.html"

	title = "Crear Oficina"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateOficina(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_oficina"

	model = Oficina
	template_name = "oficina/update-oficina.html"
	form_class = OficinaForm
	success_url = reverse_lazy("personalizador:lista-oficinas")

@login_required
@permission_required('personalizador.view_oficina', raise_exception=True)
def PaginaListaOficinas(request):
	template_name = "Lista-oficinas.html"

	return render(request, template_name, {})
