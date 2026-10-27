from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from gdu.etl.importador import Importador


class Command(BaseCommand):
    """
    Carga los datos de la base GDU heredada (Hasura) en los modelos de gdu. La fuente es
    una base scratch donde se restauró el dump de Hasura, p. ej.:

        createdb gdu_legacy
        sudo -u postgres psql -d gdu_legacy -c "CREATE EXTENSION postgis; CREATE EXTENSION pgcrypto;"
        psql -d gdu_legacy -f db-schema.sql   # los errores de OWNER y de postgis_raster son esperables

        python manage.py importar_gdu_legacy --legacy-dsn "postgresql://usuario:clave@127.0.0.1/gdu_legacy"

    Vacía y recarga todas las tablas de gdu en una transacción (es repetible). Deja en
    --salida el reporte de conciliación (.md) y el detalle de incidencias (.csv).
    """
    help = "Importa los datos de la base GDU heredada (dump de Hasura restaurado) a los modelos de gdu"

    def add_arguments(self, parser):
        parser.add_argument("--legacy-dsn", required=True, help="DSN de la base con el dump de Hasura restaurado")
        parser.add_argument("--salida", default=".", help="Directorio para el reporte y las incidencias")
        parser.add_argument(
            "--dry-run", action="store_true", help="Corre todo y genera el reporte, pero descarta los cambios",
        )

    def handle(self, *args, **options):
        salida = Path(options["salida"])
        salida.mkdir(parents=True, exist_ok=True)
        importador = Importador(options["legacy_dsn"], log=self.stdout.write)
        reporte = importador.ejecutar(dry_run=options["dry_run"])

        marca = timezone.localtime().strftime("%Y%m%d-%H%M%S")
        ruta_md = salida / f"reporte_etl_gdu_{marca}.md"
        ruta_csv = salida / f"incidencias_etl_gdu_{marca}.csv"
        ruta_md.write_text(reporte.markdown(), encoding="utf-8")
        reporte.escribir_csv(ruta_csv)

        estilo = self.style.WARNING if reporte.descartes else self.style.SUCCESS
        self.stdout.write(estilo(
            f"Listo: {reporte.descartes} filas descartadas, {len(reporte.filas)} incidencias en total."
        ))
        self.stdout.write(f"Reporte: {ruta_md}\nIncidencias: {ruta_csv}")
