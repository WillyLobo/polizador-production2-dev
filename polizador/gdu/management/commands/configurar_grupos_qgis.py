from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from gdu.grupos_qgis import PermisoFaltante, configurar_grupos


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
        try:
            editores, lectores = configurar_grupos()
        except PermisoFaltante as e:
            raise CommandError(str(e))

        User = get_user_model()
        for grupo, usernames in ((editores, options["editores"]), (lectores, options["lectores"])):
            for username in usernames:
                try:
                    User.objects.get(username=username).groups.add(grupo)
                except User.DoesNotExist:
                    raise CommandError(f"No existe el usuario {username}")
            self.stdout.write(f"{grupo.name}: {grupo.permissions.count()} permisos, {grupo.user_set.count()} usuarios")
