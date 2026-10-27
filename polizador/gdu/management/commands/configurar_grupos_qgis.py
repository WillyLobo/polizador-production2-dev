from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from gdu.oapif import ColeccionSoloLectura, api

GRUPO_EDITORES = "GDU: Editores QGIS"
GRUPO_LECTORES = "GDU: Lectores QGIS"
# permisos por campo de las UF (ver gdu.oapif.Ufs)
PERMISOS_EXTRA_EDITORES = ["editar_dominio", "editar_nro_adjudicatario"]


def permisos_de_colecciones():
    """(lectura, edición): los permisos de modelo que piden las colecciones OAPIF publicadas."""
    lectura, edicion = set(), set()
    for coleccion in api.collections.values():
        opts = coleccion.opts
        lectura.add((opts.app_label, f"view_{opts.model_name}"))
        if not isinstance(coleccion, ColeccionSoloLectura):
            edicion |= {(opts.app_label, f"{accion}_{opts.model_name}") for accion in ("add", "change", "delete")}
    return lectura, edicion


def buscar_permisos(pares):
    permisos = []
    for app_label, codename in sorted(pares):
        try:
            permisos.append(Permission.objects.get(content_type__app_label=app_label, codename=codename))
        except Permission.DoesNotExist:
            raise CommandError(f"No existe el permiso {app_label}.{codename}: falta correr migrate?")
    return permisos


class Command(BaseCommand):
    """
    Crea (o actualiza) los grupos de QGIS a partir de las colecciones de gdu/oapif.py, así
    una colección nueva queda cubierta con solo volver a correrlo. Idempotente: los
    permisos de los grupos se reemplazan, no se suman.
    """
    help = "Crea los grupos de permisos para editar/consultar las capas GDU desde QGIS (OAPIF)"

    def add_arguments(self, parser):
        parser.add_argument("--editores", nargs="*", default=[], help="usernames a agregar al grupo de editores")
        parser.add_argument("--lectores", nargs="*", default=[], help="usernames a agregar al grupo de lectores")

    @transaction.atomic
    def handle(self, *args, **options):
        # los permisos se crean en post_migrate; en una base recién migrada ya están
        for config in apps.get_app_configs():
            create_permissions(config, verbosity=0)

        lectura, edicion = permisos_de_colecciones()
        editores, _ = Group.objects.get_or_create(name=GRUPO_EDITORES)
        editores.permissions.set(buscar_permisos(lectura | edicion | {("gdu", c) for c in PERMISOS_EXTRA_EDITORES}))
        lectores, _ = Group.objects.get_or_create(name=GRUPO_LECTORES)
        lectores.permissions.set(buscar_permisos(lectura))

        User = get_user_model()
        for grupo, usernames in ((editores, options["editores"]), (lectores, options["lectores"])):
            for username in usernames:
                try:
                    User.objects.get(username=username).groups.add(grupo)
                except User.DoesNotExist:
                    raise CommandError(f"No existe el usuario {username}")
            self.stdout.write(f"{grupo.name}: {grupo.permissions.count()} permisos, {grupo.user_set.count()} usuarios")
