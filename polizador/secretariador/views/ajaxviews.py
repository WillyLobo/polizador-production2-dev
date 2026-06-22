from secretariador.models import *
from secretariador.forms import *
from personalizador.models import Agente
from django.db import models
from django_select2 import forms as s2forms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

@login_required
@permission_required("secretariador.add_solicitud", login_url="/")
def get_agentes(request):
    q = request.GET.get("q")
    agentes = Agente.objects.filter(agente_nombreyapellido__icontains=q).values("id", text=models.F("agente_nombreyapellido"))
    return JsonResponse({'results':list(agentes)},safe=False)

@login_required
@permission_required("secretariador.add_solicitud", login_url="/")
def check_resolucion(request):
    # Usage: $HOST/viaticos/ajax/check_resolucion/?instrumentolegalresoluciones_numero=1000&instrumentolegalresoluciones_ano=2025
    numero = request.POST.get("instrumentolegalresoluciones_numero")
    ano = request.POST.get("instrumentolegalresoluciones_ano")
    resolucion = InstrumentosLegalesResoluciones.objects.filter(instrumentolegalresoluciones_numero__icontains=numero, instrumentolegalresoluciones_ano=ano).exists()
    if resolucion:
        return JsonResponse({'results':True})
    else:
        return JsonResponse({'results':False})

class LocalidadMultipleWidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "carga.obra_nombre__icontains",
        "carga.obra_empresa__empresa_nombre__icontains",
        "carga.obra_convenio__icontains",
    ]

class ResolucionWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "instrumentolegalresoluciones_str__icontains",
        "instrumentolegalresoluciones_descripcion__icontains",
    ]

class SolicitudWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "solicitud_actuacion__icontains",
    ]

class ComisionadoWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "agente_nombres__icontains",
        "agente_apellidos__icontains",
    ]

class VehiculoWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "vehiculo_modelo__icontains",
        "vehiculo_patente__icontains",
    ]

class DecretoWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
    search_fields = [
        "montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_str__icontains",
    ]