from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import Directorio
from personalizador.forms.directorioforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarDirectorio(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_directorio"

	model = Directorio
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-directorios")


@method_decorator(login_required, name="dispatch")
class CrearDirectorio(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_directorio"

	model = Directorio
	template_name = "directorio/crear-directorio.html"
	form_class = DirectorioForm
	success_url = reverse_lazy("personalizador:crear-directorio")
	popup_form_partial = "partials/directorio-form-partial.html"

	title = "Crear Directorio"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateDirectorio(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_directorio"

	model = Directorio
	template_name = "directorio/update-directorio.html"
	form_class = DirectorioForm
	success_url = reverse_lazy("personalizador:lista-directorios")

@login_required
@permission_required('personalizador.view_directorio', raise_exception=True)
def PaginaListaDirectorios(request):
	template_name = "Lista-directorios.html"

	return render(request, template_name, {})
