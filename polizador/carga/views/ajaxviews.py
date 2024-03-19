from carga.models import *
from carga.forms import *
from django_select2 import forms as s2forms

class obrawidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "obra_nombre__icontains",
        "obra_empresa__empresa_nombre__icontains",
        "obra_convenio__icontains",
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

class departamentomultiplewidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "departamento_nombre__icontains",
    ]

class localidadmultiplewidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "localidad_nombre__icontains",
    ]

class municipiomultiplewidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "municipio_nombre__icontains",
    ]

class contratomontowidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "contratomonto_contrato__icontains",
    ]