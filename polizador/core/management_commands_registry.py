"""Whitelist de management commands ejecutables desde /administracion/comandos/.

Solo lo que está explícitamente listado acá puede correrse desde la web: agregar un
comando implica sumarlo a mano con su form, no alcanza con que exista en el filesystem.
No metas acá comandos built-in de Django/terceros (migrate, shell, dbshell, flush,
loaddata, createsuperuser, etc.) ni nada que mute datos sin haber sido revisado.
"""

from core.forms import CheckResolucionesForm

COMMAND_REGISTRY = {
    "resolucion_audit": {
        "label": "Verificar numeración de resoluciones",
        "help_text": (
            "Recorre las resoluciones cargadas desde 2022 y reporta los números "
            "faltantes por año (indican un error de carga). No modifica datos."
        ),
        "form": CheckResolucionesForm,
    },
}
