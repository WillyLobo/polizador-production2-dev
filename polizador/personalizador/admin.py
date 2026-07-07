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
    list_filter = ["sexo", "categoria", "agente_verificado_contra_padron", "agente_es_inpector_obra", "agente_personal_transitorio", "agente_personal_de_gabinete"]
    autocomplete_fields = [
        "agente_usuario",
        "sexo",
        "titulo_profesional",
        "categoria",
        "denominacion_cargo",
        "cargo_interno",
        "apartado",
        "ceic",
        "grupo",
        "actividad_especifica",
        "oficina",
        "domicilio_localidad",
    ]

class GeneroAgenteAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = GeneroAgenteResource
    list_display = ["generoagente_nombre"]
    search_fields = ["generoagente_nombre"]

class TituloProfesionalAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = TituloProfesionalResource
    list_display = ["tituloprofesional_nombre", "tituloprofesional_grado"]
    search_fields = ["tituloprofesional_nombre"]
    list_filter = ["tituloprofesional_grado"]

class CategoriaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CategoriaResource
    list_display = ["categoria_codigo", "categoria_nombre"]
    search_fields = ["categoria_nombre", "categoria_codigo"]

class DenominacionCargoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = DenominacionCargoResource
    list_display = ["denominacion"]
    search_fields = ["denominacion"]

class ApartadoCargoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ApartadoCargoResource
    list_display = ["apartadocargo_denominacion"]
    search_fields = ["apartadocargo_denominacion"]

class CEICAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CEICResource
    list_display = ["ceic"]
    search_fields = ["ceic"]

class GrupoCargoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = GrupoCargoResource
    list_display = ["grupo_numero"]
    search_fields = ["grupo_numero"]

class ActividadEspecificaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ActividadEspecificaResource
    list_display = ["actividad_especifica_codigo", "actividad_especifica_nombre"]
    search_fields = ["actividad_especifica_nombre", "actividad_especifica_codigo"]

class OficinaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = OficinaResource
    list_display = ["__str__", "cargo_tipo", "cargo_directorio", "cargo_gerencia", "cargo_direccion", "cargo_departamento"]
    search_fields = ["cargo_tipo__cargotipo", "cargo_gerencia__gerencia_nombre", "cargo_direccion__direccion_nombre", "cargo_departamento__departamento_nombre"]
    list_filter = ["cargo_tipo", "cargo_gerencia"]
    autocomplete_fields = ["cargo_tipo", "cargo_directorio", "cargo_gerencia", "cargo_direccion", "cargo_departamento"]

class CargoTipoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CargoTipoResource
    list_display = ["cargotipo"]
    search_fields = ["cargotipo"]

class DirectorioAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = DirectorioResource
    list_display = ["directorio_nombre", "directorio_autoridad_a_cargo_fk", "directorio_cuof"]
    search_fields = ["directorio_nombre"]
    autocomplete_fields = ["directorio_autoridad_a_cargo_fk"]

class GerenciaAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = GerenciaResource
    list_display = ["gerencia_nombre", "gerencia_directorio", "gerencia_autoridad_a_cargo_fk", "gerencia_cuof"]
    search_fields = ["gerencia_nombre"]
    list_filter = ["gerencia_directorio"]
    autocomplete_fields = ["gerencia_directorio", "gerencia_autoridad_a_cargo_fk"]

class DireccionAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = DireccionResource
    list_display = ["direccion_nombre", "direccion_directorio", "direccion_gerencia", "direccion_autoridad_a_cargo_fk", "direccion_cuof"]
    search_fields = ["direccion_nombre"]
    list_filter = ["direccion_gerencia"]
    autocomplete_fields = ["direccion_directorio", "direccion_gerencia", "direccion_autoridad_a_cargo_fk"]

class DepartamentoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = DepartamentoResource
    list_display = ["departamento_nombre", "departamento_direccion", "departamento_autoridad_a_cargo_fk", "departamento_cuof"]
    search_fields = ["departamento_nombre"]
    list_filter = ["departamento_gerencia", "departamento_direccion"]
    autocomplete_fields = ["departamento_directorio", "departamento_gerencia", "departamento_direccion", "departamento_autoridad_a_cargo_fk"]

class RepresentanteTecnicoAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = RepresentanteTecnicoResource
    list_display = ["representantetecnico_nombre", "representantetecnico_apellido", "representantetecnico_cuil", "representantetecnico_matricula"]
    search_fields = ["representantetecnico_nombre", "representantetecnico_apellido", "representantetecnico_dni", "representantetecnico_cuil"]
    list_filter = ["representantetecnico_profesion"]
    autocomplete_fields = ["representantetecnico_profesion"]

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
