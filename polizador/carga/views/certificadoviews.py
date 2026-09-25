from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from carga.certificacion import (
	aplicar_descuento_anticipo,
	calcular_monto_anticipo,
	calcular_monto_hecho_consumado,
	construir_certificados_desde_foja,
	generar_certificados_desde_foja,
	siguiente_numero,
)
from carga.certificado_contexto import _certificado_detalle_context
from carga.ley27397 import Ley27397Error
from carga.models import Certificado, FojaDeMedicion
from carga.forms.certificadoforms import *
from core.mixins import DeleteRelatedObjectsMixin


@method_decorator(login_required, name="dispatch")
class EliminarCertificado(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "carga.delete_certificado"

	model = Certificado
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-certificados")


@method_decorator(login_required, name="dispatch")
class CrearCertificado(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_certificado"

	model = Certificado
	template_name = "certificado/crear-certificado.html"
	form_class = CertificadoForm
	success_url = reverse_lazy("carga:crear-certificado")
	
	title = "Crear Certificado"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

	def get_initial(self):
		initial = super().get_initial()
		foja_id = self.request.GET.get("foja")
		if foja_id:
			foja = FojaDeMedicion.objects.filter(pk=foja_id).first()
			if foja:
				initial["certificado_foja"] = foja.pk
				initial["certificado_obra"] = foja.foja_rubro.rubro_plan.trabajos_obra_id
				initial["certificado_mes_pct"] = foja.foja_pct_avance_mes()
				initial["certificado_acum_pct"] = foja.foja_pct_acumulado()
		return initial

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.certificado_fecha_carga = timezone.now() if self.object.certificado_fecha_carga_legacy == False else self.object.certificado_fecha
		self.object.save()
		return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class GenerarCertificadosDesdeFoja(PermissionRequiredMixin, generic.View):
	permission_required = "carga.add_certificado"
	template_name = "certificado/generar-certificados-foja.html"

	def get(self, request, pk):
		foja = get_object_or_404(FojaDeMedicion, pk=pk)
		form = GenerarCertificadosDesdeFojaForm()
		return render(request, self.template_name, {"foja": foja, "form": form, "preview": False})

	def post(self, request, pk):
		foja = get_object_or_404(FojaDeMedicion, pk=pk)
		form = GenerarCertificadosDesdeFojaForm(request.POST)
		context = {"foja": foja, "form": form, "preview": False}
		if not form.is_valid():
			return render(request, self.template_name, context)

		expediente = form.cleaned_data["certificado_expediente"]
		fecha = form.cleaned_data["certificado_fecha"]

		try:
			if "confirmar" in request.POST:
				certificados = generar_certificados_desde_foja(foja, expediente, fecha)
				messages.success(request, f"Se generaron {len(certificados)} certificado(s) a partir de la Foja N°{foja.foja_numero}.")
				return redirect(reverse("carga:estado-obra", kwargs={"pk": foja.foja_rubro.rubro_plan.trabajos_obra_id}))
			certificados = construir_certificados_desde_foja(foja, expediente, fecha)
		except ValidationError as e:
			form.add_error(None, e)
			return render(request, self.template_name, context)
		except Ley27397Error as e:
			form.add_error(None, str(e))
			return render(request, self.template_name, context)

		filas = [
			{
				"certificado": certificado,
				"monto_cobrar_pesos": (
					certificado.certificado_monto_pesos
					- (certificado.certificado_devolucion_monto or 0)
					- (certificado.certificado_descuento_anticipo_pesos or 0)
				),
			}
			for certificado in certificados
		]
		context.update({
			"preview": True,
			"filas": filas,
			"tipo_certificado": certificados[0].certificado_tipo if certificados else None,
		})
		return render(request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class CrearCertificadoAnticipo(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_certificado"

	model = Certificado
	template_name = "certificado/crear-certificado-anticipo.html"
	form_class = CertificadoAnticipoForm
	success_url = reverse_lazy("carga:lista-certificados")

	def get_form_kwargs(self):
		# El tipo tiene que estar en la instancia ANTES de que el ModelForm la valide
		# (Certificado.clean() decide qué campos zapatear según certificado_tipo, y
		# corre automáticamente dentro de form.is_valid()/_post_clean, antes de que
		# form_valid() llegue a ejecutarse).
		kwargs = super().get_form_kwargs()
		kwargs["instance"] = Certificado(certificado_tipo="ANTICIPO")
		return kwargs

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.certificado_rubro_anticipo = siguiente_numero(
			self.object.certificado_obra, self.object.certificado_financiamiento, "ANTICIPO"
		)
		try:
			calcular_monto_anticipo(self.object)
			self.object.certificado_fecha_carga = timezone.now()
			self.object.full_clean()
		except ValidationError as e:
			form.add_error(None, e)
			return self.form_invalid(form)
		self.object.save()
		return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class CrearCertificadoHechoConsumado(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_certificado"

	model = Certificado
	template_name = "certificado/crear-certificado-hechoconsumado.html"
	form_class = CertificadoHechoConsumadoForm
	success_url = reverse_lazy("carga:lista-certificados")

	def get_form_kwargs(self):
		# Ver comentario análogo en CrearCertificadoAnticipo.get_form_kwargs.
		kwargs = super().get_form_kwargs()
		kwargs["instance"] = Certificado(certificado_tipo="HECHO_CONSUMADO")
		return kwargs

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.certificado_rubro_obra = siguiente_numero(
			self.object.certificado_obra, self.object.certificado_financiamiento, "HECHO_CONSUMADO"
		)
		try:
			calcular_monto_hecho_consumado(self.object)
			aplicar_descuento_anticipo(self.object)
			self.object.certificado_fecha_carga = timezone.now()
			self.object.full_clean()
		except ValidationError as e:
			form.add_error(None, e)
			return self.form_invalid(form)
		self.object.save()
		return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class NuevoCertificadoMenu(PermissionRequiredMixin, generic.TemplateView):
	permission_required = "carga.add_certificado"
	template_name = "certificado/nuevo-certificado-menu.html"


@method_decorator(login_required, name="dispatch")
class UpdateCertificado(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_certificado"

	model = Certificado
	template_name = "certificado/update-certificado.html"
	form_class = CertificadoForm
	success_url = reverse_lazy("carga:lista-certificados")

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.save()
		return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class DetalleCertificado(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_certificado"

	model = Certificado
	template_name = "certificado/certificado.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx.update(_certificado_detalle_context(self.object))
		return ctx


@method_decorator(login_required, name="dispatch")
class ImprimirCertificado(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_certificado"

	model = Certificado
	template_name = "certificado/certificado.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx.update(_certificado_detalle_context(self.object))
		ctx["auto_print"] = True
		return ctx

@login_required
@permission_required('carga.view_certificado', raise_exception=True)
def PaginaListaCertificados(request):
	template_name = "Lista-certificados.html"

	return render(request, template_name, {})

