"""
Elimina registros viejos de FormValidationError (POST crudo de forms invalidos,
capturado por core.mixins.LogInvalidFormMixin). Pensado para correr por cron,
no expuesto en el panel web de "Ejecutar comandos": es un borrado en bloque de
datos sensibles y no debe quedar a un boton en la UI.

    python manage.py purgar_errores_validacion
    python manage.py purgar_errores_validacion --dias 30
    python manage.py purgar_errores_validacion --dry-run
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import FormValidationError


class Command(BaseCommand):
    help = "Elimina FormValidationError con mas de N dias de antiguedad (default 90)."

    def add_arguments(self, parser):
        parser.add_argument("--dias", type=int, default=90)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=options["dias"])
        qs = FormValidationError.objects.filter(created_at__lt=cutoff)
        count = qs.count()
        if options["dry_run"]:
            self.stdout.write(f"{count} registros elegibles para borrar (dry-run, no se borro nada)")
            return
        qs.delete()
        self.stdout.write(f"{count} registros eliminados")
