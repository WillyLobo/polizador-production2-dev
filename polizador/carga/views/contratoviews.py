from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from carga.models import Contrato, ContratoMonto
from carga.forms.contratoforms import *
from carga.views.generics import get_deleted_objects
from secretariador.forms.mixins import FormsetViewMixin

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
class EliminarContrato(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_contrato"

	model = Contrato
	template_name = "generic/confirm_delete.html"

	def get_success_url(self):
		return reverse("carga:estado-obra", kwargs={"pk": self.object.contrato_obra_id})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

	def form_valid(self, form):
		try:
			return super().form_valid(form)
		except ProtectedError:
			messages.error(
				self.request,
				"No se puede eliminar el contrato porque tiene relaciones protegidas asociadas.",
			)
			return redirect(self.get_success_url())