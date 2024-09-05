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
    permission_required = "secretariador.add_solicitud"

    model = Comisionado
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteviaticosporagente.html"
	
    def get_queryset(self):
        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial,fecha_final]).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%d/%m/%Y")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%d/%m/%Y")
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)

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
    permission_required = "secretariador.add_solicitud"

    model = Comisionado
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteviaticosporarea.html"

    def get_queryset(self):

        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial,fecha_final]).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%d/%m/%Y")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%d/%m/%Y")
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)
        
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

@method_decorator(login_required, name="dispatch")
class CrearReporteAusenciasPorAgente(PermissionRequiredMixin, generic.ListView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "secretariador.add_solicitud"

    model = Comisionado
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteausenciasporagente.html"
	
    def get_queryset(self):
        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial,fecha_final]).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%d/%m/%Y")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%d/%m/%Y")
            solicitudes = ComisionadoSolicitud.objects.filter(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)

        agentes = Comisionado.objects.all()
        queryset = {}
        final_queryset = {}
        for agente in agentes:
            # Cantidad de días por agente
            agentes_list = solicitudes.filter(comisionadosolicitud_nombre=agente)
            solicitudes_annotated = agentes_list.annotate(
                dias=F("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"), 
                ).aggregate(
                    cantidad_de_dias=Sum("comisionadosolicitud_foreign__solicitud_cantidad_de_dias"), 
                )

            # fechas = [self.solicitud_fecha_desde+timedelta(days=x) for x in range((self.solicitud_fecha_hasta-self.solicitud_fecha_desde).days+1)]
            # fechas = [datetime.strftime(fecha, "%d/%m/%Y") for fecha in fechas]
            days_list = []
            for comision in agentes_list:
                if comision.comisionadosolicitud_foreign.solicitud_cantidad_de_dias is not None:
                    days_list.append(", ".join(comision.comisionadosolicitud_foreign.solicitud_fechas()))

            days_list = ", ".join(days_list)
            if solicitudes_annotated["cantidad_de_dias"] is not None:
                queryset.update({
                        agente.comisionado_nombreyapellido: {
                            "cantidad_de_dias": solicitudes_annotated["cantidad_de_dias"].days,
                            "fechas_en_comision": days_list
                        }
                    })
        final_queryset.update({
            "comisionados": queryset,
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final,
            "fechas_en_comision": days_list,
        })
        return final_queryset

@method_decorator(login_required, name="dispatch")
class CrearReporteComisionesDuplicadas(PermissionRequiredMixin, generic.ListView):
    """
    Genera reporte de comisiones duplicadas.
    """

    login_url = "/"
    redirect_field_name = "login"
    permission_required = "secretariador.add_solicitud"

    model = Solicitud
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteduplicados.html"
	
    def get_queryset(self):
        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = Solicitud.objects.filter(solicitud_fecha_desde__range=[fecha_inicial,fecha_final]).exclude(solicitud_anulada=True)
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%d/%m/%Y")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%d/%m/%Y")
            solicitudes = Solicitud.objects.filter(solicitud_fecha_desde__range=[fecha_inicial, fecha_final]).exclude(solicitud_anulada=True)

        fechas = [fecha_inicial+timedelta(days=x) for x in range((fecha_final-fecha_inicial).days+1)]
        fechas = [datetime.strftime(fecha, "%Y-%m-%d") for fecha in fechas]
        queryset = {}
        final_queryset = {}

        for fecha in fechas:
            solicitudes = Solicitud.objects.filter(solicitud_fecha_desde=fecha).exclude(solicitud_anulada=True)
            for solicitud in solicitudes:
                if solicitudes is not None:
                    queryset.update({
                            solicitud.solicitud_actuacion: {
                                "cantidad_de_dias": solicitud.solicitud_cantidad_de_dias.days,
                                "localidades": [localidad.localidad_nombre for localidad in solicitud.solicitud_localidades.all()],
                                "fechas": solicitud.solicitud_fechas(),
                                "solicitante": solicitud.solicitud_solicitante.comisionado_nombreyapellido,
                                "comisionados": solicitud.get_comisionados(),
                                "tareas": solicitud.solicitud_tareas,
                            }
                        })
         
        duplicates = {}
        for actuacion, values in queryset.items():
            key = tuple(values['fechas']) + tuple(values['localidades'])
            if key in duplicates:
                duplicates[key].append([
                    actuacion,
                    values["solicitante"],
                    values["comisionados"],
                    values["tareas"],
                    values["cantidad_de_dias"],
                    values["localidades"],
                    ])
            else:
                duplicates[key] = [[
                    actuacion,
                    values["solicitante"],
                    values["comisionados"],
                    values["tareas"],
                    values["cantidad_de_dias"],
                    values["localidades"],
                    ]]

        final_queryset = {}
        final_queryset["duplicados"] = {}
        for key, actuaciones in duplicates.items():
            if len(actuaciones) > 1:
                final_queryset["duplicados"].update({key : actuaciones})
        final_queryset["fechas"] = {
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final,
        }

        return final_queryset
