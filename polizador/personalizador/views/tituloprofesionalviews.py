from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import TituloProfesional
from personalizador.forms.tituloprofesionalforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarTituloProfesional(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_tituloprofesional"

	model = TituloProfesional
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-tituloprofesionales")


@method_decorator(login_required, name="dispatch")
class CrearTituloProfesional(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_tituloprofesional"

	model = TituloProfesional
	template_name = "tituloprofesional/crear-tituloprofesional.html"
	form_class = TituloProfesionalForm
	success_url = reverse_lazy("personalizador:crear-tituloprofesional")
	popup_form_partial = "partials/tituloprofesional-form-partial.html"

	title = "Crear Título Profesional"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateTituloProfesional(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_tituloprofesional"

	model = TituloProfesional
	template_name = "tituloprofesional/update-tituloprofesional.html"
	form_class = TituloProfesionalForm
	success_url = reverse_lazy("personalizador:lista-tituloprofesionales")

@login_required
@permission_required('personalizador.view_tituloprofesional', raise_exception=True)
def PaginaListaTituloProfesionales(request):
	template_name = "Lista-tituloprofesionales.html"

	return render(request, template_name, {})
