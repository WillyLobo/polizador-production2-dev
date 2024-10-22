from django.contrib import admin
from import_export.admin import ImportExportMixin

from secretariador.models import *
from secretariador.resources import OrganigramaResource, ComisionadoResource, VehiculoResource, IncorporacionResource

class InstrumentosLegalesMemorandumAdmin(admin.ModelAdmin):
    model = InstrumentosLegalesMemorandum

class InstrumentosLegalesResolucionesAdmin(admin.ModelAdmin):
    model = InstrumentosLegalesResoluciones

class InstrumentosLegalesDecretoAdmin(admin.ModelAdmin):
    model = InstrumentosLegalesDecretos

class MontoViaticoDiarioAdmin(admin.ModelAdmin):
    model = MontoViaticoDiario

class OrganigramaAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrganigramaResource

class ComisionadoSolicitudAdminInline(admin.TabularInline):
    model = ComisionadoSolicitud

class SolicitudAdmin(admin.ModelAdmin):
    inlines = [ComisionadoSolicitudAdminInline]

class ComisionadoAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ComisionadoResource

class VehiculoAdmin(ImportExportMixin, admin.ModelAdmin):
    model = Vehiculo
    resource_class = VehiculoResource

class IncorporacionAdmin(ImportExportMixin, admin.ModelAdmin):
    model = Incorporacion
    resource_class = IncorporacionResource
    inlines = [ComisionadoSolicitudAdminInline]

class ComisionadoSolicitudAdmin(admin.ModelAdmin):
    model = ComisionadoSolicitud
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