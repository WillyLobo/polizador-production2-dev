from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth.models import User
from carga import models

class ReceptorResource(resources.ModelResource):
	class Meta:
		model = models.Receptor

class AreaResource(resources.ModelResource):
	class Meta:
		model = models.Area

class AseguradoraResource(resources.ModelResource):
	class Meta:
		model = models.Aseguradora

class EmpresaResource(resources.ModelResource):
	class Meta:
		model = models.Empresa

class PolizaResource(resources.ModelResource):
	poliza_obra			= fields.Field(column_name="Obra", attribute="obra_nombre", widget=ForeignKeyWidget(models.Obra,"obra_nombre",))
	poliza_aseguradora	= fields.Field(column_name="Aseguradora", attribute="aseguradora_nombre", widget=ForeignKeyWidget(models.Aseguradora, "aseguradora_nombre",))
	poliza_tomador		= fields.Field(column_name="Tomador", attribute="tomador_nombre", widget=ForeignKeyWidget(models.Empresa, "empresa_nombre"))

	class Meta:
		fields = (
			"poliza_fecha",
			"poliza_expediente",
			"poliza_numero",
			"poliza_concepto",
			"poliza_anexo",
			"poliza_recibo",
			"poliza_aseguradora",
			"poliza_tomador",
			"poliza_obra",
			"poliza_monto_pesos",
			"poliza_monto_uvi",
			"poliza_creador",
			"poliza_editor",
		)
class LegacyPolizaResource(resources.ModelResource):
	legacy_poliza_receptor 		= fields.Field(column_name="legacy_poliza_receptor", attribute="legacy_poliza_receptor", widget=ForeignKeyWidget(models.Receptor, 'receptor_nombre',))
	legacy_poliza_area			= fields.Field(column_name="legacy_poliza_area", attribute="legacy_poliza_area", widget=ForeignKeyWidget(models.Area, 'area_nombre',))
	legacy_poliza_aseguradora	= fields.Field(column_name="legacy_poliza_aseguradora", attribute="legacy_poliza_aseguradora", widget=ForeignKeyWidget(models.Aseguradora, 'aseguradora_nombre',))
	legacy_poliza_tomador		= fields.Field(column_name="legacy_poliza_tomador", attribute="legacy_poliza_tomador", widget=ForeignKeyWidget(models.Empresa, 'empresa_nombre',))

	class Meta:
		model = models.LegacyPoliza
		fields = (
		"legacy_poliza_fecha",
		"legacy_poliza_expediente",   
		"legacy_poliza_receptor",
		"legacy_poliza_area",
		"legacy_poliza_numero",
		"legacy_poliza_concepto",
		"legacy_poliza_anexo",
		"legacy_poliza_recibo",
		"legacy_poliza_aseguradora",
		"legacy_poliza_tomador",
		"legacy_poliza_obra_nombre",
		"legacy_poliza_obra_convenio",
		"legacy_poliza_obra_expediente",
		"legacy_poliza_monto_pesos",
		"legacy_poliza_monto_uvi",
		"legacy_poliza_creador",
		"legacy_poliza_editor",
		)

class PolizaMovimientoResource(resources.ModelResource):
	poliza_movimiento_receptor 	= fields.Field(column_name="Receptor", attribute="poliza_movimento_receptor", widget=ForeignKeyWidget(models.Receptor, "receptor_nombre",))
	poliza_movimiento_area		= fields.Field(column_name="Area", attribute="poliza_movimiento_area", widget=ForeignKeyWidget(models.Area, "area_nombre",))
	poliza_movimiento_editor	= fields.Field(column_name="Editor", attribute="poliza_movimiento_editor", widget=ForeignKeyWidget(User, "username",))
	poliza_movimiento_numero	= fields.Field(column_name="Poliza", attribute="poliza_movimiento_numero", widget=ForeignKeyWidget(models.Poliza, "poliza_numero",))

class ProgramaResource(resources.ModelResource):
	class Meta:
		model = models.Programa

class DepartamentoResource(resources.ModelResource):
	class Meta:
		model = models.Departamento

class LocalidadResource(resources.ModelResource):
	class Meta:
		model = models.Localidad

class MunicipioResource(resources.ModelResource):
	class Meta:
		model = models.Municipio

class ObraResource(resources.ModelResource):
	class Meta:
		model = models.Obra

class PrototipoResource(resources.ModelResource):
	class Meta:
		model = models.Prototipo

class AgenteResource(resources.ModelResource):
	class Meta:
		model = models.Agente

class CertificadoResource(resources.ModelResource):
	class Meta:
		model = models.Certificado
	
	certificado_obra = fields.Field(column_name="Obra", attribute="obra_nombre", widget=ForeignKeyWidget(models.Obra,"obra_nombre",))

class ConjuntoLicitadoResource(resources.ModelResource):
	class Meta:
		model = models.ConjuntoLicitado
		
class RegionResource(resources.ModelResource):
	class Meta:
		model = models.Region

class CertificadoRubroResource(resources.ModelResource):
	class Meta:
		model = models.CertificadoRubro
	
class FinanciamientoResource(resources.ModelResource):
	class Meta:
		model = models.CertificadoFinanciamiento

class PlandeTrabajosResource(resources.ModelResource):
	class Meta:
		model = models.PlanDeTrabajos

class ContratoResource(resources.ModelResource):
	class Meta:
		model = models.Contrato

class ContratoMontoResource(resources.ModelResource):
	class Meta:
		model = models.ContratoMonto
	
class ContratoRubroResource(resources.ModelResource):
	class Meta:
		model = models.ContratoRubro

class ContratoDigitalResource(resources.ModelResource):
	class Meta:
		model = models.ContratosDigitales

class ResolucionDigitalResource(resources.ModelResource):
	class Meta:
		model = models.ResolucionesDigitales
