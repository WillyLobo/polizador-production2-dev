from carga.models import *
from carga.forms import *
from django_select2 import forms as s2forms
from django.contrib.auth.mixins import LoginRequiredMixin

class obrawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "obra_nombre__icontains",
        "obra_empresa__empresa_nombre__icontains",
        "obra_convenio__icontains",
    ]

class conjuntowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
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

class programawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "programa_nombre__icontains",
    ]

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

class aseguradorawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "aseguradora_nombre__icontains",
    ]

class areawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "area_nombre__icontains",
    ]

class receptorwidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
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

class empresawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "empresa_nombre__icontains",
    ]

class obramultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "obra_nombre__icontains",
        "obra_empresa__empresa_nombre__icontains",
        "obra_convenio__icontains",
    ]

class provinciawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "provincia_nombre__icontains",
    ]

class departamentomultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "departamento_nombre__icontains",
    ]

class departamentowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
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

class municipiomultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "municipio_nombre__icontains",
    ]

class municipiowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "municipio_nombre__icontains",
    ]

class contratomontowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "contratomonto_contrato__icontains",
    ]