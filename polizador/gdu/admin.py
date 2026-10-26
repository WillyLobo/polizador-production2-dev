from django.apps import apps
from django.contrib import admin

from gdu.models import GjRegistros

# GjRegistros: tabla de una sola columna json sin PK real; Postgres no puede ordenar
# ni comparar json, así que el changelist (ORDER BY -pk) y el change view (WHERE gj = ...) fallan.
EXCLUIDOS = {GjRegistros}

for model in apps.get_app_config("gdu").get_models():
    if model not in EXCLUIDOS:
        admin.site.register(model)
