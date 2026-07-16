from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from carga.models import Contrato, ContratoMonto
from carga.forms.contratoforms import *
from core.mixins import DeleteRelatedObjectsMixin, FormsetViewMixin

@method_decorator(login_required, name="dispatch")
class CrearContrato(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "carga.add_certificado"
	formset_name = ContratoMontoFormset
	view_type = "create"
	
	model = Contrato
	template_name = "contrato/crear-contrato.html"
	form_class = ContratoForm
	success_url = reverse_lazy("carga:crear-contrato")
	title = "Crear Contrato"

	def get_title(self):
		return self.title

	def get_initial(self):
		initial = super().get_initial()
		obra_id = self.request.GET.get("obra")
		if obra_id:
			initial["contrato_obra"] = obra_id
		return initial

@method_decorator(login_required, name="dispatch")
class UpdateContrato(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "carga.add_certificado"
	formset_name = ContratoMontoFormset
	view_type = "update"
	
	model = Contrato
	template_name = "contrato/update-contrato.html"
	form_class = ContratoForm

	def get_success_url(self):
		return reverse("carga:estado-obra", kwargs={"pk": self.object.contrato_obra_id})

@method_decorator(login_required, name="dispatch")
class EliminarContrato(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "carga.delete_contrato"

	model = Contrato
	template_name = "generic/confirm_delete.html"

	def get_success_url(self):
		return reverse("carga:estado-obra", kwargs={"pk": self.object.contrato_obra_id})