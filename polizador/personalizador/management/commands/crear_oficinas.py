from django.core.management.base import BaseCommand
from django.db import transaction

from personalizador.models import Departamento, Direccion, Directorio, Gerencia, Oficina


class Command(BaseCommand):
    help = (
        "Crea una Oficina por cada Directorio, Gerencia, Direccion y Departamento "
        "existente que todavia no tenga una propia, derivando los niveles "
        "superiores de la jerarquia (Directorio > Gerencia > Direccion > "
        "Departamento) a partir de ese nodo. Es re-ejecutable: los nodos que ya "
        "tienen su Oficina se saltean, asi que se puede correr de nuevo cada vez "
        "que se cargan Directorios/Gerencias/Direcciones/Departamentos nuevos."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Solo informa cuantas Oficinas se crearian, sin guardar nada.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        counts = {"directorio": 0, "gerencia": 0, "direccion": 0, "departamento": 0}

        with transaction.atomic():
            for directorio in Directorio.objects.all():
                ya_existe = Oficina.objects.filter(
                    cargo_directorio=directorio,
                    cargo_gerencia__isnull=True,
                    cargo_direccion__isnull=True,
                    cargo_departamento__isnull=True,
                ).exists()
                if ya_existe:
                    continue
                counts["directorio"] += 1
                if not dry_run:
                    Oficina.objects.create(cargo_directorio=directorio)

            for gerencia in Gerencia.objects.all():
                ya_existe = Oficina.objects.filter(
                    cargo_gerencia=gerencia,
                    cargo_direccion__isnull=True,
                    cargo_departamento__isnull=True,
                ).exists()
                if ya_existe:
                    continue
                counts["gerencia"] += 1
                if not dry_run:
                    Oficina.objects.create(
                        cargo_gerencia=gerencia,
                        cargo_directorio=gerencia.gerencia_directorio,
                    )

            for direccion in Direccion.objects.select_related("direccion_gerencia"):
                ya_existe = Oficina.objects.filter(
                    cargo_direccion=direccion,
                    cargo_departamento__isnull=True,
                ).exists()
                if ya_existe:
                    continue
                counts["direccion"] += 1
                if not dry_run:
                    gerencia = direccion.direccion_gerencia
                    directorio = direccion.direccion_directorio or (
                        gerencia.gerencia_directorio if gerencia else None
                    )
                    Oficina.objects.create(
                        cargo_direccion=direccion,
                        cargo_gerencia=gerencia,
                        cargo_directorio=directorio,
                    )

            for departamento in Departamento.objects.select_related(
                "departamento_direccion__direccion_gerencia",
                "departamento_gerencia",
                "departamento_directorio",
            ):
                if Oficina.objects.filter(cargo_departamento=departamento).exists():
                    continue
                counts["departamento"] += 1
                if not dry_run:
                    direccion = departamento.departamento_direccion
                    gerencia = departamento.departamento_gerencia or (
                        direccion.direccion_gerencia if direccion else None
                    )
                    directorio = (
                        departamento.departamento_directorio
                        or (gerencia.gerencia_directorio if gerencia else None)
                        or (direccion.direccion_directorio if direccion else None)
                    )
                    Oficina.objects.create(
                        cargo_departamento=departamento,
                        cargo_direccion=direccion,
                        cargo_gerencia=gerencia,
                        cargo_directorio=directorio,
                    )

            if dry_run:
                transaction.set_rollback(True)

        verbo = "se crearian" if dry_run else "creadas"
        self.stdout.write(self.style.SUCCESS(f"Oficinas de Directorio {verbo}: {counts['directorio']}"))
        self.stdout.write(self.style.SUCCESS(f"Oficinas de Gerencia {verbo}: {counts['gerencia']}"))
        self.stdout.write(self.style.SUCCESS(f"Oficinas de Direccion {verbo}: {counts['direccion']}"))
        self.stdout.write(self.style.SUCCESS(f"Oficinas de Departamento {verbo}: {counts['departamento']}"))
