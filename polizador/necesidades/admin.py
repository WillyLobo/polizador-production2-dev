from django.contrib import admin

from necesidades.models import Apoyo, Necesidad


class ApoyoInline(admin.TabularInline):
    model = Apoyo
    extra = 0


@admin.register(Necesidad)
class NecesidadAdmin(admin.ModelAdmin):
    list_display = ["titulo", "modulo", "urgencia", "estado", "autor_nombre", "creado"]
    list_filter = ["estado", "modulo", "urgencia", "tipo"]
    search_fields = ["titulo", "detalle", "ejemplo", "autor_username", "autor_nombre"]
    inlines = [ApoyoInline]
