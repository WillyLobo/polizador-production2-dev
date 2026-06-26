from django.contrib import admin

from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from carga import models
from carga import resources

# Register your models here.
class ReceptorAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.ReceptorResource
class AreaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.AreaResource
class AseguradoraAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.AseguradoraResource
	search_fields = ["aseguradora_nombre"]
class EmpresaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	list_display = ["id", "empresa_nombre", "empresa_cuit"]
	ordering = ["id"]
	resource_class = resources.EmpresaResource
	search_fields = ["empresa_nombre"]
class PolizaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.PolizaResource

class PolizaMovimientoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.PolizaMovimientoResource

# class LegacyPolizaAdmin(ImportExportMixin, SimpleHistoryAdmin):
# 	resource_class = resources.LegacyPolizaResource
# 	list_display = ("legacy_poliza_receptor", "legacy_poliza_concepto", "legacy_poliza_numero", "legacy_poliza_tomador")

class ProgramaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.ProgramaResource

class ProvinciaResourceAdmin(ImportExportMixin, SimpleHistoryAdmin):
	model = models.Provincia
	resource_class = resources.ProvinciaResource
	search_fields = ["provincia_nombre"]

class DepartamentoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.DepartamentoResource
	list_display = ("id", "departamento_nombre")

class LocalidadAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.LocalidadResource
	list_display = ("id", "localidad_nombre", "localidad_municipio", "localidad_departamento", "localidad_funcion")
	search_fields = ["localidad_nombre", "localidad_municipio__municipio_nombre", "localidad_departamento__departamento_nombre", "localidad_funcion"]

class MunicipioAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.MunicipioResource
	list_display = ("id", "municipio_nombre", "municipio_departamento", "municipio_region")

class ObraAdmin(ImportExportMixin, SimpleHistoryAdmin):
	ordering = ["id"]
	search_fields = ["id","obra_convenio","obra_nombre", "obra_empresa__empresa_nombre"]
	resource_class = resources.ObraResource

class PrototipoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.PrototipoResource

class CertificadoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["certificado_obra"]
	resource_class = resources.CertificadoResource

class ConjuntoLicitadoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.ConjuntoLicitadoResource

class RegionAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.RegionResource

class CertificadoRubroAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.CertificadoRubroResource

class CertificadoFinanciamientoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.FinanciamientoResource

class PlanDeTrabajosItemInline(admin.TabularInline):
	model = models.PlanDeTrabajosItem

class PlanDeTrabajosRubroInline(admin.TabularInline):
	model = models.PlanDeTrabajosRubro

class PlandeTrabajosAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["trabajos_obra"]
	search_fields = ["trabajos_obra__obra_nombre"]
	inlines = [
		PlanDeTrabajosRubroInline,
	]
	resource_class = resources.PlandeTrabajosResource

class PlanDeTrabajosRubroAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["rubro_plan"]
	search_fields = ["rubro_nombre", "rubro_plan__trabajos_obra__obra_nombre"]
	inlines = [
		PlanDeTrabajosItemInline,
	]
	resource_class = resources.PlanDeTrabajosRubroResource

class FojaDeMedicionItemInline(admin.TabularInline):
	model = models.FojaDeMedicionItem

class FojaDeMedicionFotoInline(admin.TabularInline):
	model = models.FojaDeMedicionFoto

class FojaDeMedicionAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["foja_rubro", "foja_inspector"]
	inlines = [
		FojaDeMedicionItemInline,
		FojaDeMedicionFotoInline,
	]
	resource_class = resources.FojaDeMedicionResource

class ContratoMontoInline(admin.TabularInline):
	model = models.ContratoMonto

class ContratoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["contrato_obra"]
	search_fields = ["contrato_descripcion", "contrato_obra__obra_nombre"]
	inlines = [
		ContratoMontoInline,
	]
	resource_class = resources.ContratoResource

class ContratoMontoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.ContratoMontoResource

class ContratoRubroAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.ContratoRubroResource

class ContratoDigitalAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["contratodigital_contrato"]
	resource_class = resources.ContratoDigitalResource

class ResolucionDigitalAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["resoluciondigital_contrato"]
	resource_class = resources.ResolucionDigitalResource

class UviAdmin(ImportExportMixin, SimpleHistoryAdmin):
	list_display = ("id", "uvi_fecha", "uvi_valor", "uvi_uuid")
	ordering = ("-uvi_fecha",)
	resource_class = resources.UviResource

admin.site.register(models.Receptor, ReceptorAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Aseguradora, AseguradoraAdmin)
admin.site.register(models.Empresa, EmpresaAdmin)
# admin.site.register(models.LegacyPoliza, LegacyPolizaAdmin)
admin.site.register(models.Programa, ProgramaAdmin)
admin.site.register(models.Provincia, ProvinciaResourceAdmin)
admin.site.register(models.Departamento, DepartamentoAdmin)
admin.site.register(models.Localidad, LocalidadAdmin)
admin.site.register(models.Municipio, MunicipioAdmin)
admin.site.register(models.Obra, ObraAdmin)
admin.site.register(models.Prototipo, PrototipoAdmin)
admin.site.register(models.Certificado, CertificadoAdmin)
admin.site.register(models.Poliza, PolizaAdmin)
admin.site.register(models.Poliza_Movimiento, PolizaMovimientoAdmin)
admin.site.register(models.ConjuntoLicitado, ConjuntoLicitadoAdmin)
admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.CertificadoRubro, CertificadoRubroAdmin)
admin.site.register(models.CertificadoFinanciamiento, CertificadoFinanciamientoAdmin)
admin.site.register(models.PlanDeTrabajos, PlandeTrabajosAdmin)
admin.site.register(models.PlanDeTrabajosRubro, PlanDeTrabajosRubroAdmin)
admin.site.register(models.FojaDeMedicion, FojaDeMedicionAdmin)
admin.site.register(models.Contrato, ContratoAdmin)
admin.site.register(models.ContratoMonto, ContratoMontoAdmin)
admin.site.register(models.ContratoRubro, ContratoRubroAdmin)
admin.site.register(models.ContratosDigitales, ContratoDigitalAdmin)
admin.site.register(models.ResolucionesDigitales, ResolucionDigitalAdmin)
admin.site.register(models.Uvi, UviAdmin)

class IndecAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.IndecResource

admin.site.register(models.INDEC, IndecAdmin)