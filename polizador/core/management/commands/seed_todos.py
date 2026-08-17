"""
Carga las tareas de TODO.md (raíz del repo) como registros de core.models.Todo,
para poblar la vista /administracion/tareas/.

Los datos están transcriptos a mano en TODOS de este archivo (no se lee TODO.md
en tiempo de ejecución): TODO.md es una nota de desarrollo libre que puede
moverse o desaparecer, y este comando solo necesita correr una vez para poblar
la base. La sección "# DONE:" de TODO.md se omitió porque duplica, sin agregar
información nueva, ítems ya listados (y ya resueltos) más arriba en el archivo.

Mapeo de la leyenda de TODO.md al Todo.Status del modelo:
    [ ] Pending                          -> pendiente
    [+] Completed                        -> resuelto
    [?] Implementation needs review      -> parcial
    [!] Forcibly not needed/implemented  -> resuelto (con nota "no se implementará")
    [1] (Fix Bugs, sin leyenda propia)   -> pendiente (con nota de origen)

Es idempotente: usa el título como clave y no pisa el estado de tareas que ya
existan (por si alguien las actualizó a mano desde la web).

    python manage.py seed_todos
    python manage.py seed_todos --dry-run
"""
from django.core.management.base import BaseCommand

from core.models import Todo

PENDIENTE = Todo.Status.PENDIENTE
PARCIAL = Todo.Status.PARCIAL
RESUELTO = Todo.Status.RESUELTO

# (categoría, título, descripción, status)
TODOS = [
    # --- General / Carga ---
    ("General", "Agregar los campos nombre y apellido al formulario de registro de cuenta", "", RESUELTO),
    ("General", "Eliminar easy Audit", "", RESUELTO),
    ("General", "Crear script para recopilar datos del valor UVI con fuente del BCRA", "", RESUELTO),
    (
        "General",
        "Revisar los campos de modelos que requieren operaciones aritméticas y aplicar campos generados",
        "A nivel base de datos.",
        RESUELTO,
    ),
    (
        "General",
        "Crear grupos de permisos para los usuarios",
        "Sub-tareas: Dirección General (hecho); Gerencia Operativa (hecho); "
        "Grupos para edición y grupos para vistas (tipo invitado, solo para ver reportes) — a revisar.",
        PARCIAL,
    ),
    ("General", "Repasar los permisos en los Views", "", RESUELTO),
    ("General", "Ordenar el cuadro búsqueda de datatables", "", RESUELTO),
    ("General", "Ajustar los templates de reportes de la app carga para ajustarse al resto del sitio", "", PARCIAL),
    ("General", "Corregir los Select en las páginas de creación de reportes", "", PARCIAL),
    ("General", "Redireccionar usuarios con permisos fuera de la vista sin permisos", "", RESUELTO),
    ("General", "Modificar modelo Agente para vincularlo a los agentes de la app secretariador", "", RESUELTO),
    (
        "General",
        "VerReporteCertificadoPorMes debería dar opción de ver los certificados por fecha de carga o fecha de certificado",
        "",
        RESUELTO,
    ),
    ("General", "Reparar los templates para ajustar viewport size", "", RESUELTO),
    ("General", "Rehacer la integración para contratos y resoluciones digitales de obras", "", RESUELTO),
    (
        "General",
        "Crear API view que devuelva los meses/años disponibles en los certificados para su utilización en select2",
        "",
        RESUELTO,
    ),
    ("General", "Hacer un favicon más decente", "", PARCIAL),
    ("General", "Añadir campo Representante Técnico a las obras", "", RESUELTO),
    ("General", "Implementar campo georeferencia (con PostGIS) para las obras", "", RESUELTO),
    (
        "General",
        "Actualizar a la última versión de dataTables",
        "Sub-tareas: convertir \"dom:\" a \"layout:\" (hecho); agregar botón para exportar a pdf/excel (hecho).",
        RESUELTO,
    ),
    ("General", "Eliminar código muerto JS", "", PENDIENTE),
    ("General", "Corregir el filtrado previo de resoluciones, o agregar el filtro por tipo en datatable", "", RESUELTO),
    ("General", "Normalizar los números de resoluciones para que usen el mismo separador (\"-\")", "", RESUELTO),
    (
        "General",
        "Crear helper que convierta los números de resoluciones nuevos al formato de número de resoluciones digitales (S.G.T.)",
        "",
        RESUELTO,
    ),
    ("General", "Crear helper para agregar objetos FK directamente desde los formularios", "", RESUELTO),
    ("General", "Agregar opción de remover firmas de gerente/representante técnico en la foja de medición", "", RESUELTO),
    (
        "General",
        "Agregar helptext dinámico a los campos CUIL/CUIT de los formularios que sugieran el número de CUIL/CUIT",
        "",
        PENDIENTE,
    ),
    (
        "General",
        "Agregar a la interfaz web la posibilidad de ver estado de escaneo de los instrumentos legales",
        "",
        PENDIENTE,
    ),
    ("General", "Analizar viabilidad de hacer OCR a los instrumentos legales", "", PENDIENTE),

    # --- Certificados ---
    ("Certificados", "Una foja debería engendrar 1 certificado por cada financiamiento", "", RESUELTO),
    ("Certificados", "El certificado solo debería utilizar el plan de trabajos vigente", "", RESUELTO),
    (
        "Certificados",
        "Se debe poder crear certificado de anticipo que no lleva foja",
        "El valor se debe descontar proporcionalmente de los certificados posteriores hasta cumplir la totalidad del anticipo.",
        RESUELTO,
    ),
    (
        "Certificados",
        "Se deben poder crear certificados que se aprueban con resolución o contrato pero que no llevan foja de medición",
        "Por ser hechos consumados.",
        RESUELTO,
    ),

    # --- Fojas y Planes de Trabajo ---
    (
        "Fojas y Planes de Trabajo",
        "Agregar listado de fojas y planes de trabajo con DataTables",
        "Marcado como no implementado a propósito en TODO.md ([!]).",
        RESUELTO,
    ),
    (
        "Fojas y Planes de Trabajo",
        "Crear Home para la inspección donde muestren las obras que no han sido medidas aún",
        "",
        PARCIAL,
    ),
    ("Fojas y Planes de Trabajo", "Crear funciones que generen acumulado total en las fojas de medición", "", RESUELTO),
    ("Fojas y Planes de Trabajo", "Crear vista que devuelva las obras donde el usuario es inspector", "", RESUELTO),
    (
        "Fojas y Planes de Trabajo",
        "Verificar que una obra pueda tener varios planes de trabajo, pero solo uno activo",
        "",
        RESUELTO,
    ),
    ("Fojas y Planes de Trabajo", "Imágenes múltiples para fojas de medición", "", RESUELTO),
    ("Fojas y Planes de Trabajo", "Campo archivo para planes de trabajo digitalizados", "", RESUELTO),

    # --- Models (secretariador) ---
    ("Models (secretariador)", "Create model Incorporacion", "", RESUELTO),
    ("Models (secretariador)", "Build create/update templates", "", RESUELTO),
    ("Models (secretariador)", "Create concatenated fields for display", "", RESUELTO),
    ("Models (secretariador)", "Comisionado Model", "", RESUELTO),
    ("Models (secretariador)", "ComisionadoSolicitud Model", "", RESUELTO),
    ("Models (secretariador)", "Build Create/Update/Delete/List views", "", RESUELTO),
    ("Models (secretariador)", "Add navbar links", "", RESUELTO),
    (
        "Models (secretariador)",
        "Create detail templates",
        "Sub-tareas: ListaIncorporacionesView, ListaComisionadosView, ListaVehiculosView.",
        RESUELTO,
    ),
    ("Models (secretariador)", "Create report views", "Sub-tarea: filter by agent.", RESUELTO),
    (
        "Models (secretariador)",
        "Add field localidad_distancia to Localidad model (carga app)",
        "Marcado como no implementado a propósito en TODO.md ([!]).",
        RESUELTO,
    ),
    (
        "Models (secretariador)",
        "Add route distance to Localidades (from Capital city, Resistencia)",
        "Marcado como no implementado a propósito en TODO.md ([!]).",
        RESUELTO,
    ),
    (
        "Models (secretariador)",
        "Add save method to set Comisionados into Solicitud database field",
        "Marcado como no implementado a propósito en TODO.md ([!]).",
        RESUELTO,
    ),
    (
        "Models (secretariador)",
        "Add ajax to validate if instrumentolegalresoluciones is not duplicated before filling it in the form",
        "Marcado como no implementado a propósito en TODO.md ([!]).",
        RESUELTO,
    ),
    (
        "Models (secretariador)",
        "Add field instrumentolegalresoluciones_actuacion to InstrumentosLegalesResoluciones model",
        "Generado a partir de instrumentolegalresoluciones_descripcion split. "
        "Marcado como no implementado a propósito en TODO.md ([!]).",
        RESUELTO,
    ),

    # --- Docx Templates ---
    (
        "Docx Templates",
        "Agregar una forma de actualizar template.docx",
        "Ej: subir y sobreescribir el archivo original.",
        PENDIENTE,
    ),

    # --- Web Templates ---
    (
        "Web Templates",
        "Agregar un frame lateral derecho en los templates de formularios para mostrar help-text",
        "Marcado como no implementado a propósito en TODO.md ([!]).",
        RESUELTO,
    ),
    ("Web Templates", "Agregar capacidad de logging más avanzada", "", RESUELTO),

    # --- Fix Bugs ---
    (
        "Fix Bugs",
        "Agregar campo incorporacion_solicitud_jurisdiccion que actualmente está hardcodeado",
        "Listado con prioridad [1] en TODO.md (sin marca de estado explícita).",
        PENDIENTE,
    ),
    (
        "Fix Bugs",
        "Corregir unique constraint en Solicitud e Incorporacion",
        "Debería validar actuacion_jurisdiccion, actuacion_numero y actuacion_ano en el constraint. "
        "Listado con prioridad [1] en TODO.md (sin marca de estado explícita).",
        PENDIENTE,
    ),

    # --- Personalizador APP > Models ---
    ("Personalizador", "Create database models based on RRHH requests", "", RESUELTO),
    ("Personalizador", "Manejo de los cortes de licencia Anual", "", RESUELTO),
    ("Personalizador", "Corregir vista de datos en ChangeView", "", RESUELTO),
    ("Personalizador", "Ver que la cantidad de días no muestre decimales (debe ser un entero)", "", RESUELTO),
    ("Personalizador", "Ver el cableado del instrumento legal a la solicitud según el tipo de solicitud", "", RESUELTO),
    (
        "Personalizador",
        "Modelar el cálculo de antigüedad del agente",
        "Según fecha de pase a planta, resolución que reconozca años de servicio, aportes privados, etc.",
        PENDIENTE,
    ),
]


class Command(BaseCommand):
    help = "Carga como Todo las tareas transcriptas de TODO.md (ver docstring del módulo)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="No guarda nada, solo informa cuántas tareas se crearían y cuántas ya existen.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        creadas = 0
        existentes = 0
        for categoria, title, description, status in TODOS:
            full_description = f"[{categoria}] {description}".strip() if description else f"[{categoria}]"

            if Todo.objects.filter(title=title).exists():
                existentes += 1
                continue

            creadas += 1
            if not dry_run:
                Todo.objects.create(title=title, description=full_description, status=status)

        accion = "Se crearían" if dry_run else "Creadas"
        self.stdout.write(self.style.SUCCESS(
            f"{accion} {creadas} tarea(s) nueva(s) ({existentes} ya existían por título y se dejaron como estaban)."
        ))
