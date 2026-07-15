from carga.models import *
from carga.forms import *
from django_select2 import forms as s2forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.html import format_html

class AddRelatedWidgetMixin:
    """Agrega un boton "+" al lado del select que abre (en un modal) el formulario de
    alta del modelo relacionado y, al guardar, inserta el objeto creado como opcion
    seleccionada. Requiere `add_related_url_name` (nombre de URL reversible del
    CreateView correspondiente, que debe usar PopupCreateMixin).

    `add_related_allowed` puede setearlo AddRelatedPermissionMixin (carga/forms/mixins.py)
    para ocultar el boton segun el permiso add_<modelo> del usuario actual.
    """
    add_related_url_name = None
    add_related_allowed = True

    def render(self, name, value, attrs=None, renderer=None):
        widget_html = super().render(name, value, attrs, renderer)
        if not self.add_related_url_name or not self.add_related_allowed:
            return widget_html
        select_id = (attrs or {}).get("id") or f"id_{name}"
        create_url = reverse(self.add_related_url_name)
        button_html = format_html(
            '<button type="button" class="btn btn-outline-secondary select2-add-related" '
            'data-select-id="{}" data-create-url="{}" title="Agregar nuevo">'
            '<i class="bi bi-plus-lg text-success"></i></button>',
            select_id, create_url,
        )
        return format_html('<div class="input-group select2-with-add">{}{}</div>', widget_html, button_html)

class SmallCatalogWidgetMixin:
    """Widgets over catalogs with few rows: show the first results on open, without typing."""
    max_results = 10

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-minimum-input-length"] = 0
        return attrs

class PlanDependentWidgetMixin:
    """Widgets in PlanDeTrabajosRubroForm: scope AJAX results to the obra/contrato of the
    plan currently chosen in the sibling 'rubro_plan' field, and show them on open."""
    dependent_fields = {"rubro_plan": "rubro_plan_actual"}
    max_results = 10

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-minimum-input-length"] = 0
        return attrs

    def _plan_actual(self, dependent_fields):
        plan_id = dependent_fields.pop("rubro_plan_actual", None)
        return PlanDeTrabajos.objects.filter(pk=plan_id).first() if plan_id else None

class obrawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "obra_nombre__icontains",
        "obra_empresa__empresa_nombre__icontains",
        "obra_convenio__icontains",
    ]

class conjuntowidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "carga:crear-conjunto"
    search_fields = [
        "conjunto_nombre__icontains",
    ]

class planwidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "trabajos_obra__obra_nombre__icontains",
    ]

class rubrowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "rubro_nombre__icontains",
        "rubro_plan__trabajos_obra__obra_nombre__icontains",
    ]

class rubroanteriorwidget(PlanDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    """Candidatos a 'rubro anterior': rubros de la misma obra, de un plan distinto al actual."""
    search_fields = [
        "rubro_nombre__icontains",
        "rubro_plan__trabajos_obra__obra_nombre__icontains",
    ]

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        plan = self._plan_actual(dependent_fields)
        if plan:
            queryset = queryset.filter(
                rubro_plan__trabajos_obra_id=plan.trabajos_obra_id
            ).exclude(rubro_plan_id=plan.pk)
        return super().filter_queryset(request, term, queryset)

class programawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "carga:crear-programa"
    search_fields = [
        "programa_nombre__icontains",
    ]

class FojaRubroDependentWidgetMixin:
    """Widgets en FojaDeMedicionForm: escopean resultados AJAX a la Obra del `foja_rubro`
    elegido en el form, y muestran los primeros resultados al abrir sin escribir."""
    dependent_fields = {"foja_rubro": "foja_rubro_actual"}
    max_results = 10

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-minimum-input-length"] = 0
        return attrs

    def _obra_id_actual(self, dependent_fields):
        rubro_id = dependent_fields.pop("foja_rubro_actual", None)
        if not rubro_id:
            return None
        return PlanDeTrabajosRubro.objects.filter(pk=rubro_id).values_list(
            "rubro_plan__trabajos_obra_id", flat=True
        ).first()

class certificadolegacywidget(FojaRubroDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    """Candidatos a vincular en una Foja legacy: Certificados de la Obra del rubro elegido
    que todavía no están asociados a ninguna Foja."""
    search_fields = [
        "certificado_expediente__icontains",
        "certificado_obra__obra_nombre__icontains",
    ]

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        obra_id = self._obra_id_actual(dependent_fields)
        queryset = queryset.filter(certificado_obra_id=obra_id, certificado_foja__isnull=True) if obra_id else queryset.none()
        return super().filter_queryset(request, term, queryset)

class agentemultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "agente_nombres__icontains",
        "agente_apellidos__icontains",
    ]

class agentewidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "agente_nombres__icontains",
        "agente_apellidos__icontains",
    ]

class aseguradorawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "carga:crear-aseguradora"
    search_fields = [
        "aseguradora_nombre__icontains",
    ]

class areawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "carga:crear-area"
    search_fields = [
        "area_nombre__icontains",
    ]

class receptorwidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "carga:crear-receptor"
    search_fields = [
        "receptor_nombre__icontains",
    ]

class polizawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "poliza_numero__icontains",
        "poliza_expediente__icontains",
        "poliza_aseguradora__aseguradora_nombre__icontains",
        "poliza_tomador__empresa_nombre__icontains",
        "poliza_obra__obra_nombre__icontains",
    ]

class empresawidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "carga:crear-empresa"
    search_fields = [
        "empresa_nombre__icontains",
    ]

class obramultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "obra_nombre__icontains",
        "obra_empresa__empresa_nombre__icontains",
        "obra_convenio__icontains",
    ]

class provinciawidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "provincia_nombre__icontains",
    ]

class departamentomultiplewidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "departamento_nombre__icontains",
    ]

class departamentowidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "departamento_nombre__icontains",
    ]

class localidadmultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "localidad_nombre__icontains",
    ]

class localidadwidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "localidad_nombre__icontains",
    ]

class municipiomultiplewidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "municipio_nombre__icontains",
    ]

class municipiowidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "municipio_nombre__icontains",
    ]

class contratomontowidget(PlanDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    """Montos del contrato vinculado al plan actual (o de los contratos de su obra, si no tiene uno)."""
    search_fields = [
        "contratomonto_contrato__contrato_descripcion__icontains",
        "contratomonto_contrato__contrato_obra__obra_nombre__icontains",
    ]

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        plan = self._plan_actual(dependent_fields)
        if plan:
            if plan.trabajos_contrato_id:
                queryset = queryset.filter(contratomonto_contrato_id=plan.trabajos_contrato_id)
            else:
                queryset = queryset.filter(contratomonto_contrato__contrato_obra_id=plan.trabajos_obra_id)
        return super().filter_queryset(request, term, queryset)

class contratowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "contrato_descripcion__icontains",
        "contrato_obra__obra_nombre__icontains",
    ]