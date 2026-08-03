"""
Corre ANTES de aplicar la migración 0015 (que convierte *_numero de
InstrumentosLegalesResoluciones/Decretos/Memorandum de CharField a
PositiveIntegerField) contra la base de producción.

Esa migración genera un `ALTER COLUMN ... TYPE integer USING columna::integer`.
Si una sola fila tiene un valor que Postgres no puede castear a entero (vacío,
con espacios, letras, etc.), el ALTER COLUMN entero falla y la migración no se
aplica -- Django corre las migraciones dentro de una transacción, así que no
hay pérdida de datos, pero mejor encontrarlo acá que en medio del deploy.

Uso:
    python manage.py auditar_numeros_instrumentos
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from secretariador.models import (
    InstrumentosLegalesDecretos,
    InstrumentosLegalesMemorandum,
    InstrumentosLegalesResoluciones,
)

MODELOS_Y_CAMPOS = [
    (InstrumentosLegalesResoluciones, "instrumentolegalresoluciones_numero"),
    (InstrumentosLegalesDecretos, "instrumentolegaldecretos_numero"),
    (InstrumentosLegalesMemorandum, "instrumentolegalmemorandum_numero"),
]


class Command(BaseCommand):
    help = (
        "Audita si hay valores no numéricos en los campos *_numero de Instrumentos "
        "Legales, antes de aplicar la migración que los convierte a entero."
    )

    def handle(self, *args, **options):
        hubo_problemas = False

        for modelo, campo in MODELOS_Y_CAMPOS:
            tabla = modelo._meta.db_table
            columna = modelo._meta.get_field(campo).column
            total = modelo.objects.count()

            with connection.cursor() as cursor:
                cursor.execute(
                    f'SELECT id, "{columna}" FROM "{tabla}" '
                    f"WHERE \"{columna}\"::text !~ '^[0-9]+$' "
                    f"ORDER BY id"
                )
                filas = cursor.fetchall()

            if filas:
                hubo_problemas = True
                self.stdout.write(self.style.ERROR(
                    f"{modelo.__name__}: {len(filas)} de {total} fila(s) con "
                    f"'{campo}' no numérico:"
                ))
                for pk, valor in filas[:50]:
                    self.stdout.write(f"    id={pk}  {campo}={valor!r}")
                if len(filas) > 50:
                    self.stdout.write(f"    ... y {len(filas) - 50} más.")
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"{modelo.__name__}: {total} fila(s), todas castean limpio a entero."
                ))

        if hubo_problemas:
            self.stdout.write(self.style.ERROR(
                "\nHay valores que van a hacer fallar el ALTER COLUMN de la migración "
                "0015. Corregirlos a mano antes de correr 'python manage.py migrate'."
            ))
            raise CommandError("Auditoría encontró valores no numéricos.")

        self.stdout.write(self.style.SUCCESS(
            "\nOK: no hay valores que rompan el cast a entero. Se puede migrar."
        ))
