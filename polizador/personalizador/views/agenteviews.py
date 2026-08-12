from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import Agente
from personalizador.forms.agenteforms import *
from personalizador.licencias import resumen_agente, saldos_pendientes_agente
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarAgente(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_agente"

	model = Agente
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-agentes")


@method_decorator(login_required, name="dispatch")
class CrearAgente(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_agente"

	model = Agente
	template_name = "agente/crear-agente.html"
	form_class = AgenteForm
	success_url = reverse_lazy("personalizador:crear-agente")
	popup_form_partial = "partials/agente-form-partial.html"

	title = "Crear Agente"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateAgente(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_agente"

	model = Agente
	template_name = "agente/update-agente.html"
	form_class = AgenteForm
	success_url = reverse_lazy("personalizador:lista-agentes")


@method_decorator(login_required, name="dispatch")
class FichaAgente(PermissionRequiredMixin, generic.DetailView):
	permission_required = "personalizador.view_agente"

	model = Agente
	template_name = "agente/ficha-agente.html"

	def get_queryset(self):
		return Agente.objects.select_related(
			"sexo", "categoria", "denominacion_cargo", "apartado", "ceic", "grupo",
			"actividad_especifica", "domicilio_localidad", "domicilio_provincia",
			"agente_usuario",
			"oficina__cargo_directorio", "oficina__cargo_gerencia",
			"oficina__cargo_direccion", "oficina__cargo_departamento",
			"cargo_interno__cargo_directorio", "cargo_interno__cargo_gerencia",
			"cargo_interno__cargo_direccion", "cargo_interno__cargo_departamento",
		).prefetch_related(
			"titulo_profesional",
			"licenciapermiso_set__licenciapermiso_tipo",
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		anio = timezone.now().year
		context["anio"] = anio
		context["resumen"] = resumen_agente(self.object, anio)
		context["saldos_pendientes"] = saldos_pendientes_agente(self.object)
		context["licencias_recientes"] = self.object.licenciapermiso_set.all()[:10]
		return context


@login_required
@permission_required('personalizador.view_agente', raise_exception=True)
def PaginaListaAgentes(request):
	template_name = "Lista-agentes.html"

	return render(request, template_name, {})
