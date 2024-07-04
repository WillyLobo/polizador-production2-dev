from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from secretariador.models import *
from django.db.models import Q, FilteredRelation, Subquery, OuterRef, Sum, F, Min, Max
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from datetime import datetime, timedelta

@method_decorator(login_required, name="dispatch")
class CrearReporteViaticosPorAgente(PermissionRequiredMixin, generic.ListView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "secretariador.view_solicitudes"

    model = Comisionado
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteviaticosporagente.html"
	
    def get_queryset(self):
        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial,fecha_final])
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%d/%m/%Y")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%d/%m/%Y")
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final])

        agentes = Comisionado.objects.all()
        queryset = {}
        final_queryset = {}
        for agente in agentes:
            # Cantidad de días por agente
            agentes_list = solicitudes.filter(comisionadosolicitud_nombre=agente)
            solicitudes_annotated = agentes_list.annotate(
                dias=F("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"), 
                viatico=F("comisionadosolicitud_viatico_computado"),
                pasaje=F("comisionadosolicitud_pasaje"), 
                gastos=F("comisionadosolicitud_gastos"), 
                combustible=F("comisionadosolicitud_combustible"),
                valor_viatico=F("comisionadosolicitud_viatico_total")
                ).aggregate(
                    cantidad_de_dias=Sum("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"), 
                    viatico=Sum("comisionadosolicitud_viatico_computado"),
                    pasaje=Sum("comisionadosolicitud_pasaje"), 
                    gastos=Sum("comisionadosolicitud_gastos"), 
                    combustible=Sum("comisionadosolicitud_combustible"),
                    valor_viatico=Sum("comisionadosolicitud_viatico_total")
                )
            
            if solicitudes_annotated["cantidad_de_dias"] is not None:
                queryset.update({
                        agente.comisionado_nombreyapellido: {
                            "cantidad_de_dias": solicitudes_annotated["cantidad_de_dias"].days,
                            "viatico":          solicitudes_annotated["viatico"],
                            "pasaje":           solicitudes_annotated["pasaje"],
                            "gastos":           solicitudes_annotated["gastos"],
                            "combustible":      solicitudes_annotated["combustible"],
                            "valor_viatico":    solicitudes_annotated["valor_viatico"]
                        }
                    })
        final_queryset.update({
            "comisionados": queryset,
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final
        })
        return final_queryset

@method_decorator(login_required, name="dispatch")
class CrearReporteViaticosporArea(PermissionRequiredMixin, generic.ListView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "secretariador.view_solicitudes"

    model = Comisionado
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteviaticosporarea.html"

    def get_queryset(self):

        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial,fecha_final])
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%d/%m/%Y")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%d/%m/%Y")
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final])
        
        agentes = Comisionado.objects.all()
        queryset = {}
        final_queryset = {}
        for agente in agentes:
            agentes_list = solicitudes.filter(comisionadosolicitud_foreign__solicitud_solicitante=agente)
            
            solicitudes_annotated = agentes_list.annotate(
                dias=F("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"), 
                viatico=F("comisionadosolicitud_viatico_computado"),
                pasaje=F("comisionadosolicitud_pasaje"), 
                gastos=F("comisionadosolicitud_gastos"), 
                combustible=F("comisionadosolicitud_combustible"),
                valor_viatico=F("comisionadosolicitud_viatico_total"),
                dia_min=F("comisionadosolicitud_foreign__solicitud_fecha_desde"),
                dia_max=F("comisionadosolicitud_foreign__solicitud_fecha_hasta")
                ).aggregate(
                    cantidad_de_dias=Sum("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"), 
                    viatico=Sum("comisionadosolicitud_viatico_computado"),
                    pasaje=Sum("comisionadosolicitud_pasaje"), 
                    gastos=Sum("comisionadosolicitud_gastos"), 
                    combustible=Sum("comisionadosolicitud_combustible"),
                    valor_viatico=Sum("comisionadosolicitud_viatico_total")
                )
            
            if solicitudes_annotated["cantidad_de_dias"] is not None:
                queryset.update({
                        agente.comisionado_nombreyapellido: {
                            "cantidad_de_dias": solicitudes_annotated["cantidad_de_dias"].days,
                            "viatico":          solicitudes_annotated["viatico"],
                            "pasaje":           solicitudes_annotated["pasaje"],
                            "gastos":           solicitudes_annotated["gastos"],
                            "combustible":      solicitudes_annotated["combustible"],
                            "valor_viatico":    solicitudes_annotated["valor_viatico"]
                        }
                    })
        final_queryset.update({
            "comisionados": queryset,
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final
        })
        return final_queryset