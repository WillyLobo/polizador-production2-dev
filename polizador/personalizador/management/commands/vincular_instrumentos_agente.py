"""Vincula los instrumentos heredados (texto) de cada Agente a la Resolucion/Decreto del
IPDUV que les corresponde.

Recorre los conceptos de personalizador/instrumentos.py::CONCEPTOS: si el texto heredado
matchea exactamente un instrumento (ver instrumentos.buscar), setea la FK y vacia el texto
y su tipo. Lo que no matchea queda como dato heredado y se lista en el reporte.

Se puede correr las veces que haga falta (ej. despues de cada sync_resoluciones_sgt /
sync_decretos_sgt, que van cargando instrumentos que antes no estaban).
"""
import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from personalizador.instrumentos import CONCEPTOS, vincular
from personalizador.models import Agente


class Command(BaseCommand):
    help = "Vincula los instrumentos heredados (texto) de los Agentes con Resoluciones/Decretos existentes."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="No guarda cambios, solo informa.")
        parser.add_argument("--csv", help="Ruta de un CSV donde volcar los instrumentos que no se pudieron vincular.")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        vinculados = 0
        pendientes = []

        with transaction.atomic():
            for agente in Agente.objects.filter(Agente.q_instrumentos_sin_vincular()).order_by("agente_apellidos", "agente_nombres"):
                campos = []
                for concepto in CONCEPTOS:
                    texto = getattr(agente, concepto.heredado)
                    resultado, tocados = vincular(agente, concepto)
                    if resultado is None:
                        continue
                    if tocados:
                        vinculados += 1
                        campos += tocados
                        self.stdout.write(f"{agente} | {concepto.label}: {texto} -> {resultado.instrumento}")
                    else:
                        pendientes.append((agente, concepto, texto, resultado.motivo))
                if campos and not dry_run:
                    agente.save(update_fields=campos)
            if dry_run:
                transaction.set_rollback(True)

        if options["csv"]:
            with open(options["csv"], "w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["agente_id", "agente", "dni", "concepto", "valor", "motivo"])
                for agente, concepto, texto, motivo in pendientes:
                    writer.writerow([agente.pk, agente.agente_apellidoynombre_coma, agente.dni, concepto.label, texto, motivo])

        prefijo = "[dry-run] " if dry_run else ""
        self.stdout.write(self.style.SUCCESS(
            f"{prefijo}{vinculados} instrumentos vinculados, {len(pendientes)} quedan sin vincular."
        ))
