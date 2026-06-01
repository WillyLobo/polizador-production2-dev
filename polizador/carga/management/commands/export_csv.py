from django.core.management.base import BaseCommand
import os
import csv
from django.apps import apps
from import_export import resources


def get_resource(model_class):
    class DynamicResource(resources.ModelResource):
        class Meta:
            model = model_class
            export_order = [f.name for f in model_class._meta.fields]

    return DynamicResource


class Command(BaseCommand):
    help = 'Exporta todos los modelos de las apps carga, secretariador y personalizador a archivos CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apps',
            type=str,
            default='carga,secretariador,personalizador',
            help='Apps separadas por coma (ej: carga,secretariador)'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='csv_exports',
            help='Directorio de salida para los archivos CSV'
        )

    def handle(self, *args, **options):
        apps_list = [a.strip() for a in options['apps'].split(',')]
        output_dir = options['output_dir']
        os.makedirs(output_dir, exist_ok=True)

        total_files = []

        for app_label in apps_list:
            try:
                app_config = apps.get_app_config(app_label)
            except LookupError:
                self.stderr.write(self.style.ERROR(f"App '{app_label}' no encontrada"))
                continue

            models = sorted(
                [m for m in app_config.get_models() if hasattr(m, '_meta')],
                key=lambda m: m.__name__
            )

            if not models:
                self.stderr.write(self.style.WARNING(f"No hay modelos en '{app_label}'"))
                continue

            self.stdout.write(f"\nApp: {app_label} ({len(models)} modelos)")

            for model in models:
                try:
                    resource = get_resource(model)
                    queryset = model.objects.all()
                    dataset = resource().export(queryset)

                    filename = model.__name__.lower() + '.csv'
                    filepath = os.path.join(output_dir, filename)

                    with open(filepath, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        if dataset.headers:
                            writer.writerow(dataset.headers)
                        for row in dataset:
                            writer.writerow(list(row))

                    count = queryset.count()
                    self.stdout.write(
                        self.style.SUCCESS(f"  {model.__name__} -> {filepath} ({count} registros)")
                    )
                    total_files.append(filepath)

                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"  Error exportando {model.__name__}: {e}")
                    )

        self.stdout.write(
            self.style.SUCCESS(f"\nExportacion completada. {len(total_files)} archivos en '{output_dir}/'")
        )
