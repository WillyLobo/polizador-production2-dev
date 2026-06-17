from django.contrib import admin
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from secretariador.models import *
from secretariador.resources import OrganigramaResource, ComisionadoResource, VehiculoResource, IncorporacionResource
from django.contrib.auth.models import Group

class InstrumentosLegalesMemorandumAdmin(SimpleHistoryAdmin):
    model = InstrumentosLegalesMemorandum
    search_fields = ["instrumentolegalmemorandum_tipo", "instrumentolegalmemorandum_numero", "instrumentolegalmemorandum_ano"]

class InstrumentosLegalesResolucionesAdmin(SimpleHistoryAdmin):
    model = InstrumentosLegalesResoluciones
    search_fields = ["instrumentolegalresoluciones_tipo", "instrumentolegalresoluciones_numero", "instrumentolegalresoluciones_ano"]

class InstrumentosLegalesResolucionesDirectorioAdmin(SimpleHistoryAdmin):
    model = InstrumentosLegalesResolucionesDirectorio
    search_fields = ["instrumentolegalresolucionesdirectorio_tipo", "instrumentolegalresolucionesdirectorio_numero", "instrumentolegalresolucionesdirectorio_ano"]

class InstrumentosLegalesDecretoAdmin(SimpleHistoryAdmin):
    model = InstrumentosLegalesDecretos
    search_fields = ["instrumentolegaldecretos_tipo", "instrumentolegaldecretos_numero", "instrumentolegaldecretos_ano"]

class MontoViaticoDiarioAdmin(SimpleHistoryAdmin):
    model = MontoViaticoDiario
    search_fields = ["montoviaticodiario_decreto_reglamentario__instrumentolegaldecretos_numero"]
    autocomplete_fields = ["montoviaticodiario_decreto_reglamentario"]

class OrganigramaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = OrganigramaResource
    search_fields = ["organigrama_cargo", "organigrama_escalafon"]

class ComisionadoSolicitudAdminInline(admin.TabularInline):
    model = ComisionadoSolicitud
    search_fields = ["comisionadosolicitud_nombre__comisionado_nombreyapellido"]
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

class ComisionadoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ComisionadoResource
    search_fields = ["comisionado_nombreyapellido", "comisionado_dni"]
    autocomplete_fields = []

class VehiculoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    model = Vehiculo
    resource_class = VehiculoResource
    search_fields = ["vehiculo_modelo", "vehiculo_patente"]
    autocomplete_fields = ["vehiculo_titular_agente", "vehiculo_titular_empresa", "vehiculo_poliza_aseguradora"]

class IncorporacionAdmin(ImportExportMixin, SimpleHistoryAdmin):
    model = Incorporacion
    resource_class = IncorporacionResource
    inlines = [ComisionadoSolicitudAdminInline]
    search_fields = ["incorporacion_actuacion"]
    autocomplete_fields = ["incorporacion_solicitud", "incorporacion_solicitante", "incorporacion_resolucion"]

class ComisionadoSolicitudAdmin(SimpleHistoryAdmin):
    model = ComisionadoSolicitud
    search_fields = ["comisionadosolicitud_foreign__solicitud_actuacion", "comisionadosolicitud_incorporacion_foreign__incorporacion_actuacion", "comisionadosolicitud_nombre__comisionado_nombreyapellido"]
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
admin.site.register(Comisionado, ComisionadoAdmin)
admin.site.register(Organigrama, OrganigramaAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Incorporacion, IncorporacionAdmin)
admin.site.register(ComisionadoSolicitud, ComisionadoSolicitudAdmin)
admin.site.register(InstrumentosLegalesResolucionesDirectorio, InstrumentosLegalesResolucionesDirectorioAdmin)