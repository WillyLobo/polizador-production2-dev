from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import BooleanField, Case, Q, Value, When
from django.utils.decorators import method_decorator
from django.views import generic

from personalizador.licencias import disponibles_agente, periodo_anual_vigente, tipo_anual_invierno
from personalizador.models import Agente, Oficina, PeriodoLicencia
from personalizador.views.ajaxviews import oficinawidget


class oficinareportewidget(oficinawidget):
	"""oficinawidget sin el boton "+": en un filtro de reporte no se crean oficinas."""
	add_related_url_name = None


class ReporteLicenciasPorOficinaForm(forms.Form):
	oficina = forms.ModelChoiceField(
		label="Oficina", queryset=Oficina.objects.all(),
		widget=oficinareportewidget(attrs={"class": "form-control customSelect2", "data-placeholder": "Buscar oficina"}),
	)
	anio = forms.TypedChoiceField(label="Período de Licencia Anual", coerce=int)
	incluir_dependientes = forms.BooleanField(
		label="Incluir oficinas dependientes", required=False,
		help_text="Ej. al elegir una Gerencia, incluye a los agentes de sus Direcciones y Departamentos.",
		widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
	)
	incluir_designados = forms.BooleanField(
		label="Incluir designados temporalmente", required=False,
		help_text="Agrega a los agentes con Designación Temporal en la oficina, aunque su oficina habitual sea otra.",
		widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		vigente = periodo_anual_vigente()
		anios = set(PeriodoLicencia.objects.filter(periodolicencia_categoria="LOR_ANUAL").values_list("periodolicencia_anio", flat=True))
		anios.add(vigente)
		self.fields["anio"].choices = [(a, str(a)) for a in sorted(anios, reverse=True)]
		self.fields["anio"].initial = vigente
		self.fields["anio"].widget.attrs["class"] = "form-select"


def filtro_oficina(oficina, incluir_dependientes, campo="oficina"):
	"""Q de los agentes cuyo `campo` (oficina habitual, o cargo_interno = Designación Temporal)
	es `oficina`; con incluir_dependientes, tambien las oficinas que cuelgan de su nivel mas
	especifico (Departamento > Direccion > Gerencia > Directorio)."""
	if not incluir_dependientes or oficina.cargo_departamento_id:
		return Q(**{campo: oficina})
	for nivel in ("cargo_direccion_id", "cargo_gerencia_id", "cargo_directorio_id"):
		if getattr(oficina, nivel):
			return Q(**{f"{campo}__{nivel}": getattr(oficina, nivel)})
	return Q(**{campo: oficina})


@method_decorator(login_required, name="dispatch")
class ReporteLicenciasPorOficina(PermissionRequiredMixin, generic.TemplateView):
	"""Agentes activos de una oficina con sus días de licencia disponibles: Licencia Anual
	Ordinaria y de Invierno del período elegido y saldos de cortes todavía vigentes."""
	permission_required = "personalizador.view_licenciapermiso"
	template_name = "reportes/reporte-licencias-por-oficina.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		form = ReporteLicenciasPorOficinaForm(self.request.GET or None)
		context["form"] = form
		if not form.is_bound or not form.is_valid():
			return context

		oficina = form.cleaned_data["oficina"]
		anio = form.cleaned_data["anio"]
		dependientes = form.cleaned_data["incluir_dependientes"]
		por_oficina = filtro_oficina(oficina, dependientes)
		filtro = por_oficina
		if form.cleaned_data["incluir_designados"]:
			filtro |= filtro_oficina(oficina, dependientes, campo="cargo_interno")
		tipo_anual, tipo_invierno = tipo_anual_invierno()
		agentes = Agente.objects.filter(filtro, activo=True).annotate(
			# Entra solo por la Designación Temporal (su oficina habitual es otra).
			designado=Case(When(por_oficina, then=Value(False)), default=Value(True), output_field=BooleanField()),
		).select_related(
			"oficina__cargo_directorio", "oficina__cargo_gerencia",
			"oficina__cargo_direccion", "oficina__cargo_departamento",
			"cargo_interno__cargo_directorio", "cargo_interno__cargo_gerencia",
			"cargo_interno__cargo_direccion", "cargo_interno__cargo_departamento",
		).order_by("agente_apellidos", "agente_nombres")
		filas = [
			{"agente": agente, **disponibles_agente(agente, anio, tipo_anual, tipo_invierno)}
			for agente in agentes
		]
		context.update({
			"oficina": oficina,
			"anio": anio,
			"filas": filas,
			"hay_invierno": tipo_invierno is not None,
			"varias_oficinas": len({fila["agente"].oficina_id for fila in filas}) > 1 or any(fila["agente"].designado for fila in filas),
		})
		return context
