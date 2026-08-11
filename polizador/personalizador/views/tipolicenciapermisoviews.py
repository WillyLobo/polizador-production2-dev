from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import TipoLicenciaPermiso
from personalizador.forms.tipolicenciapermisoforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarTipoLicenciaPermiso(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_tipolicenciapermiso"

	model = TipoLicenciaPermiso
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-tipolicenciapermisos")


@method_decorator(login_required, name="dispatch")
class CrearTipoLicenciaPermiso(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_tipolicenciapermiso"

	model = TipoLicenciaPermiso
	template_name = "tipolicenciapermiso/crear-tipolicenciapermiso.html"
	form_class = TipoLicenciaPermisoForm
	success_url = reverse_lazy("personalizador:lista-tipolicenciapermisos")
	popup_form_partial = "partials/tipolicenciapermiso-form-partial.html"

	title = "Nuevo Tipo de Licencia/Permiso"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateTipoLicenciaPermiso(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_tipolicenciapermiso"

	model = TipoLicenciaPermiso
	template_name = "tipolicenciapermiso/update-tipolicenciapermiso.html"
	form_class = TipoLicenciaPermisoForm
	success_url = reverse_lazy("personalizador:lista-tipolicenciapermisos")

@login_required
@permission_required('personalizador.view_tipolicenciapermiso', raise_exception=True)
def PaginaListaTipoLicenciaPermisos(request):
	template_name = "Lista-tipolicenciapermisos.html"

	return render(request, template_name, {})
