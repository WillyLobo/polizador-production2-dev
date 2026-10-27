from django.apps import apps
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from gdu.models import Catastrourbano


class SoloLecturaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Catastrourbano es referencia provincial de solo lectura: lo carga el ETL, nadie lo edita.
admin.site.register(Catastrourbano, SoloLecturaAdmin)

for model in apps.get_app_config("gdu").get_models():
    if admin.site.is_registered(model) or model.__name__.startswith("Historical"):
        continue
    admin.site.register(model, SimpleHistoryAdmin if hasattr(model, "history") else admin.ModelAdmin)
