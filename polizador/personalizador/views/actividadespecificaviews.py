from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import ActividadEspecifica
from personalizador.forms.actividadespecificaforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarActividadEspecifica(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_actividadespecifica"

	model = ActividadEspecifica
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-actividadespecificas")


@method_decorator(login_required, name="dispatch")
class CrearActividadEspecifica(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_actividadespecifica"

	model = ActividadEspecifica
	template_name = "actividadespecifica/crear-actividadespecifica.html"
	form_class = ActividadEspecificaForm
	success_url = reverse_lazy("personalizador:crear-actividadespecifica")
	popup_form_partial = "partials/actividadespecifica-form-partial.html"

	title = "Crear Actividad Específica"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateActividadEspecifica(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_actividadespecifica"

	model = ActividadEspecifica
	template_name = "actividadespecifica/update-actividadespecifica.html"
	form_class = ActividadEspecificaForm
	success_url = reverse_lazy("personalizador:lista-actividadespecificas")

@login_required
@permission_required('personalizador.view_actividadespecifica', raise_exception=True)
def PaginaListaActividadEspecificas(request):
	template_name = "Lista-actividadespecificas.html"

	return render(request, template_name, {})
