from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from secretariador.models import *
from personalizador.models import Agente, Oficina
from django.db.models import Q, FilteredRelation, Subquery, OuterRef, Sum, F, Min, Max
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from datetime import datetime, timedelta


def _anos_disponibles():
    # Años con al menos una solicitud, para poblar los <select name="ano"> de los
    # reportes de calendario en vez de hardcodear un rango fijo de años.
    return [d.year for d in Solicitud.objects.dates("solicitud_fecha_desde", "year", order="DESC")]


@method_decorator(login_required, name="dispatch")
class PDFMergeTemplateView(PermissionRequiredMixin, generic.TemplateView):
    permission_required = "secretariador.view_solicitud"
    template_name = "html_to_pdf_merger.html"

@method_decorator(login_required, name="dispatch")
class CrearReporteViaticosPorAgente(PermissionRequiredMixin, generic.ListView):
    permission_required = "secretariador.view_solicitud"

    model = Agente
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteviaticosporagente.html"
	
    def get_queryset(self):
        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = ComisionadoSolicitud.objects.filter(Q(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]) | Q(
                comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_fecha_desde__range=[fecha_inicial, fecha_final])).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%d")
            solicitudes = ComisionadoSolicitud.objects.filter(Q(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]) | Q(
                comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_fecha_desde__range=[fecha_inicial, fecha_final])).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)

        agentes = Agente.objects.all()
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
                        agente.agente_nombreyapellido: {
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
    permission_required = "secretariador.view_solicitud"

    model = Oficina
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteviaticosporarea.html"

    def get_queryset(self):

        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = ComisionadoSolicitud.objects.filter(Q(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]) | Q(
                comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_fecha_desde__range=[fecha_inicial, fecha_final])).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%d")
            solicitudes = ComisionadoSolicitud.objects.filter(Q(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]) | Q(
                comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_fecha_desde__range=[fecha_inicial, fecha_final])).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)

        def _totales(qs):
            return qs.annotate(
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

        # Se agrupa por el nivel mas alto cargado en la Oficina del solicitante (Gerencia; si no
        # tiene, Direccion; si no tiene, el Directorio/Presidencia), en vez de por la Oficina exacta
        # (que suele llegar hasta Departamento), para que el reporte quede a nivel de area/gerencia.
        # cargo_gerencia/cargo_direccion/cargo_directorio ya vienen consistentes entre si por
        # Oficina.clean(), asi que filtrar por uno de ellos alcanza a todas las Oficinas del grupo.
        grupos = {}
        for oficina in Oficina.objects.all():
            if oficina.cargo_gerencia_id:
                key = ("gerencia", oficina.cargo_gerencia_id)
                label = str(oficina.cargo_gerencia)
                filtro = {"oficina__cargo_gerencia_id": oficina.cargo_gerencia_id}
            elif oficina.cargo_direccion_id:
                key = ("direccion", oficina.cargo_direccion_id)
                label = str(oficina.cargo_direccion)
                filtro = {"oficina__cargo_direccion_id": oficina.cargo_direccion_id}
            elif oficina.cargo_directorio_id:
                key = ("directorio", oficina.cargo_directorio_id)
                label = str(oficina.cargo_directorio)
                filtro = {
                    "oficina__cargo_directorio_id": oficina.cargo_directorio_id,
                    "oficina__cargo_gerencia__isnull": True,
                    "oficina__cargo_direccion__isnull": True,
                }
            else:
                continue
            grupos.setdefault(key, (label, filtro))

        queryset = {}
        final_queryset = {}
        for label, filtro in grupos.values():
            agentes_list = solicitudes.filter(
                Q(**{f"comisionadosolicitud_foreign__solicitud_solicitante__{k}": v for k, v in filtro.items()}) |
                Q(**{f"comisionadosolicitud_incorporacion_foreign__incorporacion_solicitante__{k}": v for k, v in filtro.items()})
            )

            solicitudes_annotated = _totales(agentes_list)

            if solicitudes_annotated["cantidad_de_dias"] is not None:
                queryset.update({
                        label: {
                            "cantidad_de_dias": solicitudes_annotated["cantidad_de_dias"].days,
                            "viatico":          solicitudes_annotated["viatico"],
                            "pasaje":           solicitudes_annotated["pasaje"],
                            "gastos":           solicitudes_annotated["gastos"],
                            "combustible":      solicitudes_annotated["combustible"],
                            "valor_viatico":    solicitudes_annotated["valor_viatico"]
                        }
                    })

        # Solicitantes sin oficina cargada: se agrupan aparte para que ninguna solicitud
        # quede fuera del reporte. El guard *_foreign__isnull=False evita que el LEFT JOIN
        # de la rama no usada (p.ej. incorporacion en una solicitud regular) cuente como "sin oficina".
        solicitudes_sin_area = solicitudes.filter(
            Q(comisionadosolicitud_foreign__isnull=False, comisionadosolicitud_foreign__solicitud_solicitante__oficina__isnull=True) |
            Q(comisionadosolicitud_incorporacion_foreign__isnull=False, comisionadosolicitud_incorporacion_foreign__incorporacion_solicitante__oficina__isnull=True)
        )
        solicitudes_annotadas_sin_area = _totales(solicitudes_sin_area)
        if solicitudes_annotadas_sin_area["cantidad_de_dias"] is not None:
            queryset.update({
                    "Sin área cargada": {
                        "cantidad_de_dias": solicitudes_annotadas_sin_area["cantidad_de_dias"].days,
                        "viatico":          solicitudes_annotadas_sin_area["viatico"],
                        "pasaje":           solicitudes_annotadas_sin_area["pasaje"],
                        "gastos":           solicitudes_annotadas_sin_area["gastos"],
                        "combustible":      solicitudes_annotadas_sin_area["combustible"],
                        "valor_viatico":    solicitudes_annotadas_sin_area["valor_viatico"]
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
    permission_required = "secretariador.view_solicitud"

    model = Agente
    context_object_name = "solicitud"
    template_name = "reportes/crear-reporteausenciasporagente.html"
	
    def get_queryset(self):
        if not self.request.GET or self.request.GET.get("fecha_final") == "" or self.request.GET.get("fecha_inicial") == "":
            fecha_final = datetime.today()
            fecha_inicial = fecha_final - timedelta(days=30)
            solicitudes = ComisionadoSolicitud.objects.filter(Q(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]) | Q(
                comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_fecha_desde__range=[fecha_inicial, fecha_final])).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)
        elif self.request.GET:
            fecha_final = self.request.GET.get("fecha_final")
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%d")
            solicitudes = ComisionadoSolicitud.objects.filter(Q(comisionadosolicitud_foreign__solicitud_fecha_desde__range=[fecha_inicial, fecha_final]) | Q(
                comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_fecha_desde__range=[fecha_inicial, fecha_final])).exclude(comisionadosolicitud_foreign__solicitud_anulada=True)

        agentes = Agente.objects.all()
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
            # fechas = [datetime.strftime(fecha, "%Y-%m-%d") for fecha in fechas]
            days_list = []
            for comision in agentes_list:
                if comision.comisionadosolicitud_foreign:
                    if comision.comisionadosolicitud_foreign.solicitud_cantidad_de_dias is not None:
                        days_list.append(", ".join(comision.comisionadosolicitud_foreign.solicitud_fechas()))
                if comision.comisionadosolicitud_incorporacion_foreign:
                    if comision.comisionadosolicitud_incorporacion_foreign.incorporacion_solicitud.solicitud_cantidad_de_dias is not None:
                        days_list.append(", ".join(comision.comisionadosolicitud_incorporacion_foreign.incorporacion_solicitud.solicitud_fechas()))

            days_list = ", ".join(days_list)
            if solicitudes_annotated["cantidad_de_dias"] is not None:
                queryset.update({
                        agente.agente_nombreyapellido: {
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

    permission_required = "secretariador.view_solicitud"

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
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
            fecha_inicial = self.request.GET.get("fecha_inicial")
            fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%d")
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
                                "solicitante": solicitud.solicitud_solicitante.agente_nombreyapellido,
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

@method_decorator(login_required, name="dispatch")
class CrearReporteViaticosPorAgenteIndividual(PermissionRequiredMixin, generic.TemplateView):
    # Los eventos del calendario los trae el propio FullCalendar desde
    # /v1/api/calendario/agente-individual/ (ver api/views/secretariador_views.py);
    # esta vista solo arma el shell de filtros con los valores ya elegidos.
    permission_required = "secretariador.view_solicitud"

    template_name = "reportes/crear-reporteviaticosporagenteindividual.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agente_id = self.request.GET.get("agente")
        ano = self.request.GET.get("ano") or datetime.today().year
        agente = get_object_or_404(Agente, id=agente_id) if agente_id else None
        context.update({
            "initial_date": f"{ano}-01-01",
            "ano": str(ano),
            "agente": agente,
            "anos_disponibles": _anos_disponibles(),
        })
        return context

@method_decorator(login_required, name="dispatch")
class CalendarioSemanal(PermissionRequiredMixin, generic.TemplateView):
    # Los eventos del calendario los trae el propio FullCalendar desde
    # /v1/api/calendario/semanal/ (ver api/views/secretariador_views.py);
    # esta vista solo arma el shell de filtros con los valores ya elegidos.
    permission_required = "secretariador.view_solicitud"

    template_name = "reportes/calendario-semanal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agente_id = self.request.GET.get("agente")
        agente = get_object_or_404(Agente, id=agente_id) if agente_id else None
        context.update({
            "initial_date": datetime.today().strftime("%Y-%m-%d"),
            "agente": agente,
        })
        return context

@method_decorator(login_required, name="dispatch")
class CalendarioAnual(PermissionRequiredMixin, generic.TemplateView):
    # Los eventos del calendario los trae el propio FullCalendar desde
    # /v1/api/calendario/anual/ (ver api/views/secretariador_views.py);
    # esta vista solo arma el shell de filtros con los valores ya elegidos.
    permission_required = "secretariador.view_solicitud"

    template_name = "reportes/calendario-anual.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ano_param = self.request.GET.get("ano")
        ano = ano_param or datetime.today().year
        # Sin filtro explícito de año, arranca en la semana actual; si se eligió
        # un año puntual, arranca desde el 1° de enero de ese año.
        initial_date = f"{ano}-01-01" if ano_param else datetime.today().strftime("%Y-%m-%d")
        context.update({
            "initial_date": initial_date,
            "ano": str(ano),
            "anos_disponibles": _anos_disponibles(),
        })
        return context