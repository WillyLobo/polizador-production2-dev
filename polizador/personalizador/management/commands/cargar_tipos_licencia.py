import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from personalizador.models import TipoLicenciaPermiso

logger = logging.getLogger(__name__)


# Metadata transcripta de la Ley 645-A (ex Ley 3521), Capítulos I a IV.
# tope=None => tope variable (antigüedad, junta médica, criterio de la autoridad, etc.),
# no un número fijo.
TIPOS_DATA = [
    # --- A) a) Licencias Ordinarias ---
    {"categoria": "LOR", "nombre": "Anual", "articulo": "Art. 7", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 6, "certificado": False, "compensacion": False,
     "observaciones": "Tope según antigüedad al 31/12 (Art. 8): 6m-5a=23 días, +5-10a=28, +10-18a=42, +18a=49 días corridos."},
    {"categoria": "LOR", "nombre": "Anual Proporcional", "articulo": "Art. 10", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 6, "certificado": False, "compensacion": False,
     "observaciones": "Uso adelantado, total o parcial, de la Licencia Anual Ordinaria del propio período calendario de fecha_desde (que, por ser año vencido, recién abre el 15/12 de ese año): consume ese cupo antes de su apertura formal, en vez de esperar a diciembre. Debe efectivizarse dentro del plazo del último párrafo del Art. 7°. (La planilla de RRHH suele rotular esto como \"adelanto <año+1>\" por ser el año en que mayormente se goza, pero el período de devengamiento sigue siendo el de fecha_desde.)"},
    {"categoria": "LOR", "nombre": "Motivos de Salud (Enfermedad o lesión común)", "articulo": "Art. 14 A", "unidad": "DC", "tope": 45, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "LOR", "nombre": "Motivos de Salud (Enfermedad prolongada o lesión grave)", "articulo": "Art. 14 B", "unidad": "DC", "tope": 730, "tope_periodo": "TOT", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "2 años con goce de haberes + opción de 1 año más sin goce."},
    {"categoria": "LOR", "nombre": "Motivos de Salud (Accidente de trabajo o enfermedad ocupacional)", "articulo": "Art. 14 C", "unidad": "DC", "tope": 730, "tope_periodo": "TOT", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "2 años con remuneración íntegra + 1 año más sin goce."},
    {"categoria": "LOR", "nombre": "Motivos de Salud (Atención de familiar enfermo)", "articulo": "Art. 14 D", "unidad": "DC", "tope": 30, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "LOR", "nombre": "Motivos de Salud (Enfermedad o lesión grave de familiar)", "articulo": "Art. 14 E", "unidad": "DC", "tope": 90, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "Subsume el término del Art. 23."},
    {"categoria": "LOR", "nombre": "Anual de Invierno", "articulo": "Art. 9", "unidad": "DC", "tope": 10, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": False, "compensacion": False,
     "observaciones": "Período de goce fijado anualmente por el Poder Ejecutivo."},
    {"categoria": "LOR", "nombre": "Maternidad o Gravidez", "articulo": "Art. 13/14", "unidad": "DC", "tope": 180, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "60 días antes + 120 después del parto (o acumulados). Extensiones por parto múltiple/prematuro (+30), hijo discapacitado (+90)."},

    # --- A) b) Licencias Extraordinarias ---
    {"categoria": "LEX", "nombre": "Adopción", "articulo": "Art. 29", "unidad": "DC", "tope": 180, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "100 días (niño hasta 8 años), 180 si es menor de 2 años, 90 si es mayor de 8 años."},
    {"categoria": "LEX", "nombre": "Matrimonio", "articulo": "Art. 30/31", "unidad": "DH", "tope": 12, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 3, "certificado": False, "compensacion": False},
    {"categoria": "LEX", "nombre": "Estudios de Interés General", "articulo": "Art. 32/33", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 6, "certificado": True, "compensacion": False,
     "observaciones": "Término fijado según la actividad, a criterio de la autoridad competente."},
    {"categoria": "LEX", "nombre": "Estudios de Interés Particular", "articulo": "Art. 34/35", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "NO", "antiguedad_meses": 12, "certificado": True, "compensacion": False},
    {"categoria": "LEX", "nombre": "Permiso por Exámenes", "articulo": "Art. 36/37", "unidad": "DH", "tope": 28, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "Fracciones máximas de 4 días hábiles por examen, hasta 8 si se rinde más de una materia."},
    {"categoria": "LEX", "nombre": "Incorporación a las Fuerzas Armadas", "articulo": "Art. 38", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "Término determinado por las Fuerzas Armadas."},
    {"categoria": "LEX", "nombre": "Examen Psicofisiológico", "articulo": "Art. 39", "unidad": "DC", "tope": 10, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": False, "compensacion": False},
    {"categoria": "LEX", "nombre": "Actividades Artísticas y Culturales", "articulo": "Art. 40/41", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "LEX", "nombre": "Actividades Deportivas", "articulo": "Art. 42/43", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 6, "certificado": True, "compensacion": False},
    {"categoria": "LEX", "nombre": "Razones Particulares", "articulo": "Art. 44", "unidad": "DC", "tope": 12, "tope_periodo": "TOT", "remunerada": "NO", "antiguedad_meses": 60, "certificado": False, "compensacion": False,
     "observaciones": "Términos: +5-10a=1 mes, +10-20a=6 meses, +20a=12 meses. Una sola vez por período; no válida a fines jubilatorios/antigüedad."},
    {"categoria": "LEX", "nombre": "Ejercicio de Funciones de Nivel Superior", "articulo": "Art. 45/46", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "NO", "antiguedad_meses": 12, "certificado": True, "compensacion": False,
     "observaciones": "Sin goce de haberes por el término de la función superior."},
    {"categoria": "LEX", "nombre": "Actividades Políticas", "articulo": "Art. 47", "unidad": "DC", "tope": 30, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "30 días corridos (candidatos) o 5 días hábiles antes de asumir (electos), con opción a licencia sin goce hasta finalizar el mandato."},
    {"categoria": "LEX", "nombre": "Representación Gremial", "articulo": "Art. 48", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 24, "certificado": False, "compensacion": False,
     "observaciones": "Mientras dure el mandato + 5 días hábiles posteriores."},
    {"categoria": "LEX", "nombre": "Representación Mutual", "articulo": "Art. 49", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "NO", "antiguedad_meses": 24, "certificado": False, "compensacion": False,
     "observaciones": "Mientras dure el mandato + 5 días hábiles posteriores. Abonada por la mutual."},
    {"categoria": "LEX", "nombre": "Donación de Órganos", "articulo": "Art. 51", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "LEX", "nombre": "Examen de Papanicolau y/o Mamografía", "articulo": "Art. 52", "unidad": "DC", "tope": 1, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "LEX", "nombre": "Exámenes de Control PSA", "articulo": "Art. 53", "unidad": "DC", "tope": 1, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "Agentes mayores de 45 años."},
    {"categoria": "LEX", "nombre": "Nacimiento", "articulo": "Art. 54", "unidad": "DH", "tope": 20, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "15 días hábiles (parto a término) o 20 (parto prematuro), agente varón."},
    {"categoria": "LEX", "nombre": "Violencia de Género y/o Familiar", "articulo": "Art. 55/57", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "LEX", "nombre": "Fertilización Asistida", "articulo": "Art. 58/59", "unidad": "DC", "tope": 30, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},

    # --- B) Permisos ---
    {"categoria": "PER", "nombre": "Adopción (nieto)", "articulo": "Art. 54 b)", "unidad": "DC", "tope": 2, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "2 días, +1 por cada nieto en nacimiento/adopción múltiple, +2 si el hogar está a más de 200km."},
    {"categoria": "PER", "nombre": "Lactancia", "articulo": "Art. 50 inc. 6", "unidad": "HS", "tope": 2, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "120 minutos diarios por 3 meses desde el fin de la licencia por maternidad, prorrogable."},
    {"categoria": "PER", "nombre": "Natalicio del Agente", "articulo": "Art. 50 inc. 8", "unidad": "DC", "tope": 1, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": False, "compensacion": False},
    {"categoria": "PER", "nombre": "Matrimonio de Hijo del Agente", "articulo": "Art. 50 inc. 7", "unidad": "DH", "tope": 2, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": False, "compensacion": False},
    {"categoria": "PER", "nombre": "Fallecimiento de Familiar", "articulo": "Art. 50 inc. 1", "unidad": "DH", "tope": 6, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False,
     "observaciones": "Cónyuge/padres/hijos/hermanos: 6 días. Suegros/abuelos/nietos/a cargo: 2 días. Parientes 3er grado: 1 día."},
    {"categoria": "PER", "nombre": "Siniestro o Hecho de Extrema Gravedad", "articulo": "Art. 50 inc. 2", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "PER", "nombre": "Donación de Sangre", "articulo": "Art. 50 inc. 3", "unidad": "DH", "tope": 1, "tope_periodo": "VEZ", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "PER", "nombre": "Razones Particulares", "articulo": "Art. 50 inc. 4", "unidad": "HS", "tope": 40, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": False, "compensacion": True,
     "observaciones": "Requiere autorización previa y compensación de horario."},
    {"categoria": "PER", "nombre": "Estudios Regulares", "articulo": "Art. 50 inc. 5", "unidad": "HS", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": True,
     "observaciones": "Cambio de turno/horario especial; si no es posible, salidas compensadas con horas extra sin retribución."},
    {"categoria": "PER", "nombre": "Representación Gremial", "articulo": "Art. 50 inc. 9", "unidad": "HS", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 0, "certificado": False, "compensacion": False,
     "observaciones": "2 horas diarias sin reposición de horario, para delegados electos."},
    {"categoria": "PER", "nombre": "Citación Legal con Acreditación de Comparecencia", "articulo": "Art. 50 inc. 10", "unidad": "DC", "tope": None, "tope_periodo": "VAR", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
    {"categoria": "PER", "nombre": "Atención a Familiar Incapacitado o Discapacitado", "articulo": "Art. 50 inc. 11", "unidad": "DH", "tope": 15, "tope_periodo": "ANI", "remunerada": "SI", "antiguedad_meses": 0, "certificado": True, "compensacion": False},
]


class Command(BaseCommand):
    help = (
        "Carga (o actualiza) el catálogo de Tipos de Licencia/Permiso de la Ley 645-A. "
        "El match para update_or_create es (categoria, nombre): si alguien renombró un "
        "TipoLicenciaPermiso a mano (admin, shell) sin actualizar TIPOS_DATA, ese nombre "
        "ya no matchea y el comando CREA un duplicado en vez de actualizar el existente. "
        "Antes de escribir, siempre chequea posibles renombres comparando por 'articulo' "
        "(más estable que 'nombre') y avisa por consola; con --dry-run no escribe nada."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Solo corre la verificación de renombres/nuevos y muestra el resumen, sin guardar nada.",
        )

    def _verificar_renombres(self):
        """Compara TIPOS_DATA contra la base por 'articulo' (categoria+articulo), que
        es mucho más estable que 'nombre' (un artículo de la Ley 645-A no cambia,
        pero el nombre de un tipo sí puede editarse a mano). Devuelve una lista de
        avisos de texto; no modifica nada."""
        avisos = []
        existentes_por_nombre = {
            (t.tipolicenciapermiso_categoria, t.tipolicenciapermiso_nombre)
            for t in TipoLicenciaPermiso.objects.all()
        }
        existentes_por_articulo = {}
        for t in TipoLicenciaPermiso.objects.exclude(tipolicenciapermiso_articulo__isnull=True).exclude(tipolicenciapermiso_articulo=""):
            existentes_por_articulo.setdefault((t.tipolicenciapermiso_categoria, t.tipolicenciapermiso_articulo), []).append(t)

        existentes_por_nombre_obj = {
            (t.tipolicenciapermiso_categoria, t.tipolicenciapermiso_nombre): t
            for t in TipoLicenciaPermiso.objects.all()
        }
        for item in TIPOS_DATA:
            clave_nombre = (item["categoria"], item["nombre"])
            if clave_nombre in existentes_por_nombre:
                actual = existentes_por_nombre_obj[clave_nombre]
                if actual.tipolicenciapermiso_articulo != item.get("articulo"):
                    avisos.append(
                        f"ARTICULO DISTINTO: {item['categoria']} {item['nombre']!r} (pk={actual.pk}) tiene "
                        f"articulo={actual.tipolicenciapermiso_articulo!r} en la base, pero TIPOS_DATA "
                        f"espera {item.get('articulo')!r}. Si se corre el comando así, se va a PISAR el "
                        "valor de la base con el de TIPOS_DATA -- revisar cuál es el correcto antes de continuar."
                    )
                continue  # matchea por nombre, update_or_create lo va a actualizar bien

            articulo = item.get("articulo")
            candidatos = existentes_por_articulo.get((item["categoria"], articulo)) if articulo else None
            if candidatos:
                nombres_db = ", ".join(f"pk={c.pk} {c.tipolicenciapermiso_nombre!r}" for c in candidatos)
                avisos.append(
                    f"POSIBLE RENOMBRE: {item['categoria']} {articulo!r} en TIPOS_DATA se llama "
                    f"{item['nombre']!r}, pero en la base ya existe con otro nombre ({nombres_db}). "
                    "Si se corre el comando así, se va a CREAR un TipoLicenciaPermiso duplicado en "
                    "vez de actualizar el existente -- reconciliar a mano antes de continuar "
                    "(renombrar el de la base, o ajustar TIPOS_DATA si el nombre nuevo es el correcto)."
                )
            else:
                avisos.append(
                    f"NUEVO: {item['categoria']} {item['nombre']!r} (articulo={articulo!r}) no existe "
                    "en la base todavía -- se va a crear."
                )

        nombres_data = {(item["categoria"], item["nombre"]) for item in TIPOS_DATA}
        for t in TipoLicenciaPermiso.objects.all():
            if (t.tipolicenciapermiso_categoria, t.tipolicenciapermiso_nombre) not in nombres_data:
                avisos.append(
                    f"EN LA BASE PERO NO EN TIPOS_DATA: pk={t.pk} {t.tipolicenciapermiso_categoria} "
                    f"{t.tipolicenciapermiso_nombre!r} (articulo={t.tipolicenciapermiso_articulo!r}) -- "
                    "no se toca (el comando nunca borra), pero revisar si es un duplicado viejo o un "
                    "tipo agregado a mano que falta transcribir a TIPOS_DATA."
                )
        return avisos

    def handle(self, *args, **options):
        avisos = self._verificar_renombres()
        for aviso in avisos:
            self.stdout.write(self.style.WARNING(aviso))

        if options["dry_run"]:
            if not avisos:
                self.stdout.write(self.style.SUCCESS("Sin discrepancias: TIPOS_DATA matchea la base 1 a 1."))
            self.stdout.write(self.style.NOTICE("Modo dry-run: no se guardo ningun cambio en la base de datos."))
            return

        with transaction.atomic():
            creados = 0
            actualizados = 0
            for item in TIPOS_DATA:
                defaults = {
                    "tipolicenciapermiso_articulo": item.get("articulo"),
                    "tipolicenciapermiso_unidad": item["unidad"],
                    "tipolicenciapermiso_tope_cantidad": item.get("tope"),
                    "tipolicenciapermiso_tope_periodo": item["tope_periodo"],
                    "tipolicenciapermiso_remunerada": item["remunerada"],
                    "tipolicenciapermiso_antiguedad_meses": item.get("antiguedad_meses", 0),
                    "tipolicenciapermiso_requiere_certificado": item.get("certificado", False),
                    "tipolicenciapermiso_compensacion_horaria": item.get("compensacion", False),
                    "tipolicenciapermiso_observaciones": item.get("observaciones"),
                }
                obj, created = TipoLicenciaPermiso.objects.update_or_create(
                    tipolicenciapermiso_categoria=item["categoria"],
                    tipolicenciapermiso_nombre=item["nombre"],
                    defaults=defaults,
                )
                if created:
                    creados += 1
                else:
                    actualizados += 1

        logger.info("Tipos de licencia/permiso: %s creados, %s actualizados.", creados, actualizados)
        self.stdout.write(self.style.SUCCESS(f"Tipos de licencia/permiso: {creados} creados, {actualizados} actualizados."))
