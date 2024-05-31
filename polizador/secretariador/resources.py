from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from secretariador import models
from carga.models import Aseguradora

class OrganigramaResource(resources.ModelResource):
	class Meta:
		model = models.Organigrama

class ComisionadoResource(resources.ModelResource):
	class Meta:
		model = models.Comisionado

class VehiculoResource(resources.ModelResource):
	class Meta:
		model = models.Vehiculo

vehiculo_poliza_aseguradora			= fields.Field(column_name="aseguradora_nombre", attribute="vehiculo_poliza_aseguradora", widget=ForeignKeyWidget(Aseguradora,"aseguradora_nombre",))

class IncorporacionResource(resources.ModelResource):
	class Meta:
		model = models.Incorporacion
