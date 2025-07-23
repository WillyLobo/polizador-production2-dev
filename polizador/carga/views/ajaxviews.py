from carga.models import *
from carga.forms import *
from django_select2 import forms as s2forms

class obrawidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "obra_nombre__icontains",
        "obra_empresa__empresa_nombre__icontains",
        "obra_convenio__icontains",
    ]

class conjuntowidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "conjunto_nombre__icontains",
    ]

class programawidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "programa_nombre__icontains",
    ]

class agentemultiplewidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "agente_nombre__icontains",
    ]

class agentewidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "agente_nombre__icontains",
    ]

class aseguradorawidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "aseguradora_nombre__icontains",
    ]

class areawidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "area_nombre__icontains",
    ]

class receptorwidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "receptor_nombre__icontains",
    ]

class polizawidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "poliza_numero__icontains",
        "poliza_expediente__icontains",
        "poliza_aseguradora__aseguradora_nombre__icontains",
        "poliza_tomador__empresa_nombre__icontains",
        "poliza_obra__obra_nombre__icontains",
    ]

class empresawidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "empresa_nombre__icontains",
    ]

class obramultiplewidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "obra_nombre__icontains",
        "obra_empresa__empresa_nombre__icontains",
        "obra_convenio__icontains",
    ]

class provinciawidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "provincia_nombre__icontains",
    ]

class departamentomultiplewidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "departamento_nombre__icontains",
    ]

class departamentowidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "departamento_nombre__icontains",
    ]

class localidadmultiplewidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "localidad_nombre__icontains",
    ]

class localidadwidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "localidad_nombre__icontains",
    ]

class municipiomultiplewidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "municipio_nombre__icontains",
    ]

class municipiowidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "municipio_nombre__icontains",
    ]

class contratomontowidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "contratomonto_contrato__icontains",
    ]