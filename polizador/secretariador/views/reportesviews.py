from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from secretariador.models import *
from django.db.models import Q, FilteredRelation, Subquery, OuterRef, Sum, F
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
        mes_list = self.request.GET.getlist("mes")
        ano = self.request.GET.get("ano")
        agentes = Comisionado.objects.all()
        queryset = {}
        for agente in agentes:
            # Cantidad de días por agente
            if not mes_list and not ano:
                agentes_list = ComisionadoSolicitud.objects.all().filter(comisionadosolicitud_nombre=agente)
            elif not mes_list:
                agentes_list = ComisionadoSolicitud.objects.filter(
                comisionadosolicitud_foreign__solicitud_fecha_desde__year=ano).filter(comisionadosolicitud_nombre=agente)
            elif not ano:
                agentes_list = ComisionadoSolicitud.objects.filter(
                comisionadosolicitud_foreign__solicitud_fecha_desde__month__in=mes_list).filter(comisionadosolicitud_nombre=agente)
            elif not mes_list and not ano:
                agentes_list = ComisionadoSolicitud.objects.all().filter(comisionadosolicitud_nombre=agente)
            else:
                agentes_list = ComisionadoSolicitud.objects.filter(
                    comisionadosolicitud_foreign__solicitud_fecha_desde__year=ano, comisionadosolicitud_foreign__solicitud_fecha_desde__month__in=mes_list).filter(comisionadosolicitud_nombre=agente)
            
            dias = agentes_list.annotate(
                            cantidad_de_dias=Sum("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"))
            dias = dias.aggregate(cantidad_de_dias=Sum("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"))
            
            if dias["cantidad_de_dias"] is not None:
                agente_last = agentes_list.last()
                
                dias["valor_viaticos"] = agente_last.valor_viatico_dia() * dias["cantidad_de_dias"].days
                dias["combustible"] = agentes_list.aggregate(combustible=Sum("comisionadosolicitud_combustible"))["combustible"]
                dias["gastos"] = agentes_list.aggregate(gastos=Sum("comisionadosolicitud_gastos"))["gastos"]
                dias["pasajes"] = agentes_list.aggregate(pasajes=Sum("comisionadosolicitud_pasaje"))["pasajes"]
                dias["total"] = dias["valor_viaticos"] + dias["combustible"] + dias["gastos"] + dias["pasajes"]
                queryset.update({
                    agente.comisionado_nombreyapellido:dias
                    })

        return queryset

@method_decorator(login_required, name="dispatch")
class CrearReporteViaticosporArea(PermissionRequiredMixin, generic.ListView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "secretariador.view_solicitudes"

    model = Comisionado
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteviaticosporarea.html"

    def get_queryset(self):
        mes_list = self.request.GET.getlist("mes")
        ano = self.request.GET.get("ano")
        agentes = Comisionado.objects.all()
        queryset = {}
        for agente in agentes:
            if not mes_list and not ano:
                agentes_list = ComisionadoSolicitud.objects.all().filter(comisionadosolicitud_foreign__solicitud_solicitante=agente)
            elif not mes_list:
                agentes_list = ComisionadoSolicitud.objects.filter(
                comisionadosolicitud_foreign__solicitud_fecha_desde__year=ano).filter(comisionadosolicitud_foreign__solicitud_solicitante=agente)
            elif not ano:
                agentes_list = ComisionadoSolicitud.objects.filter(
                comisionadosolicitud_foreign__solicitud_fecha_desde__month__in=mes_list).filter(comisionadosolicitud_foreign__solicitud_solicitante=agente)
            elif not mes_list and not ano:
                agentes_list = ComisionadoSolicitud.objects.all().filter(comisionadosolicitud_foreign__solicitud_solicitante=agente)
            else:
                agentes_list = ComisionadoSolicitud.objects.filter(
                    comisionadosolicitud_foreign__solicitud_fecha_desde__year=ano, comisionadosolicitud_foreign__solicitud_fecha_desde__month__in=mes_list).filter(comisionadosolicitud_foreign__solicitud_solicitante=agente)
        
            
            dias = agentes_list.annotate(
                            cantidad_de_dias=Sum("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"))
            dias = dias.aggregate(cantidad_de_dias=Sum("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"))
            
            if dias["cantidad_de_dias"] is not None:
                agente_last = agentes_list.last()
                
                dias["valor_viaticos"] = agente_last.valor_viatico_dia() * dias["cantidad_de_dias"].days
                dias["combustible"] = agentes_list.aggregate(combustible=Sum("comisionadosolicitud_combustible"))["combustible"]
                dias["gastos"] = agentes_list.aggregate(gastos=Sum("comisionadosolicitud_gastos"))["gastos"]
                dias["pasajes"] = agentes_list.aggregate(pasajes=Sum("comisionadosolicitud_pasaje"))["pasajes"]
                dias["total"] = dias["valor_viaticos"] + dias["combustible"] + dias["gastos"] + dias["pasajes"]
                queryset.update({
                    agente.comisionado_nombreyapellido:dias
                    })

        return queryset
