from django.contrib import admin
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from secretariador.models import *
from secretariador.resources import OrganigramaResource, VehiculoResource, IncorporacionResource
from django.contrib.auth.models import Group

class InstrumentosLegalesMemorandumAdmin(SimpleHistoryAdmin):
    model = InstrumentosLegalesMemorandum
    search_fields = ["instrumentolegalmemorandum_tipo", "instrumentolegalmemorandum_numero", "instrumentolegalmemorandum_ano"]
    list_display = ["id", "instrumentolegalmemorandum_tipo", "instrumentolegalmemorandum_numero", "instrumentolegalmemorandum_ano", "instrumentolegalmemorandum_fecha_aprobacion"]
    list_filter = ["instrumentolegalmemorandum_tipo", "instrumentolegalmemorandum_autocarga"]

class InstrumentosLegalesResolucionesAdmin(SimpleHistoryAdmin):
    model = InstrumentosLegalesResoluciones
    search_fields = ["instrumentolegalresoluciones_tipo", "instrumentolegalresoluciones_numero", "instrumentolegalresoluciones_acta", "instrumentolegalresoluciones_ano"]
    list_display = ["id", "instrumentolegalresoluciones_tipo", "instrumentolegalresoluciones_numero", "instrumentolegalresoluciones_acta", "instrumentolegalresoluciones_ano", "instrumentolegalresoluciones_fecha_aprobacion"]
    list_filter = ["instrumentolegalresoluciones_tipo", "instrumentolegalresoluciones_autocarga"]

class InstrumentosLegalesDecretoAdmin(SimpleHistoryAdmin):
    model = InstrumentosLegalesDecretos
    search_fields = ["instrumentolegaldecretos_tipo", "instrumentolegaldecretos_numero", "instrumentolegaldecretos_ano"]
    list_display = ["id", "instrumentolegaldecretos_tipo", "instrumentolegaldecretos_numero", "instrumentolegaldecretos_ano", "instrumentolegaldecretos_fecha_aprobacion"]
    list_filter = ["instrumentolegaldecretos_tipo"]

class MontoViaticoDiarioAdmin(SimpleHistoryAdmin):
    model = MontoViaticoDiario
    search_fields = ["montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_numero"]
    autocomplete_fields = ["montoviaticodiario_decreto_reglamentario"]
    list_display = ["id", "montoviaticodiario_decreto_reglamentario"]

class OrganigramaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = OrganigramaResource
    search_fields = ["organigrama_cargo", "organigrama_escalafon"]
    list_display = ["id", "organigrama_cargo", "organigrama_escalafon"]

class ComisionadoSolicitudAdminInline(admin.TabularInline):
    model = ComisionadoSolicitud
    search_fields = ["comisionadosolicitud_nombre__agente_nombreyapellido"]
    fields = [
        "comisionadosolicitud_nombre",
        "comisionadosolicitud_colaborador",
        "comisionadosolicitud_chofer",
        "comisionadosolicitud_combustible",
        "comisionadosolicitud_pasaje",
        "comisionadosolicitud_gastos",
    ]
    autocomplete_fields = ["comisionadosolicitud_foreign", "comisionadosolicitud_incorporacion_foreign", "comisionadosolicitud_nombre"]

class SolicitudAdmin(SimpleHistoryAdmin):
    inlines = [ComisionadoSolicitudAdminInline]
    search_fields = ["solicitud_actuacion"]
    autocomplete_fields = ["solicitud_solicitante", "solicitud_provincia", "solicitud_localidades", "solicitud_decreto_viaticos", "solicitud_vehiculo", "solicitud_resolucion"]
    list_display = ["id", "solicitud_actuacion", "solicitud_solicitante", "solicitud_provincia", "solicitud_fecha_desde", "solicitud_fecha_hasta", "solicitud_anulada"]
    list_filter = ["solicitud_provincia", "solicitud_aereo", "solicitud_dia_inhabil", "solicitud_anulada"]

class VehiculoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    model = Vehiculo
    resource_class = VehiculoResource
    search_fields = ["vehiculo_modelo", "vehiculo_patente"]
    autocomplete_fields = ["vehiculo_titular_agente", "vehiculo_titular_empresa", "vehiculo_poliza_aseguradora"]
    list_display = ["id", "vehiculo_modelo", "vehiculo_patente", "vehiculo_caracter", "vehiculo_titular_agente", "vehiculo_titular_empresa"]
    list_filter = ["vehiculo_caracter"]

class IncorporacionAdmin(ImportExportMixin, SimpleHistoryAdmin):
    model = Incorporacion
    resource_class = IncorporacionResource
    inlines = [ComisionadoSolicitudAdminInline]
    search_fields = ["incorporacion_actuacion"]
    autocomplete_fields = ["incorporacion_solicitud", "incorporacion_solicitante", "incorporacion_resolucion"]
    list_display = ["id", "incorporacion_actuacion", "incorporacion_solicitud", "incorporacion_solicitante"]

class ComisionadoSolicitudAdmin(SimpleHistoryAdmin):
    model = ComisionadoSolicitud
    search_fields = ["comisionadosolicitud_foreign__solicitud_actuacion", "comisionadosolicitud_incorporacion_foreign__incorporacion_actuacion", "comisionadosolicitud_nombre__agente_nombreyapellido"]
    autocomplete_fields = ["comisionadosolicitud_foreign", "comisionadosolicitud_incorporacion_foreign", "comisionadosolicitud_nombre"]
    list_display = ["id", "comisionadosolicitud_nombre", "comisionadosolicitud_foreign", "comisionadosolicitud_incorporacion_foreign", "comisionadosolicitud_viatico_total"]
    list_filter = ["comisionadosolicitud_colaborador", "comisionadosolicitud_chofer", "comisionadosolicitud_sin_viatico"]
    fields = [
        "comisionadosolicitud_foreign",
        "comisionadosolicitud_incorporacion_foreign",
        "comisionadosolicitud_nombre",
        "comisionadosolicitud_colaborador",
        "comisionadosolicitud_chofer",
        "comisionadosolicitud_combustible",
        "comisionadosolicitud_pasaje",
        "comisionadosolicitud_gastos",
        "comisionadosolicitud_viatico_diario",
        "comisionadosolicitud_viatico_computado",
        "comisionadosolicitud_cantidad_de_dias"
    ]
    readonly_fields = [
        "comisionadosolicitud_viatico_diario",
        "comisionadosolicitud_viatico_computado",
        "comisionadosolicitud_cantidad_de_dias",
        "comisionadosolicitud_viatico_total"
    ]

# Registro de los modelos en Admin
admin.site.register(InstrumentosLegalesMemorandum, InstrumentosLegalesMemorandumAdmin)
admin.site.register(InstrumentosLegalesResoluciones, InstrumentosLegalesResolucionesAdmin)
admin.site.register(InstrumentosLegalesDecretos, InstrumentosLegalesDecretoAdmin)
admin.site.register(MontoViaticoDiario, MontoViaticoDiarioAdmin)
admin.site.register(Organigrama, OrganigramaAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Incorporacion, IncorporacionAdmin)
admin.site.register(ComisionadoSolicitud, ComisionadoSolicitudAdmin)