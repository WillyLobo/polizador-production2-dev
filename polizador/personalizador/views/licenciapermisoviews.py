from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from personalizador.models import LicenciaPermiso, Agente, CorteLicencia
from personalizador.forms.licenciapermisoforms import LicenciaPermisoForm, DevolucionHorasPermisoFormset
from personalizador.licencias import (
	resumen_agente, saldos_pendientes_agente,
	LICENCIA_ANUAL_ORDINARIA_NOMBRE, LICENCIA_ANUAL_INVIERNO_NOMBRE,
)
from core.mixins import DeleteRelatedObjectsMixin, FormsetViewMixin

@method_decorator(login_required, name="dispatch")
class EliminarLicenciaPermiso(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_licenciapermiso"

	model = LicenciaPermiso
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-licenciapermisos")


@method_decorator(login_required, name="dispatch")
class CrearLicenciaPermiso(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "personalizador.add_licenciapermiso"
	formset_name = DevolucionHorasPermisoFormset
	view_type = "create"

	model = LicenciaPermiso
	template_name = "licenciapermiso/crear-licenciapermiso.html"
	form_class = LicenciaPermisoForm
	success_url = reverse_lazy("personalizador:lista-licenciapermisos")

	title = "Registrar Licencia/Permiso"

	def get_title(self):
		return self.title

	def get_initial(self):
		initial = super().get_initial()
		corte_id = self.request.GET.get("saldo_de_corte")
		if corte_id:
			corte = get_object_or_404(CorteLicencia, pk=corte_id)
			licencia_original = corte.cortelicencia_licencia
			initial["licenciapermiso_saldo_de_corte"] = corte
			initial["licenciapermiso_agente"] = licencia_original.licenciapermiso_agente
			initial["licenciapermiso_tipo"] = licencia_original.licenciapermiso_tipo
		return initial

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateLicenciaPermiso(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "personalizador.change_licenciapermiso"
	formset_name = DevolucionHorasPermisoFormset
	view_type = "update"

	model = LicenciaPermiso
	template_name = "licenciapermiso/update-licenciapermiso.html"
	form_class = LicenciaPermisoForm
	success_url = reverse_lazy("personalizador:lista-licenciapermisos")


@method_decorator(login_required, name="dispatch")
class VerLicenciaPermiso(PermissionRequiredMixin, generic.DetailView):
	permission_required = "personalizador.view_licenciapermiso"

	model = LicenciaPermiso
	template_name = "licenciapermiso/ver-licenciapermiso.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["es_licencia_anual"] = self.object.licenciapermiso_tipo.tipolicenciapermiso_nombre in (
			LICENCIA_ANUAL_ORDINARIA_NOMBRE, LICENCIA_ANUAL_INVIERNO_NOMBRE,
		)
		return context


@login_required
@permission_required('personalizador.view_licenciapermiso', raise_exception=True)
def PaginaListaLicenciaPermisos(request):
	template_name = "Lista-licenciapermisos.html"

	return render(request, template_name, {})


@login_required
@permission_required('personalizador.view_licenciapermiso', raise_exception=True)
def ControlLicenciasAgente(request, pk):
	agente = get_object_or_404(Agente, pk=pk)
	try:
		anio = int(request.GET.get("anio", timezone.now().year))
	except (TypeError, ValueError):
		anio = timezone.now().year

	context = {
		"agente": agente,
		"anio": anio,
		"anios": range(timezone.now().year - 5, timezone.now().year + 1),
		"resumen": resumen_agente(agente, anio),
		"saldos_pendientes": saldos_pendientes_agente(agente),
	}
	return render(request, "licenciapermiso/control-licencias.html", context)
