from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import PeriodoLicencia
from personalizador.forms.periodolicenciaforms import *
from core.mixins import DeleteRelatedObjectsMixin

@method_decorator(login_required, name="dispatch")
class EliminarPeriodoLicencia(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_periodolicencia"

	model = PeriodoLicencia
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-periodolicencias")


@method_decorator(login_required, name="dispatch")
class CrearPeriodoLicencia(PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_periodolicencia"

	model = PeriodoLicencia
	template_name = "periodolicencia/crear-periodolicencia.html"
	form_class = PeriodoLicenciaForm
	success_url = reverse_lazy("personalizador:lista-periodolicencias")

	def get_initial(self):
		initial = super().get_initial()
		categoria = self.request.GET.get("categoria")
		anio = self.request.GET.get("anio")
		if categoria:
			initial["periodolicencia_categoria"] = categoria
		if anio:
			initial["periodolicencia_anio"] = anio
		return initial


@method_decorator(login_required, name="dispatch")
class UpdatePeriodoLicencia(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_periodolicencia"

	model = PeriodoLicencia
	template_name = "periodolicencia/update-periodolicencia.html"
	form_class = PeriodoLicenciaForm
	success_url = reverse_lazy("personalizador:lista-periodolicencias")


@login_required
@permission_required("personalizador.view_periodolicencia", raise_exception=True)
def PaginaListaPeriodoLicencias(request):
	template_name = "Lista-periodolicencias.html"

	return render(request, template_name, {})
