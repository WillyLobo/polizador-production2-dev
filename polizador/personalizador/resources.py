from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from personalizador import models

class CargosResource(resources.ModelResource):
    class Meta:
        model = models.Cargos
        
class CargoTipoResource(resources.ModelResource):
    class Meta:
        model = models.CargoTipo

class GerenciaResource(resources.ModelResource):
    class Meta:
        model = models.Gerencia

class DireccionResource(resources.ModelResource):
    class Meta:
        model = models.Direccion

class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = models.Departamento