from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from personalizador.models import CorteLicencia, LicenciaPermiso
from personalizador.forms.cortelicenciaforms import CorteLicenciaForm
from core.mixins import DeleteRelatedObjectsMixin

@method_decorator(login_required, name="dispatch")
class CrearCorteLicencia(PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_cortelicencia"

	model = CorteLicencia
	template_name = "cortelicencia/crear-cortelicencia.html"
	form_class = CorteLicenciaForm

	def get_licencia(self):
		return get_object_or_404(LicenciaPermiso, pk=self.kwargs["licenciapermiso_pk"])

	def get_initial(self):
		initial = super().get_initial()
		licencia = self.get_licencia()
		initial["cortelicencia_licencia"] = licencia
		initial["cortelicencia_fecha_vencimiento"] = date(licencia.licenciapermiso_fecha_desde.year + 1, 4, 30)
		return initial

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["licencia"] = self.get_licencia()
		context["title"] = "Registrar Corte de Licencia"
		return context

	def get_success_url(self):
		return reverse_lazy("personalizador:ver-licenciapermiso", kwargs={"pk": self.object.cortelicencia_licencia_id})


@method_decorator(login_required, name="dispatch")
class UpdateCorteLicencia(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_cortelicencia"

	model = CorteLicencia
	template_name = "cortelicencia/update-cortelicencia.html"
	form_class = CorteLicenciaForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["licencia"] = self.object.cortelicencia_licencia
		context["title"] = "Editar Corte de Licencia"
		return context

	def get_success_url(self):
		return reverse_lazy("personalizador:ver-licenciapermiso", kwargs={"pk": self.object.cortelicencia_licencia_id})


@method_decorator(login_required, name="dispatch")
class EliminarCorteLicencia(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_cortelicencia"

	model = CorteLicencia
	template_name = "generic/confirm_delete.html"

	def get_success_url(self):
		return reverse_lazy("personalizador:ver-licenciapermiso", kwargs={"pk": self.object.cortelicencia_licencia_id})
