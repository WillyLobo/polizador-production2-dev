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

class CargosAdmin(SimpleHistoryAdmin):
    model = Cargos
    resource_class = CargosResource
    search_fields = ["cargo_tipo__cargotipo", "cargo_gerencia__gerencia_nombre", "cargo_direccion__direccion_nombre", "cargo_departamento__departamento_nombre"]

class CargoTipoResource(SimpleHistoryAdmin):
    model = CargoTipo
    resource_class = CargoTipoResource


class GerenciaAdmin(SimpleHistoryAdmin):
    model = Gerencia
    resource_class = GerenciaResource

class DireccionAdmin(SimpleHistoryAdmin):
    model = Direccion
    resource_class = DireccionResource

class DepartamentoAdmin(SimpleHistoryAdmin):
    model = Departamento
    resource_class = DepartamentoResource

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Cargos, CargosAdmin)
admin.site.register(CargoTipo, CargoTipoResource)
admin.site.register(Gerencia, GerenciaAdmin)
admin.site.register(Direccion, DireccionAdmin)
admin.site.register(Departamento, DepartamentoAdmin)