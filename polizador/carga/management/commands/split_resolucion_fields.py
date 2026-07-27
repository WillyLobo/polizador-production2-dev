import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from carga.models import Contrato, ConjuntoLicitado, Obra

# (model, campo de texto libre legado, prefijo de los campos nuevos)
MODELOS_A_MIGRAR = (
    (Obra, "obra_resolucion", "obra_resolucion"),
    (ConjuntoLicitado, "conjunto_resolucion", "conjunto_resolucion"),
    (Contrato, "contrato_resolucion", "contrato_resolucion"),
)


class Command(BaseCommand):
    help = (
        "Backfillea los campos separados (tipo/año/número/jurisdicción/acta) de las "
        "resoluciones cargadas a mano en Obra/ConjuntoLicitado/Contrato. Dos fuentes: "
        "(1) el campo de texto libre legado ('numero-año', 'numero-acta-año' o "
        "'año-numero-jurisdiccion-acta'), para los registros sin FK; (2) el propio "
        "InstrumentosLegalesResoluciones vinculado, para los registros que ya tienen "
        "*_resolucion_fk (donde el texto legado nunca se completó, o directamente no "
        "aplica). No modifica el campo legado. Corre en modo dry-run por default, "
        "pasar --commit para persistir."
    )

    def add_arguments(self, parser):
        parser.add_argument("--commit", action="store_true", help="Persiste los cambios (sin esto, sólo reporta).")
        parser.add_argument(
            "--reporte-csv", default=None,
            help="Ruta de archivo CSV donde volcar los registros que no se pudieron "
                 "interpretar (o que requieren revisión manual del tipo), para revisión.",
        )

    def handle(self, *args, **options):
        commit = options["commit"]
        reporte_csv = options["reporte_csv"] or f"split_resolucion_fields_pendientes_{datetime.now():%Y%m%d_%H%M%S}.csv"

        total_migrados = 0
        total_saltados = 0
        pendientes = []

        with transaction.atomic():
            for model, campo_legado, prefijo in MODELOS_A_MIGRAR:
                migrados = 0
                saltados = 0
                queryset = model.objects.filter(**{
                    f"{prefijo}_fk__isnull": True,
                    f"{prefijo}_ano": "",
                    f"{prefijo}_numero": "",
                }).exclude(**{campo_legado: ""}).exclude(**{f"{campo_legado}__isnull": True})

                for instance in queryset:
                    valor = getattr(instance, campo_legado)
                    partes = valor.split("-")

                    if not all(p.isdigit() for p in partes):
                        pendientes.append((model.__name__, instance.pk, valor, "partes no numéricas"))
                        saltados += 1
                        continue

                    if len(partes) == 2:
                        numero, ano = partes
                        tipo, acta, jurisdiccion = "P", "1", "10"
                    elif len(partes) == 3:
                        numero, acta, ano = partes
                        tipo, jurisdiccion = "D", "10"
                    elif len(partes) == 4:
                        ano, numero, jurisdiccion, acta = partes
                        tipo = "P" if acta == "1" else "D"
                        pendientes.append((
                            model.__name__, instance.pk, valor,
                            "formato ya nuevo: revisar tipo inferido por heurística",
                        ))
                    else:
                        pendientes.append((model.__name__, instance.pk, valor, "cantidad de partes inesperada"))
                        saltados += 1
                        continue

                    setattr(instance, f"{prefijo}_tipo", tipo)
                    setattr(instance, f"{prefijo}_ano", ano)
                    setattr(instance, f"{prefijo}_numero", numero)
                    setattr(instance, f"{prefijo}_jurisdiccion", jurisdiccion)
                    setattr(instance, f"{prefijo}_acta", acta)
                    self.stdout.write(
                        f"{model.__name__} [pk={instance.pk}]: {valor!r} -> "
                        f"tipo={tipo} año={ano} numero={numero} jurisdiccion={jurisdiccion} acta={acta}"
                    )
                    if commit:
                        instance.save(update_fields=[
                            f"{prefijo}_tipo", f"{prefijo}_ano", f"{prefijo}_numero",
                            f"{prefijo}_jurisdiccion", f"{prefijo}_acta",
                        ])
                    migrados += 1

                queryset_fk = model.objects.select_related(f"{prefijo}_fk").filter(**{
                    f"{prefijo}_fk__isnull": False,
                    f"{prefijo}_ano": "",
                    f"{prefijo}_numero": "",
                })
                for instance in queryset_fk:
                    resolucion = getattr(instance, f"{prefijo}_fk")
                    tipo = resolucion.instrumentolegalresoluciones_tipo
                    ano = resolucion.instrumentolegalresoluciones_ano
                    numero = resolucion.instrumentolegalresoluciones_numero
                    jurisdiccion = "10"
                    acta = resolucion.instrumentolegalresoluciones_acta if tipo == "D" else "1"

                    setattr(instance, f"{prefijo}_tipo", tipo)
                    setattr(instance, f"{prefijo}_ano", ano)
                    setattr(instance, f"{prefijo}_numero", numero)
                    setattr(instance, f"{prefijo}_jurisdiccion", jurisdiccion)
                    setattr(instance, f"{prefijo}_acta", acta)
                    self.stdout.write(
                        f"{model.__name__} [pk={instance.pk}]: vinculado a {resolucion!s} -> "
                        f"tipo={tipo} año={ano} numero={numero} jurisdiccion={jurisdiccion} acta={acta}"
                    )
                    if commit:
                        instance.save(update_fields=[
                            f"{prefijo}_tipo", f"{prefijo}_ano", f"{prefijo}_numero",
                            f"{prefijo}_jurisdiccion", f"{prefijo}_acta",
                        ])
                    migrados += 1

                self.stdout.write(self.style.SUCCESS(f"{model.__name__}: {migrados} migrado(s), {saltados} saltado(s)"))
                total_migrados += migrados
                total_saltados += saltados

            if not commit:
                self.stdout.write(self.style.WARNING("Dry-run: no se guardó ningún cambio (pasar --commit para persistir)."))
                transaction.set_rollback(True)

        if pendientes:
            with open(reporte_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["modelo", "pk", "valor_legado", "motivo"])
                writer.writerows(pendientes)
            self.stdout.write(self.style.WARNING(f"{len(pendientes)} registro(s) para revisión manual en: {reporte_csv}"))

        self.stdout.write(self.style.SUCCESS(f"Total: {total_migrados} migrado(s), {total_saltados} saltado(s)"))
