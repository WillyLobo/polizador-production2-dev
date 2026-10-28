"""
Grupos de permisos para usar el proyecto QGIS (las colecciones OAPIF de gdu/oapif.py). Los
arma configurar_grupos_qgis y también el ETL, que les asigna los usuarios migrados.
"""
from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission

from gdu.oapif import ColeccionSoloLectura, api

GRUPO_EDITORES = "GDU: Editores QGIS"
GRUPO_LECTORES = "GDU: Lectores QGIS"
# permisos por campo de las UF (ver gdu.oapif.Ufs)
PERMISOS_EXTRA_EDITORES = ["editar_dominio", "editar_nro_adjudicatario"]


class PermisoFaltante(Exception):
    pass


def permisos_de_colecciones():
    """(lectura, edición): los permisos de modelo que piden las colecciones OAPIF publicadas."""
    lectura, edicion = set(), set()
    for coleccion in api.collections.values():
        opts = coleccion.opts
        lectura.add((opts.app_label, f"view_{opts.model_name}"))
        if not isinstance(coleccion, ColeccionSoloLectura):
            edicion |= {(opts.app_label, f"{accion}_{opts.model_name}") for accion in ("add", "change", "delete")}
    return lectura, edicion


def _buscar_permisos(pares):
    permisos = []
    for app_label, codename in sorted(pares):
        try:
            permisos.append(Permission.objects.get(content_type__app_label=app_label, codename=codename))
        except Permission.DoesNotExist:
            raise PermisoFaltante(f"No existe el permiso {app_label}.{codename}: falta correr migrate?")
    return permisos


def configurar_grupos():
    """Crea o actualiza los dos grupos; sus permisos se reemplazan, no se suman. Devuelve
    (editores, lectores)."""
    # los permisos se crean en post_migrate; en una base recién migrada ya están
    for config in apps.get_app_configs():
        create_permissions(config, verbosity=0)
    lectura, edicion = permisos_de_colecciones()
    editores, _ = Group.objects.get_or_create(name=GRUPO_EDITORES)
    editores.permissions.set(_buscar_permisos(lectura | edicion | {("gdu", c) for c in PERMISOS_EXTRA_EDITORES}))
    lectores, _ = Group.objects.get_or_create(name=GRUPO_LECTORES)
    lectores.permissions.set(_buscar_permisos(lectura))
    return editores, lectores
