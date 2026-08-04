"""Whitelist de management commands ejecutables desde /administracion/comandos/.

Solo lo que está explícitamente listado acá puede correrse desde la web: agregar un
comando implica sumarlo a mano con su form, no alcanza con que exista en el filesystem.
No metas acá comandos built-in de Django/terceros (migrate, shell, dbshell, flush,
loaddata, createsuperuser, etc.) ni nada que mute datos sin haber sido revisado.

`mutates_data` solo controla si la web muestra una advertencia antes de correrlo — no
cambia el comportamiento del comando en si.
"""

from core.forms import (
    BcraUviForm,
    CheckResolucionesForm,
    CopiarBucketDevForm,
    EmpaquetarResolucionesMensualForm,
    FixObraResolucionNumbersForm,
    NumerosCertificadosAuditForm,
    ResaveComisionadoForm,
    SyncResolucionesSgtForm,
)

COMMAND_REGISTRY = {
    "resolucion_audit": {
        "label": "Verificar numeración de resoluciones",
        "help_text": (
            "Recorre las resoluciones cargadas desde 2022 y reporta los números "
            "faltantes por año (indican un error de carga). No modifica datos."
        ),
        "form": CheckResolucionesForm,
        "mutates_data": False,
    },
    "bcra_uvi": {
        "label": "Sincronizar UVI (BCRA)",
        "help_text": (
            "Descarga valores diarios de UVI desde la API pública del BCRA y los guarda "
            "en la base. Es aditivo e idempotente: solo inserta fechas que todavía no "
            "existen, nunca modifica ni borra un valor ya guardado."
        ),
        "form": BcraUviForm,
        "mutates_data": True,
    },
    "fix_obra_resolucion_numbers": {
        "label": "Normalizar numeración de resoluciones (Obra/Contrato)",
        "help_text": (
            "Reemplaza '/' por '-' en la numeración de resolución cargada a mano en "
            "Obra, ConjuntoLicitado y Contrato, para adoptar la convención "
            "RES-AAAA-NUMERO-JURISDICCION-ACTA. Elegí 'Solo verificar' o 'Simular' "
            "antes de aplicar los cambios."
        ),
        "form": FixObraResolucionNumbersForm,
        "mutates_data": True,
    },
    "numeros_certificados_audit": {
        "label": "Corregir numeración de certificados",
        "help_text": (
            "Corrige numeración de certificados de anticipo/Res.62 y obras cargadas con "
            "convenio FO.PRO.VI. mal cargado. Elegí 'Solo verificar' o 'Simular' antes "
            "de aplicar los cambios."
        ),
        "form": NumerosCertificadosAuditForm,
        "mutates_data": True,
    },
    "copiar_bucket_dev": {
        "label": "Copiar bucket GCS producción -> dev",
        "help_text": (
            "Copia objetos server-side (no pasan por este servidor) de "
            "polizador-production-pdf a polizador-dev-pdf. Es una copia puntual, no un "
            "sync continuo: se vuelve a correr a mano cuando haga falta realinear. "
            "Requiere credenciales de GCS cargadas en el servidor."
        ),
        "form": CopiarBucketDevForm,
        "mutates_data": True,
    },
    "empaquetar_resoluciones_mensual": {
        "label": "Empaquetar resoluciones del mes (ZIP/PDF)",
        "help_text": (
            "Arma los paquetes mensuales de resoluciones (ZIP y/o PDF fusionado) y los "
            "deja en GCS para descargar. Sin Año/Mes, empaqueta el mes anterior al "
            "actual (uso normal, pensado para correr el día 1 de cada mes). Borra "
            "paquetes viejos del mismo mes/formato antes de generar los nuevos."
        ),
        "form": EmpaquetarResolucionesMensualForm,
        "mutates_data": True,
    },
    "resave_comisionado": {
        "label": "Recalcular viáticos de comisionados",
        "help_text": (
            "Vuelve a guardar todas las ComisionadoSolicitud para forzar el recálculo "
            "de los campos derivados (días, viático diario, viático computado, viático "
            "total). Sin parámetros: toca todos los registros de la tabla."
        ),
        "form": ResaveComisionadoForm,
        "mutates_data": True,
    },
    "sync_resoluciones_sgt": {
        "label": "Importar resoluciones desde el SGT",
        "help_text": (
            "Maneja un navegador real (Playwright/Firefox) para iniciar sesión en el SGT "
            "(app.chaco.gob.ar) con las credenciales institucionales del .env y descargar "
            "las Resoluciones aprobadas que todavía no están cargadas en Polizador. Puede "
            "tardar varios minutos. Empezá con 'Simular' para ver qué importaría."
        ),
        "form": SyncResolucionesSgtForm,
        "mutates_data": True,
    },
}
