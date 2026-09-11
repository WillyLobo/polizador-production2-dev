from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from carga.models import Poliza, Poliza_Movimiento
from carga.forms.polizaforms import *
from core.mixins import DeleteRelatedObjectsMixin, UserKwargsMixin, UserFormsetKwargsMixin
from core.mixins import FormsetViewMixin
from personalizador.models import Agente


def _firmante_organigrama(agente):
	"""Cargo y unidad de un Agente segun el organigrama: su denominacion_cargo y la
	oficina (o designacion temporal, cargo_interno, si tiene una) a la que pertenece."""
	if not agente:
		return None

	oficina = agente.cargo_interno or agente.oficina
	cargo = agente.denominacion_cargo.denominacion if agente.denominacion_cargo_id else ""
	if not oficina:
		return {"agente": agente, "cargo": cargo, "unidad": None, "unidad_padre": None}

	unidad = oficina.cargo_departamento or oficina.cargo_direccion or oficina.cargo_gerencia or oficina.cargo_directorio
	unidad_padre = oficina.cargo_gerencia if oficina.cargo_gerencia and oficina.cargo_gerencia != unidad else None
	return {
		"agente": agente,
		"cargo": cargo,
		"unidad": str(unidad) if unidad else None,
		"unidad_padre": unidad_padre.gerencia_nombre if unidad_padre else None,
	}

@method_decorator(login_required, name="dispatch")
class EliminarPoliza(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "carga.delete_poliza"

	model = Poliza
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-polizas")


@method_decorator(login_required, name="dispatch")
class CrearPoliza(PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "carga.add_poliza"
	formset_name = PolizaMovimientoFormset
	view_type = "create"

	model = Poliza
	template_name = "poliza/crear-poliza.html"
	form_class = PolizaForm
	success_url = reverse_lazy("carga:crear-poliza")

	title = "Crear Póliza"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

@method_decorator(login_required, name="dispatch")
class UpdatePoliza(PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "carga.change_poliza"
	formset_name = PolizaMovimientoFormset
	view_type = "update"

	model = Poliza
	template_name = "poliza/update-poliza.html"
	form_class = PolizaForm
	success_url = reverse_lazy("carga:lista-polizas")

@method_decorator(login_required, name="dispatch")
class CrearPolizaMovimiento(PermissionRequiredMixin, UserKwargsMixin, generic.CreateView):
	permission_required = "carga.add_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "poliza/crear-poliza-movimiento.html"
	form_class = PolizaMovimientoForm

	title = "Registrar Movimiento de Póliza"

	def get_title(self):
		return self.title

	def get_initial(self):
		initial = super().get_initial()
		poliza_id = self.request.GET.get("poliza")
		if poliza_id:
			initial["poliza_movimiento_numero"] = poliza_id
		return initial

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

	def get_success_url(self):
		return reverse("carga:estado-poliza", kwargs={"pk": self.object.poliza_movimiento_numero_id})


@method_decorator(login_required, name="dispatch")
class UpdatePolizaMovimiento(PermissionRequiredMixin, UserKwargsMixin, generic.UpdateView):
	permission_required = "carga.change_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "poliza/update-poliza-movimiento.html"
	form_class = PolizaMovimientoForm

	def get_success_url(self):
		return reverse("carga:estado-poliza", kwargs={"pk": self.object.poliza_movimiento_numero_id})


@method_decorator(login_required, name="dispatch")
class EliminarPolizaMovimiento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "carga.delete_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "generic/confirm_delete.html"

@method_decorator(login_required, name="dispatch")
class EstadoPoliza(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_poliza"

	model = Poliza
	template_name = "poliza/estado-poliza.html"

	# def get(self, request, *args, **kwargs):
	# 	poliza = request.session.get('poliza', 0)
	# 	request.session['num_visits'] = num_visits + 1
	# 	return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		self.object = self.get_object()
		poliza = models.Poliza.objects.get(id=self.object.id)
		poliza_id = str(poliza.id)
		self.request.session["poliza_id"] = poliza_id
		return context

@method_decorator(login_required, name="dispatch")
class ImprimirPolizaMovimiento(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "poliza/imprimir-poliza.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		agente = Agente.objects.filter(agente_usuario=self.request.user).first()
		if not agente:
			# Todavia no todos los CustomUser tienen su Agente vinculado via
			# agente_usuario: como respaldo, se lo ubica por nombre y apellido.
			nombre = f"{self.request.user.first_name} {self.request.user.last_name}".strip()
			if nombre:
				agente = Agente.objects.filter(agente_nombreyapellido__iexact=nombre).first()
		context["firmante"] = _firmante_organigrama(agente)
		return context

@login_required
@permission_required("carga.view_poliza", raise_exception=True)
def PaginaListaPolizas(request):
	template_name = "Lista-polizas.html"

	return render(request, template_name, {})

