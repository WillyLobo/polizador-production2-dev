from django.contrib import admin
from import_export.admin import ImportExportMixin

from personalizador.models import *
from personalizador.resources import *

class CargosAdmin(admin.ModelAdmin):
    model = Cargos
    resource_class = CargosResource

class CargoTipoResource(admin.ModelAdmin):
    model = CargoTipo
    resource_class = CargoTipoResource

class GerenciaAdmin(admin.ModelAdmin):
    model = Gerencia
    resource_class = GerenciaResource

class DireccionAdmin(admin.ModelAdmin):
    model = Direccion
    resource_class = DireccionResource

class DepartamentoAdmin(admin.ModelAdmin):
    model = Departamento
    resource_class = DepartamentoResource

admin.site.register(Cargos, CargosAdmin)
admin.site.register(CargoTipo, CargoTipoResource)
admin.site.register(Gerencia, GerenciaAdmin)
admin.site.register(Direccion, DireccionAdmin)
admin.site.register(Departamento, DepartamentoAdmin)