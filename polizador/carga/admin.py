from django.contrib import admin

from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from carga import models
from carga import resources

# Register your models here.
class ReceptorAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.ReceptorResource
	search_fields = ["receptor_nombre"]
	list_display = ["id", "receptor_nombre"]
class AreaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.AreaResource
	search_fields = ["area_nombre"]
	list_display = ["id", "area_nombre"]
class AseguradoraAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.AseguradoraResource
	search_fields = ["aseguradora_nombre"]
	list_display = ["id", "aseguradora_nombre"]
class EmpresaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	list_display = ["id", "empresa_nombre", "empresa_cuit"]
	ordering = ["id"]
	resource_class = resources.EmpresaResource
	search_fields = ["empresa_nombre", "empresa_cuit"]
class PolizaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["poliza_aseguradora", "poliza_tomador", "poliza_obra"]
	search_fields = ["poliza_numero", "poliza_expediente", "poliza_aseguradora__aseguradora_nombre", "poliza_tomador__empresa_nombre", "poliza_obra__obra_nombre"]
	list_display = ["id", "poliza_numero", "poliza_fecha", "poliza_concepto", "poliza_aseguradora", "poliza_tomador", "poliza_obra"]
	list_filter = ["poliza_concepto", "poliza_aseguradora"]
	resource_class = resources.PolizaResource

class PolizaMovimientoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["poliza_movimiento_receptor", "poliza_movimiento_area", "poliza_movimiento_numero"]
	search_fields = ["poliza_movimiento_numero__poliza_numero"]
	list_display = ["id", "poliza_movimiento_numero", "poliza_movimiento_area", "poliza_movimiento_receptor", "poliza_movimiento_fecha"]
	list_filter = ["poliza_movimiento_area"]
	resource_class = resources.PolizaMovimientoResource

class ProgramaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.ProgramaResource
	search_fields = ["programa_nombre"]
	list_display = ["id", "programa_nombre"]

class ProvinciaResourceAdmin(ImportExportMixin, SimpleHistoryAdmin):
	model = models.Provincia
	resource_class = resources.ProvinciaResource
	search_fields = ["provincia_nombre"]
	list_display = ["id", "provincia_nombre"]

class DepartamentoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.DepartamentoResource
	search_fields = ["departamento_nombre"]
	list_display = ("id", "departamento_nombre")

class LocalidadAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.LocalidadResource
	autocomplete_fields = ["localidad_departamento", "localidad_municipio"]
	list_display = ("id", "localidad_nombre", "localidad_municipio", "localidad_departamento", "localidad_funcion")
	search_fields = ["localidad_nombre", "localidad_municipio__municipio_nombre", "localidad_departamento__departamento_nombre", "localidad_funcion"]
	list_filter = ["localidad_departamento", "localidad_funcion"]

class MunicipioAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.MunicipioResource
	autocomplete_fields = ["municipio_departamento", "municipio_region"]
	search_fields = ["municipio_nombre"]
	list_display = ("id", "municipio_nombre", "municipio_departamento", "municipio_region")
	list_filter = ["municipio_departamento", "municipio_region"]

class ObraAdmin(ImportExportMixin, SimpleHistoryAdmin):
	ordering = ["id"]
	autocomplete_fields = [
		"obra_empresa",
		"obra_region",
		"obra_departamento_m",
		"obra_municipio_m",
		"obra_localidad_m",
		"obra_conjunto",
		"obra_programa",
		"obra_inspector",
		"obra_representantetecnico",
		"obra_principal"
	]
	search_fields = ["id","obra_convenio","obra_nombre", "obra_empresa__empresa_nombre"]
	list_display = ["id", "obra_convenio", "obra_nombre", "obra_empresa", "obra_programa", "obra_expediente"]
	list_filter = ["obra_licitacion_tipo", "obra_programa", "obra_region"]
	resource_class = resources.ObraResource

class PrototipoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["prototipo_obra"]
	search_fields = ["prototipo_obra__obra_nombre"]
	list_display = ["id", "prototipo_obra", "prototipo_tipo", "prototipo_cantidad", "prototipo_superficie"]
	list_filter = ["prototipo_tipo", "prototipo_discapacitado"]
	resource_class = resources.PrototipoResource

class CertificadoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["certificado_obra", "certificado_rubro_db", "certificado_foja", "certificado_contrato_origen", "certificado_contrato_tramo"]
	list_select_related = ["certificado_obra"]
	search_fields = ["certificado_expediente", "certificado_obra__obra_nombre", "certificado_periodo"]
	list_display = [
		"id",
		"certificado_obra__obra_nombre",
		"certificado_tipo",
		"certificado_rubro_anticipo",
		"certificado_rubro_obra",
		"certificado_rubro_devanticipo",
		"certificado_fecha",
		"certificado_fecha_carga"
		]
	list_filter = ["certificado_tipo", "certificado_financiamiento", "certificado_fecha_carga_legacy"]

	resource_class = resources.CertificadoResource

class ConjuntoLicitadoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["conjunto_subconjunto"]
	search_fields = ["conjunto_nombre"]
	list_display = ["id", "conjunto_nombre", "conjunto_resolucion", "conjunto_subconjunto"]
	resource_class = resources.ConjuntoLicitadoResource

class RegionAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.RegionResource
	search_fields = ["region_numero"]
	list_display = ["id", "region_numero"]

class CertificadoRubroAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.CertificadoRubroResource
	search_fields = ["certificadorubro_nombre"]
	list_display = ["id", "certificadorubro_nombre", "certificadorubro_nombre_corto"]

class CertificadoFinanciamientoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.FinanciamientoResource
	search_fields = ["certificadofinanciamiento_nombre"]
	list_display = ["id", "certificadofinanciamiento_nombre", "certificadofinanciamiento_nombre_corto"]

class PlanDeTrabajosItemAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["planitem_rubro", "item_anterior"]
	search_fields = ["planitem_nombre", "planitem_rubro__rubro_nombre"]
	list_display = ["id", "planitem_nombre", "planitem_rubro", "planitem_incidencia_pct", "planitem_orden"]
	list_filter = ["planitem_rubro"]
	resource_class = resources.PlanDeTrabajosItemResource

class PlanDeTrabajosItemInline(admin.TabularInline):
	model = models.PlanDeTrabajosItem
	autocomplete_fields = ["item_anterior"]

class PlanDeTrabajosRubroInline(admin.TabularInline):
	model = models.PlanDeTrabajosRubro
	autocomplete_fields = ["rubro_anterior", "rubro_contratomonto"]

class PlandeTrabajosAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["trabajos_obra", "trabajos_contrato"]
	search_fields = ["trabajos_obra__obra_nombre"]
	list_display = ["id", "trabajos_obra", "trabajos_fecha", "trabajos_meses", "trabajos_contrato"]
	list_filter = ["trabajos_fecha"]
	fields = ["trabajos_obra", "trabajos_fecha", "trabajos_meses", "trabajos_fecha_inicio", "trabajos_contrato"]
	inlines = [
		PlanDeTrabajosRubroInline,
	]
	resource_class = resources.PlandeTrabajosResource

class PlanDeTrabajosRubroAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["rubro_plan", "rubro_anterior", "rubro_contratomonto", "rubro_certificado_rubro"]
	search_fields = ["rubro_nombre", "rubro_plan__trabajos_obra__obra_nombre"]
	list_display = ("rubro_nombre", "rubro_plan", "rubro_presupuesto", "rubro_contratomonto", "rubro_certificado_rubro")
	list_filter = ["rubro_certificado_rubro"]
	inlines = [
		PlanDeTrabajosItemInline,
	]
	resource_class = resources.PlanDeTrabajosRubroResource

class PlanDeTrabajosEtapaItemInline(admin.TabularInline):
	model = models.PlanDeTrabajosEtapaItem
	autocomplete_fields = ["etapaitem_planitem"]

class PlanDeTrabajosEtapaAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["etapa_rubro"]
	search_fields = ["etapa_rubro__rubro_nombre"]
	list_display = ("id", "etapa_rubro", "etapa_numero", "etapa_fecha")
	list_filter = ["etapa_fecha"]
	inlines = [
		PlanDeTrabajosEtapaItemInline,
	]
	resource_class = resources.PlanDeTrabajosEtapaResource

class FojaDeMedicionItemInline(admin.TabularInline):
	model = models.FojaDeMedicionItem
	autocomplete_fields = ["fojaitem_planitem"]

class FojaDeMedicionFotoInline(admin.TabularInline):
	model = models.FojaDeMedicionFoto

class FojaDeMedicionAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["foja_rubro", "foja_inspector"]
	search_fields = ["foja_rubro__rubro_nombre", "foja_numero"]
	list_display = ["id", "foja_numero", "foja_rubro", "foja_periodo", "foja_fecha", "foja_legacy"]
	list_filter = ["foja_legacy"]
	inlines = [
		FojaDeMedicionItemInline,
		FojaDeMedicionFotoInline,
	]
	resource_class = resources.FojaDeMedicionResource

class ContratoMontoInline(admin.TabularInline):
	model = models.ContratoMonto
	autocomplete_fields = ["contratomonto_rubro", "contratomonto_financiamiento"]

class ContratoTramoPagoInline(admin.TabularInline):
	model = models.ContratoTramoPago
	readonly_fields = ["tramo_numero"]

class ContratoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["contrato_obra"]
	search_fields = ["contrato_descripcion", "contrato_obra__obra_nombre"]
	list_display = ["id", "contrato_obra", "contrato_descripcion", "contrato_fecha", "contrato_resolucion"]
	list_filter = ["contrato_certificacion_por_etapas", "contrato_autocarga"]
	inlines = [
		ContratoMontoInline,
		ContratoTramoPagoInline,
	]
	resource_class = resources.ContratoResource

class ContratoMontoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["contratomonto_contrato", "contratomonto_rubro", "contratomonto_financiamiento"]
	search_fields = ["contratomonto_contrato__contrato_descripcion", "contratomonto_contrato__contrato_obra__obra_nombre"]
	list_display = ["id", "contratomonto_contrato", "contratomonto_rubro", "contratomonto_financiamiento", "contratomonto_pesos", "contratomonto_uvi"]
	list_filter = ["contratomonto_rubro", "contratomonto_financiamiento"]
	resource_class = resources.ContratoMontoResource

class ContratoTramoPagoAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["tramo_contrato"]
	search_fields = ["tramo_contrato__contrato_descripcion", "tramo_contrato__contrato_obra__obra_nombre"]
	list_display = ["id", "tramo_contrato", "tramo_numero", "tramo_pct_pago", "tramo_pct_disparador"]
	readonly_fields = ["tramo_numero"]
	resource_class = resources.ContratoTramoPagoResource

class ContratoRubroAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.ContratoRubroResource
	search_fields = ["contratorubro_tipo"]
	list_display = ["id", "contratorubro_tipo"]

class ContratoDigitalAdmin(ImportExportMixin, SimpleHistoryAdmin):
	autocomplete_fields = ["contratodigital_contrato", "contratodigital_tipo"]
	search_fields = ["contratodigital_descripcion", "contratodigital_contrato__contrato_descripcion", "contratodigital_contrato__contrato_obra__obra_nombre"]
	list_display = ["id", "contratodigital_contrato", "contratodigital_tipo", "contratodigital_nombre_archivo"]
	list_filter = ["contratodigital_tipo"]
	resource_class = resources.ContratoDigitalResource

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
admin.site.register(models.PlanDeTrabajosItem, PlanDeTrabajosItemAdmin)
admin.site.register(models.PlanDeTrabajosEtapa, PlanDeTrabajosEtapaAdmin)
admin.site.register(models.FojaDeMedicion, FojaDeMedicionAdmin)
admin.site.register(models.Contrato, ContratoAdmin)
admin.site.register(models.ContratoMonto, ContratoMontoAdmin)
admin.site.register(models.ContratoTramoPago, ContratoTramoPagoAdmin)
admin.site.register(models.ContratoRubro, ContratoRubroAdmin)
admin.site.register(models.ContratosDigitales, ContratoDigitalAdmin)
admin.site.register(models.Uvi, UviAdmin)

class IndecAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = resources.IndecResource
	list_display = ["id", "mes"]

admin.site.register(models.INDEC, IndecAdmin)