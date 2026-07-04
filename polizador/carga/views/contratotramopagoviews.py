from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from carga.models import Contrato
from carga.forms.contratotramopagoforms import ContratoTramoPagoFormset


@method_decorator(login_required, name="dispatch")
class GestionarTramosContrato(PermissionRequiredMixin, generic.View):
	"""Carga/edita de una sola vez los Tramos de Pago de un Contrato marcado con
	certificación por etapas (ver Contrato.contrato_certificacion_por_etapas)."""

	permission_required = ("carga.add_contratotramopago", "carga.change_contratotramopago")
	template_name = "contratotramopago/gestionar-tramos.html"

	def has_permission(self):
		return any(self.request.user.has_perm(perm) for perm in self.get_permission_required())

	def get(self, request, pk):
		contrato = get_object_or_404(Contrato, pk=pk)
		formset = ContratoTramoPagoFormset(instance=contrato)
		return render(request, self.template_name, {"contrato": contrato, "formset": formset})

	def post(self, request, pk):
		contrato = get_object_or_404(Contrato, pk=pk)
		formset = ContratoTramoPagoFormset(request.POST, instance=contrato)
		if formset.is_valid():
			try:
				with transaction.atomic():
					formset.save()
			except ProtectedError:
				messages.error(
					request,
					"No se puede eliminar un tramo que ya tiene un Certificado de Etapa generado.",
				)
				return render(request, self.template_name, {"contrato": contrato, "formset": formset})
			return redirect(reverse("carga:update-contrato", kwargs={"pk": contrato.pk}))
		return render(request, self.template_name, {"contrato": contrato, "formset": formset})
