import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from carga.models import Contrato, ConjuntoLicitado, Obra

# (model, field name, field label for output)
FIELDS_TO_FIX = (
    (Obra, "obra_resolucion", "Obra.obra_resolucion"),
    (ConjuntoLicitado, "conjunto_resolucion", "ConjuntoLicitado.conjunto_resolucion"),
    (Contrato, "contrato_resolucion", "Contrato.contrato_resolucion"),
)


class Command(BaseCommand):
    help = (
        "Normaliza numeración de resoluciones cargadas a mano (CharField, no las que apuntan a "
        "InstrumentosLegalesResoluciones via FK) reemplazando '/' por '-', para adoptar la "
        "convencion RES-AAAA-NUMERO-JURISDICCION-ACTA. Genera un CSV con el detalle de los cambios."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Muestra los cambios que se harían sin guardarlos.",
        )
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Ruta del CSV de salida (default: fix_obra_resolucion_numbers_<timestamp>.csv)",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        output_path = options["output"] or f"fix_obra_resolucion_numbers_{datetime.now():%Y%m%d_%H%M%S}.csv"
        total_updated = 0
        changes = []

        with transaction.atomic():
            for model, field_name, label in FIELDS_TO_FIX:
                updated = 0
                queryset = model.objects.filter(**{f"{field_name}__contains": "/"})
                for instance in queryset:
                    old_value = getattr(instance, field_name)
                    new_value = old_value.replace("/", "-")
                    if new_value == old_value:
                        continue
                    self.stdout.write(f"{label} [pk={instance.pk}]: {old_value!r} -> {new_value!r}")
                    changes.append((model.__name__, field_name, instance.pk, old_value, new_value))
                    setattr(instance, field_name, new_value)
                    if not dry_run:
                        instance.save(update_fields=[field_name])
                    updated += 1

                self.stdout.write(self.style.SUCCESS(f"{label}: {updated} registro(s) actualizado(s)"))
                total_updated += updated

            if dry_run and total_updated:
                self.stdout.write(self.style.WARNING("Dry-run: no se guardó ningún cambio."))
                transaction.set_rollback(True)

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["modelo", "campo", "pk", "valor_anterior", "valor_nuevo"])
            writer.writerows(changes)

        self.stdout.write(self.style.SUCCESS(f"Total: {total_updated} registro(s) actualizado(s)"))
        self.stdout.write(self.style.SUCCESS(f"Detalle guardado en: {output_path}"))
