from secretariador.models import *
from secretariador.forms import *
from django_select2 import forms as s2forms

# class obrawidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "obra_nombre__icontains",
#         "obra_empresa__empresa_nombre__icontains",
#         "obra_convenio__icontains",
#     ]

class LocalidadMultipleWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "carga.obra_nombre__icontains",
        "carga.obra_empresa__empresa_nombre__icontains",
        "carga.obra_convenio__icontains",
    ]

class ResolucionWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "instrumentolegalresoluciones_str__icontains",
    ]

class SolicitudWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "solicitud_actuacion__icontains",
    ]

class ComisionadoWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "comisionado_nombres__icontains",
        "comisionado_apellidos__icontains",
    ]

class VehiculoWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "vehiculo_str__icontains",
    ]