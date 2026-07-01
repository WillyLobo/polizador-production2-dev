from django.contrib import admin
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin

from personalizador.models import *
from personalizador.resources import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'usuario_dni']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('usuario_dni',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('usuario_dni',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class AgenteAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = AgenteResource
    list_display = ["agente_nombreyapellido", "dni", "n_legajo", "categoria", "oficina"]
    search_fields = ["agente_nombres", "agente_apellidos", "dni", "cuil"]

class GeneroAgenteAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = GeneroAgenteResource
    list_display = ["generoagente_nombre"]

class TituloProfesionalAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = TituloProfesionalResource
    list_display = ["tituloprofesional_nombre", "tituloprofesional_grado"]
    search_fields = ["tituloprofesional_nombre"]

class CategoriaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CategoriaResource
    list_display = ["categoria_codigo", "categoria_nombre"]

class DenominacionCargoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = DenominacionCargoResource
    list_display = ["denominacion"]

class ApartadoCargoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ApartadoCargoResource
    list_display = ["apartadocargo_denominacion"]

class CEICAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CEICResource
    list_display = ["ceic"]

class GrupoCargoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = GrupoCargoResource
    list_display = ["grupo_numero"]

class ActividadEspecificaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ActividadEspecificaResource
    list_display = ["actividad_especifica_codigo", "actividad_especifica_nombre"]

class OficinaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = OficinaResource
    list_display = ["__str__", "cargo_tipo", "cargo_gerencia", "cargo_direccion", "cargo_departamento"]

class CargoTipoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CargoTipoResource
    list_display = ["cargotipo"]

class DirectorioAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = DirectorioResource
    list_display = ["directorio_nombre", "directorio_cuof"]

class GerenciaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = GerenciaResource
    list_display = ["gerencia_nombre", "gerencia_directorio", "gerencia_cuof"]

class DireccionAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = DireccionResource
    list_display = ["direccion_nombre", "direccion_gerencia", "direccion_cuof"]

class DepartamentoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = DepartamentoResource
    list_display = ["departamento_nombre", "departamento_direccion", "departamento_cuof"]

class RepresentanteTecnicoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = RepresentanteTecnicoResource
    list_display = ["representantetecnico_nombre", "representantetecnico_apellido", "representantetecnico_cuil", "representantetecnico_matricula"]

admin.site.register(Agente, AgenteAdmin)
admin.site.register(GeneroAgente, GeneroAgenteAdmin)
admin.site.register(TituloProfesional, TituloProfesionalAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(DenominacionCargo, DenominacionCargoAdmin)
admin.site.register(ApartadoCargo, ApartadoCargoAdmin)
admin.site.register(CEIC, CEICAdmin)
admin.site.register(GrupoCargo, GrupoCargoAdmin)
admin.site.register(ActividadEspecifica, ActividadEspecificaAdmin)
admin.site.register(Oficina, OficinaAdmin)
admin.site.register(CargoTipo, CargoTipoAdmin)
admin.site.register(Directorio, DirectorioAdmin)
admin.site.register(Gerencia, GerenciaAdmin)
admin.site.register(Direccion, DireccionAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(RepresentanteTecnico, RepresentanteTecnicoAdmin)
