from secretariador.models import *
from secretariador.forms import *
from django_select2 import forms as s2forms
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse

@login_required
@permission_required("secretariador.add_solicitud", login_url="/")
def get_agentes(request):
        q = request.GET.get("q")
        agentes = Comisionado.objects.filter(comisionado_nombreyapellido__icontains=q).values("id", text=models.F("comisionado_nombreyapellido"))
        return JsonResponse({'results':list(agentes)},safe=False)

class LocalidadMultipleWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "carga.obra_nombre__icontains",
        "carga.obra_empresa__empresa_nombre__icontains",
        "carga.obra_convenio__icontains",
    ]

class ResolucionWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "instrumentolegalresoluciones_str__icontains",
        "instrumentolegalresoluciones_descripcion__icontains",
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
        "vehiculo_modelo__icontains",
        "vehiculo_patente__icontains",
    ]

class DecretoWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_str__icontains",
    ]