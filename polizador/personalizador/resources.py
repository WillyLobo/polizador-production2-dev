from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from personalizador import models

class AgenteResource(resources.ModelResource):
    class Meta:
        model = models.Agente

class GeneroAgenteResource(resources.ModelResource):
    class Meta:
        model = models.GeneroAgente

class TituloProfesionalResource(resources.ModelResource):
    class Meta:
        model = models.TituloProfesional

class CategoriaResource(resources.ModelResource):
    class Meta:
        model = models.Categoria

class DenominacionCargoResource(resources.ModelResource):
    class Meta:
        model = models.DenominacionCargo

class ApartadoCargoResource(resources.ModelResource):
    class Meta:
        model = models.ApartadoCargo

class CEICResource(resources.ModelResource):
    class Meta:
        model = models.CEIC

class GrupoCargoResource(resources.ModelResource):
    class Meta:
        model = models.GrupoCargo

class ActividadEspecificaResource(resources.ModelResource):
    class Meta:
        model = models.ActividadEspecifica

class OficinaResource(resources.ModelResource):
    class Meta:
        model = models.Oficina

class CargoTipoResource(resources.ModelResource):
    class Meta:
        model = models.CargoTipo

class DirectorioResource(resources.ModelResource):
    class Meta:
        model = models.Directorio

class GerenciaResource(resources.ModelResource):
    class Meta:
        model = models.Gerencia

class DireccionResource(resources.ModelResource):
    class Meta:
        model = models.Direccion

class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = models.Departamento

class RepresentanteTecnicoResource(resources.ModelResource):

    class Meta:
        model = models.RepresentanteTecnico