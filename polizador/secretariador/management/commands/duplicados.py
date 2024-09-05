from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from secretariador.models import *
from carga.models import *
from django.db.models import Q, FilteredRelation, Subquery, OuterRef, Sum, F, Min, Max
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from datetime import datetime, timedelta

# class Style:
#     def ERROR(self, text: str) -> str: ...
#     def SUCCESS(self, text: str) -> str: ...
#     def WARNING(self, text: str) -> str: ...
#     def NOTICE(self, text: str) -> str: ...
#     def SQL_FIELD(self, text: str) -> str: ...
#     def SQL_COLTYPE(self, text: str) -> str: ...
#     def SQL_KEYWORD(self, text: str) -> str: ...
#     def SQL_TABLE(self, text: str) -> str: ...
#     def HTTP_INFO(self, text: str) -> str: ...
#     def HTTP_SUCCESS(self, text: str) -> str: ...
#     def HTTP_REDIRECT(self, text: str) -> str: ...
#     def HTTP_NOT_MODIFIED(self, text: str) -> str: ...
#     def HTTP_BAD_REQUEST(self, text: str) -> str: ...
#     def HTTP_NOT_FOUND(self, text: str) -> str: ...
#     def HTTP_SERVER_ERROR(self, text: str) -> str: ...
#     def MIGRATE_HEADING(self, text: str) -> str: ...
#     def MIGRATE_LABEL(self, text: str) -> str: ...
#     def ERROR_OUTPUT(self, text: str) -> str: ...

"""
SELECT "listado_padron"."id", "listado_padron"."DISTRITO", "listado_padron"."TX_TIPO_EJEMPLAR", "listado_padron"."NU_MATRICULA", "listado_padron"."TX_APELLIDO", "listado_padron"."TX_NOMBRE", "listado_padron"."TX_CLASE", "listado_padron"."TX_GENERO", "listado_padron"."TX_DOMICILIO", "listado_padron"."TX_SECCION", "listado_padron"."TX_CIRCUITO", "listado_padron"."TX_LOCALIDAD", "listado_padron"."TX_CODIGO_POSTAL", "listado_padron"."TX_TIPO_NACIONALIDAD", "listado_padron"."NUMERO_MESA", "listado_padron"."NU_ORDEN_MESA" 
    FROM "listado_padron" WHERE "listado_padron"."NU_MATRICULA" = 30789619
"""
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        Checks if solicitudes are duplicados in day and location.
        """

        fecha_final = datetime.today()
        fecha_inicial = "01/01/2024"
        fecha_inicial = datetime.strptime(fecha_inicial, "%d/%m/%Y")
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
                                "solicitante": solicitud.solicitud_solicitante,
                                "comisionados": solicitud.get_comisionados(),
                                "tareas": solicitud.solicitud_tareas,
                            }
                        })
         
        duplicates = {}
        for actuacion, values in queryset.items():
            key = tuple(values['fechas']) + tuple(values['localidades'])
            if key in duplicates:
                duplicates[key].append([actuacion, values["solicitante"], values["comisionados"], values["tareas"]])
            else:
                duplicates[key] = [[actuacion, values["solicitante"], values["comisionados"], values["tareas"]]]

        final_queryset = {}
        for key, actuaciones in duplicates.items():
            if len(actuaciones) > 1:
                final_queryset[key] = actuaciones

        # Print the final_queryset
        for key, actuaciones in final_queryset.items():
            print(f"{self.style.ERROR('Fechas y Localidades duplicadas:')} {key}")
            print("-------------------------")
            for actuacion in actuaciones:
                print(f"{self.style.WARNING('Actuacion:')} {actuacion[0]}")
                print(f"Solicitante: {actuacion[1]}")
                print(f"Comisionados: {actuacion[2]}")
                print(f"Tareas: {actuacion[3]}")
            print("-------------------------")