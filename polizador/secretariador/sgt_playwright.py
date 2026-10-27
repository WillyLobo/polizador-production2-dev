"""
Lanzamiento de Firefox para los comandos sync_*_sgt, con auto-reparación.

Cada versión del paquete `playwright` de pip trae fijada una revisión puntual de
Firefox (~/.cache/ms-playwright/firefox-<rev>). Cuando se actualiza el paquete
(dependabot, pip-update.py) el binario nuevo todavía no está descargado y
launch() falla con "Executable doesn't exist", cortando la corrida programada.
Acá se detecta ese caso puntual, se baja el navegador con el mismo intérprete
del venv (`python -m playwright`, nunca el `playwright` del PATH: sin el venv
activo Ubuntu sugiere `apt install node-playwright`, que no tiene nada que ver)
y se reintenta una sola vez.

Lo que no se intenta reparar: dependencias del sistema faltantes (eso es
`sudo ... playwright install-deps firefox`, requiere root).
"""
import subprocess
import sys

from django.core.management.base import CommandError

COMANDO_INSTALAR = f"{sys.executable} -m playwright install firefox"


def _falta_el_navegador(error):
    return "Executable doesn't exist" in str(error)


def instalar_firefox(stdout=None):
    if stdout:
        stdout.write(f"Firefox de Playwright no está descargado; corriendo `{COMANDO_INSTALAR}`...")
    resultado = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "firefox"],
        capture_output=True, text=True, timeout=600,
    )
    if resultado.returncode != 0:
        raise CommandError(
            f"Falló `{COMANDO_INSTALAR}`:\n{resultado.stderr or resultado.stdout}"
        )


def lanzar_firefox(p, headless=True, stdout=None):
    try:
        return p.firefox.launch(headless=headless)
    except Exception as e:
        if not _falta_el_navegador(e):
            raise CommandError(f"No pude lanzar Firefox: {e}")
    instalar_firefox(stdout)
    try:
        return p.firefox.launch(headless=headless)
    except Exception as e:
        raise CommandError(
            f"No pude lanzar Firefox aun después de instalarlo: {e}\n"
            f"Probá a mano `{COMANDO_INSTALAR}` (y si faltan librerías del sistema, "
            f"`sudo {sys.executable} -m playwright install-deps firefox`)."
        )
