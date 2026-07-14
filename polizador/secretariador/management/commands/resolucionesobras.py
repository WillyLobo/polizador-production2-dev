import os
import re
from datetime import datetime

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from carga.models import Contrato, ConjuntoLicitado, Obra
from secretariador.models import InstrumentosLegalesResoluciones


FECHA_RE = re.compile(r"^\d{8}$")
ACCION_POR_ETIQUETA = {
    etiqueta.lower(): codigo for codigo, etiqueta in InstrumentosLegalesResoluciones.ACCION
}

# Modelos con un campo de texto libre "numero/acta/año" o "numero/año" y un FK
# hermano a InstrumentosLegalesResoluciones a completar.
MODELOS_A_VINCULAR = [
    (Obra, "obra_resolucion", "obra_resolucion_fk"),
    (ConjuntoLicitado, "conjunto_resolucion", "conjunto_resolucion_fk"),
    (Contrato, "contrato_resolucion", "contrato_resolucion_fk"),
]

PATRON_DIRECTORIO = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*$")  # numero/acta/año
PATRON_PRESIDENCIA = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*$")  # numero/año


class Command(BaseCommand):
    """
    Importa resoluciones (PDF) escaneadas desde una carpeta, parseando el nombre
    de cada archivo para determinar sus datos y creando los registros en
    InstrumentosLegalesResoluciones.

    Formato del nombre de archivo (sin extensión), separado por '+':
        <numero>-<acta>-<ano>+<condiciones...>   -> Resolución de Directorio
        <numero>-<ano>+<condiciones...>          -> Resolución de Presidencia

    Las <condiciones> pueden aparecer en cualquier orden e incluir:
        - la acción de la resolución (adjudicatoria, aprobatoria, ratificatoria, ampliatoria)
          -> instrumentolegalresoluciones_accion
        - "horrible" si el escaneo está en mala condición -> instrumentolegalresoluciones_estado_escaneo
        - "referendum" si es una resolución de presidencia firmada ad referendum
          -> instrumentolegalresoluciones_ad_referendum
        - una fecha de aprobación en formato ddmmaaaa -> instrumentolegalresoluciones_fecha_aprobacion

    Cualquier condición que no matchee ninguna de las anteriores se vuelca, tal
    cual, en instrumentolegalresoluciones_descripcion para revisión manual.

    Ejemplos:
        0005-01-2013+adjudicatoria.pdf
        0165-2014+adjudicatoria+referendum+horrible.pdf

    Es re-ejecutable: si ya existe una resolución con el mismo tipo/número/acta/año, se omite.

    Además, luego de importar los PDFs, recorre los modelos que tienen un campo
    de texto libre con la resolución (carga.Obra, carga.ConjuntoLicitado,
    carga.Contrato) y para aquellos registros sin el FK correspondiente
    completado, intenta interpretar ese texto como "numero/acta/año" (resolución
    de Directorio) o "numero/año" (resolución de Presidencia) y vincularlo con
    el InstrumentosLegalesResoluciones que corresponda.

    Corre en modo dry-run por default (no escribe nada); pasar --commit para persistir.

    Uso:
        python manage.py resolucionesobras
        python manage.py resolucionesobras --commit
        python manage.py resolucionesobras --dir /ruta/a/otra/carpeta --commit
    """

    help = "Importa PDFs de resoluciones desde una carpeta parseando sus nombres de archivo (dry-run por default, pasar --commit para persistir)."

    DEFAULT_DIR = os.path.join(
        os.path.dirname(__file__),  # .../secretariador/management/commands
        "../../../../env/.snipets/Resoluciones",
    )

    def add_arguments(self, parser):
        parser.add_argument("--dir", default=self.DEFAULT_DIR, help="Carpeta a escanear en busca de PDFs.")
        parser.add_argument("--commit", action="store_true", help="Persiste los cambios (sin esto, sólo reporta).")

    def handle(self, *args, **options):
        directorio = os.path.abspath(options["dir"])
        commit = options["commit"]

        self.stdout.write(f"Escaneando: {directorio}")
        if not os.path.isdir(directorio):
            self.stderr.write(self.style.ERROR(f"La carpeta no existe: {directorio}"))
            return

        archivos = sorted(f for f in os.listdir(directorio) if f.lower().endswith(".pdf"))
        self.stdout.write(f"Se encontraron {len(archivos)} archivo(s) PDF")

        if not commit:
            self.stdout.write(self.style.WARNING(
                "Modo dry-run: no se va a persistir nada. Pasar --commit para crear los registros."
            ))

        creados = 0
        omitidos = 0
        errores = 0

        for filename in archivos:
            filepath = os.path.join(directorio, filename)
            try:
                datos = self.parse_filename(filename)
            except ValueError as e:
                self.stderr.write(self.style.ERROR(f"{filename}: {e}"))
                errores += 1
                continue

            if datos["fecha_estimada"]:
                self.stdout.write(self.style.WARNING(
                    f"{filename}: no se encontró fecha de aprobación en el nombre, "
                    f"se usará la fecha actual como aproximación."
                ))

            existe = InstrumentosLegalesResoluciones.objects.filter(
                instrumentolegalresoluciones_tipo=datos["tipo"],
                instrumentolegalresoluciones_numero=datos["numero"],
                instrumentolegalresoluciones_acta=datos["acta"],
                instrumentolegalresoluciones_ano=datos["ano"],
            ).exists()
            if existe:
                self.stdout.write(self.style.WARNING(
                    f"{filename}: ya existe una resolución Nº{datos['numero']}/{datos['ano']} "
                    f"(acta {datos['acta'] or '-'}), se omite."
                ))
                omitidos += 1
                continue

            etiqueta = (
                f"{datos['numero']}-{datos['acta']}-{datos['ano']}" if datos["acta"]
                else f"{datos['numero']}-{datos['ano']}"
            )
            tipo_legible = "Directorio" if datos["tipo"] == "D" else "Presidencia"

            resumen_condiciones = (
                f"accion={datos['accion'] or '-'} "
                f"escaneo={datos['estado_escaneo']} "
                f"ad_referendum={datos['ad_referendum']}"
            )

            if not commit:
                self.stdout.write(
                    f"[dry-run] {filename} -> {tipo_legible} Nº{etiqueta} - "
                    f"{resumen_condiciones} - descripcion={datos['descripcion']!r} "
                    f"(fecha: {datos['fecha_aprobacion']})"
                )
                creados += 1
                continue

            try:
                with transaction.atomic():
                    obj = InstrumentosLegalesResoluciones(
                        instrumentolegalresoluciones_tipo=datos["tipo"],
                        instrumentolegalresoluciones_numero=datos["numero"],
                        instrumentolegalresoluciones_acta=datos["acta"],
                        instrumentolegalresoluciones_ano=datos["ano"],
                        instrumentolegalresoluciones_fecha_aprobacion=datos["fecha_aprobacion"],
                        instrumentolegalresoluciones_descripcion=datos["descripcion"],
                        instrumentolegalresoluciones_estado_escaneo=datos["estado_escaneo"],
                        instrumentolegalresoluciones_ad_referendum=datos["ad_referendum"],
                        instrumentolegalresoluciones_accion=datos["accion"],
                        instrumentolegalresoluciones_autocarga=True,
                    )
                    with open(filepath, "rb") as local_file:
                        obj.instrumentolegalresoluciones.save(filename, File(local_file), save=True)
                self.stdout.write(self.style.SUCCESS(f"Creado -> {tipo_legible} Nº{etiqueta}"))
                creados += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error al importar '{filename}': {e}"))
                errores += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nResumen: {creados} {'a crear (dry-run)' if not commit else 'creado(s)'}, "
            f"{omitidos} omitido(s), {errores} error(es)"
        ))

        self.vincular_fks(commit)

    def vincular_fks(self, commit):
        self.stdout.write("\nBuscando vínculos por patrón numero/acta/año o numero/año...")

        for modelo, campo_texto, campo_fk in MODELOS_A_VINCULAR:
            queryset = modelo.objects.filter(
                **{f"{campo_fk}__isnull": True}
            ).exclude(**{campo_texto: None}).exclude(**{campo_texto: ""})

            vinculados = sin_match = ambiguos = 0

            for obj in queryset:
                texto = getattr(obj, campo_texto).strip()
                resolucion, motivo = self.buscar_resolucion(texto)

                if motivo == "ambiguo":
                    self.stdout.write(self.style.WARNING(
                        f"{modelo.__name__}#{obj.pk}: '{texto}' es ambiguo (varias resoluciones coinciden), se omite."
                    ))
                    ambiguos += 1
                    continue

                if resolucion is None:
                    sin_match += 1
                    continue

                accion = "Vinculado" if commit else "[dry-run] A vincular"
                self.stdout.write(f"{accion}: {modelo.__name__}#{obj.pk} '{texto}' -> {resolucion}")
                if commit:
                    setattr(obj, campo_fk, resolucion)
                    obj.save(update_fields=[campo_fk])
                vinculados += 1

            self.stdout.write(self.style.SUCCESS(
                f"{modelo.__name__}: {vinculados} {'vinculado(s) (dry-run)' if not commit else 'vinculado(s)'}, "
                f"{sin_match} sin match, {ambiguos} ambiguo(s)"
            ))

    def buscar_resolucion(self, texto):
        """
        Interpreta 'texto' como numero/acta/año (Resolución de Directorio) o
        numero/año (Resolución de Presidencia) y busca la resolución que
        corresponde. Devuelve (resolucion_o_None, motivo) donde motivo es
        "ambiguo" si hay más de una coincidencia, o None en cualquier otro caso.
        """
        match = PATRON_DIRECTORIO.match(texto)
        if match:
            numero, _acta, ano = match.groups()
            queryset = InstrumentosLegalesResoluciones.objects.filter(
                instrumentolegalresoluciones_tipo="D",
                instrumentolegalresoluciones_numero=numero.zfill(5),
                instrumentolegalresoluciones_ano=ano,
            )
        else:
            match = PATRON_PRESIDENCIA.match(texto)
            if not match:
                return None, None
            numero, ano = match.groups()
            queryset = InstrumentosLegalesResoluciones.objects.filter(
                instrumentolegalresoluciones_tipo="P",
                instrumentolegalresoluciones_numero=numero.zfill(5),
                instrumentolegalresoluciones_ano=ano,
            )

        candidatos = list(queryset[:2])
        if not candidatos:
            return None, None
        if len(candidatos) > 1:
            return None, "ambiguo"
        return candidatos[0], None

    def parse_filename(self, filename):
        """
        Parsea un nombre de archivo con formato:
            <numero>[-<acta>]-<ano>+<condicion1>+<condicion2>+...
        Las condiciones pueden estar en cualquier orden y son: la acción de la
        resolución (adjudicatoria/aprobatoria/ratificatoria/ampliatoria),
        "horrible", "referendum" y/o una fecha ddmmaaaa.
        """
        stem = filename[:-4] if filename.lower().endswith(".pdf") else filename
        partes = stem.split("+")
        numero_parte = partes[0]
        condiciones = partes[1:]

        segmentos = numero_parte.split("-")
        if len(segmentos) == 3:
            numero, acta, ano = segmentos
            tipo = "D"
        elif len(segmentos) == 2:
            numero, ano = segmentos
            acta = ""
            tipo = "P"
        else:
            raise ValueError(f"no se pudo interpretar el número de instrumento: '{numero_parte}'")

        if not (numero.isdigit() and ano.isdigit() and (not acta or acta.isdigit())):
            raise ValueError(f"número de instrumento inválido: '{numero_parte}'")

        estado_escaneo = "N"
        ad_referendum = False
        accion = None
        fecha_aprobacion = None
        descripcion_partes = []

        for condicion in condiciones:
            condicion = condicion.strip()
            if not condicion:
                continue
            clave = condicion.lower()
            if clave == "horrible":
                estado_escaneo = "H"
            elif clave == "referendum":
                ad_referendum = True
            elif FECHA_RE.match(condicion):
                try:
                    fecha_aprobacion = datetime.strptime(condicion, "%d%m%Y").date()
                except ValueError:
                    raise ValueError(f"fecha de aprobación inválida: '{condicion}'")
            elif clave in ACCION_POR_ETIQUETA:
                accion = ACCION_POR_ETIQUETA[clave]
            else:
                # Condición no reconocida: se guarda en descripción para revisión manual.
                descripcion_partes.append(condicion.capitalize())

        return {
            "tipo": tipo,
            "numero": numero.zfill(5),
            "acta": acta,
            "ano": ano,
            "fecha_aprobacion": fecha_aprobacion or timezone.now().date(),
            "fecha_estimada": fecha_aprobacion is None,
            "estado_escaneo": estado_escaneo,
            "ad_referendum": ad_referendum,
            "accion": accion,
            "descripcion": " - ".join(descripcion_partes)[:600],
        }
