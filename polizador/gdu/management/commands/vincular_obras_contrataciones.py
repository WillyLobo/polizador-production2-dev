import csv
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

from carga.models import Obra
from gdu.matching import normalizar_expediente
from gdu.models import Contratacion, ObraContratacion


class Command(BaseCommand):
    """
    Vincula carga.Obra con gdu.Contratacion (catastro.contratacion) haciendo matching
    por expediente normalizado. El expediente es texto libre en ambos lados y catastro
    trae mucho ruido ('SIN DATOS', notas entre paréntesis, saltos de línea), así que el
    match automático sólo cubre una fracción de los casos: el resto se resuelve con el
    mismo flujo de CSV de corrección manual que usa migrar_usuarios_gdu.py para
    VisualizadorUser <-> Agente.
    """
    help = "Vincula carga.Obra con gdu.Contratacion por expediente, con flujo de corrección manual por CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv-sin-match",
            default="sin_match_obra_contratacion.csv",
            help="Ruta del CSV donde se listan las obras sin match único (default: sin_match_obra_contratacion.csv)",
        )
        parser.add_argument(
            "--csv-correcciones",
            default=None,
            help=(
                "Ruta a un CSV previamente generado por --csv-sin-match con la columna "
                "'contratacion_id_manual' completada a mano. Las filas con ese campo lleno se "
                "toman como match único, en vez de volver a intentar el matching automático."
            ),
        )
        parser.add_argument(
            "--completar-match-obra",
            action="store_true",
            help=(
                "Además de reportar, persiste ObraContratacion para las obras con match único "
                "(automático o tomado de --csv-correcciones)."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        candidatos_por_expediente = defaultdict(set)
        for contratacion_id, expediente in Contratacion.objects.values_list("id", "expediente"):
            clave = normalizar_expediente(expediente)
            if clave is not None:
                candidatos_por_expediente[clave].add(contratacion_id)

        ids_contratacion_validos = {
            cid for ids in candidatos_por_expediente.values() for cid in ids
        }
        correcciones = self._leer_csv_correcciones(
            options["csv_correcciones"], ids_contratacion_validos,
        ) if options["csv_correcciones"] else {}

        vinculados_existentes = set(ObraContratacion.objects.values_list("obra_id", flat=True))

        unicos = ambiguos = sin_match = corregidos = vinculados = 0
        a_revisar = []
        a_revisar_csv = []
        for obra in Obra.objects.exclude(obra_expediente=""):
            if obra.id in correcciones:
                candidatos_ids = {correcciones[obra.id]}
                corregidos += 1
            else:
                clave = normalizar_expediente(obra.obra_expediente)
                candidatos_ids = candidatos_por_expediente.get(clave, set()) if clave else set()
            cantidad = len(candidatos_ids)

            if cantidad == 1:
                unicos += 1
                if options["completar_match_obra"]:
                    contratacion_id = next(iter(candidatos_ids))
                    vinculados += self._vincular(
                        obra, contratacion_id, obra.id in correcciones, obra.id in vinculados_existentes,
                    )
            elif cantidad == 0:
                sin_match += 1
                a_revisar.append(f"Obra #{obra.id} '{obra.obra_expediente}': sin candidatos")
                a_revisar_csv.append((obra, candidatos_ids))
            else:
                ambiguos += 1
                a_revisar.append(f"Obra #{obra.id} '{obra.obra_expediente}': {cantidad} candidatos")
                a_revisar_csv.append((obra, candidatos_ids))

        self.stdout.write(self.style.WARNING(
            f"Match Obra -> Contratacion: {unicos} único, {ambiguos} ambiguos, "
            f"{sin_match} sin match ({corregidos} tomados de {options['csv_correcciones']})."
        ))
        for item in a_revisar:
            self.stdout.write(f"  - {item}")

        if options["completar_match_obra"]:
            self.stdout.write(self.style.SUCCESS(
                f"ObraContratacion creado/actualizado para {vinculados} de {unicos} matches únicos."
            ))

        self._escribir_csv_sin_match(options["csv_sin_match"], a_revisar_csv)
        self.stdout.write(self.style.SUCCESS(
            f"CSV de obras sin match o ambiguas escrito en '{options['csv_sin_match']}' ({len(a_revisar_csv)} filas)."
        ))

    def _vincular(self, obra, contratacion_id, es_manual, ya_vinculada):
        """
        Persiste ObraContratacion para un match único. No pisa un vínculo existente
        hacia otra contratación (podría ser una corrección previa hecha a mano).
        """
        if ya_vinculada:
            existente = ObraContratacion.objects.get(obra_id=obra.id)
            if existente.contratacion_id != contratacion_id:
                self.stderr.write(self.style.WARNING(
                    f"Obra #{obra.id} ya está vinculada a otra contratación "
                    f"(#{existente.contratacion_id}), se omite."
                ))
            return 0

        ObraContratacion.objects.create(
            obra=obra, contratacion_id=contratacion_id, vinculado_manualmente=es_manual,
        )
        return 1

    def _leer_csv_correcciones(self, ruta, ids_contratacion_validos):
        """
        Lee un CSV con el formato generado por _escribir_csv_sin_match (columnas
        obra_id, obra_nombre, obra_expediente, candidatos_ids, contratacion_id_manual)
        y devuelve {obra_id: contratacion_id} sólo para las filas donde se completó
        contratacion_id_manual con un id de Contratacion que existe.
        """
        correcciones = {}
        with open(ruta, newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                valor = (fila.get("contratacion_id_manual") or "").strip()
                if not valor:
                    continue
                obra_id = int(fila["obra_id"])
                contratacion_id = int(valor)
                if contratacion_id not in ids_contratacion_validos:
                    self.stderr.write(self.style.WARNING(
                        f"'{ruta}': obra_id={obra_id} referencia contratacion_id={contratacion_id} "
                        "que no existe, se ignora."
                    ))
                    continue
                correcciones[obra_id] = contratacion_id
        return correcciones

    def _escribir_csv_sin_match(self, ruta, filas):
        """
        `filas` es una lista de (Obra, candidatos_ids) — tanto las que quedaron sin
        ningún candidato como las ambiguas (más de uno), para poder revisar y completar
        'contratacion_id_manual' a mano en ambos casos.
        """
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "obra_id", "obra_nombre", "obra_expediente",
                "candidatos_ids", "contratacion_id_manual",
            ])
            for obra, candidatos_ids in filas:
                writer.writerow([
                    obra.id,
                    obra.obra_nombre,
                    obra.obra_expediente,
                    ",".join(str(cid) for cid in sorted(candidatos_ids)),
                    "",
                ])
