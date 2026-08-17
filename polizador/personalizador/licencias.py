"""Cálculo de saldos de licencias y permisos (Ley 645-A).

Funciones puras que no dependen de vistas: reciben un `Agente` y devuelven la
cantidad de días/horas correspondientes, usados y disponibles para un tipo de
licencia/permiso en un año calendario dado.
"""
from datetime import date

from personalizador.models import CorteLicencia, LicenciaPermiso, TipoLicenciaPermiso

LICENCIA_ANUAL_ORDINARIA_NOMBRE = "Anual"
LICENCIA_ANUAL_INVIERNO_NOMBRE = "Anual de Invierno"
LICENCIA_ANUAL_ADELANTADA_NOMBRE = "Anual Proporcional"

# Prefijo de licenciapermiso_motivo que marca un registro generado por
# personalizador.management.commands.importar_control_licencias (en vez de
# cargado a mano): permite reconocerlos para el datatable y para reejecutar
# el import sin duplicar. Vive aca (no en el comando) para poder importarlo
# tanto desde el comando como desde las vistas sin depender de un modulo de
# management command.
LICENCIA_IMPORTADA_MOTIVO_PREFIJO = "[Importado control_licencias.xlsx]"


def _tipo_anual_adelantada():
    return TipoLicenciaPermiso.objects.filter(
        tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre=LICENCIA_ANUAL_ADELANTADA_NOMBRE,
    ).first()


def _tipo_anual_ordinaria():
    return TipoLicenciaPermiso.objects.filter(
        tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre=LICENCIA_ANUAL_ORDINARIA_NOMBRE,
    ).first()


def antiguedad_meses(agente, hasta):
    """Antigüedad del agente (en meses completos) a la fecha `hasta`, tomando
    `agente.fecha_ingreso` como inicio. Devuelve 0 si no hay fecha de ingreso cargada."""
    ingreso = agente.fecha_ingreso
    if not ingreso:
        return 0
    meses = (hasta.year - ingreso.year) * 12 + (hasta.month - ingreso.month)
    if hasta.day < ingreso.day:
        meses -= 1
    return max(meses, 0)


def dias_licencia_ordinaria_correspondientes(agente, anio):
    """Días corridos de Licencia Anual Ordinaria según la antigüedad acreditada al
    31/12 del año (Art. 8, Ley 645-A)."""
    meses = antiguedad_meses(agente, date(anio, 12, 31))
    if meses < 6:
        return 0
    anios = meses / 12
    if anios <= 5:
        return 23
    if anios <= 10:
        return 28
    if anios <= 18:
        return 42
    return 49


def _cantidad_registrada(agente, tipo, anio):
    """Suma cruda de LicenciaPermiso no anuladas de `tipo` cuya fecha_desde cae en
    `anio`, sin aplicar ninguna regla de re-imputación entre años calendario (eso vive
    en `dias_usados`, que es lo que hay que llamar en general).

    Las fracciones que consumen el saldo de un CorteLicencia (`licenciapermiso_saldo_de_corte`)
    quedan afuera: no consumen el cupo del año en que se usan, sino el saldo ya
    descontado del cupo del año de la licencia original. El registro que fue cortado
    cuenta, a su vez, solo los días efectivamente gozados (`corte.cortelicencia_dias_gozados`)
    en vez de su `licenciapermiso_cantidad` completa."""
    registros = LicenciaPermiso.objects.filter(
        licenciapermiso_agente=agente,
        licenciapermiso_tipo=tipo,
        licenciapermiso_anulada=False,
        licenciapermiso_saldo_de_corte__isnull=True,
        licenciapermiso_fecha_desde__year=anio,
    ).select_related("corte")
    return sum(
        registro.corte.cortelicencia_dias_gozados if hasattr(registro, "corte") else registro.licenciapermiso_cantidad
        for registro in registros
    )


def dias_usados(agente, tipo, anio):
    """`_cantidad_registrada` más, para la Licencia Anual Ordinaria, los adelantos
    (Art. 10, tipo "Anual Proporcional") tomados el año calendario ANTERIOR con destino
    a este año: esos registros físicamente ocurren en `anio - 1` pero consumen el cupo
    de `anio`, no el de su propio año."""
    total = _cantidad_registrada(agente, tipo, anio)

    if tipo.tipolicenciapermiso_categoria == "LOR" and tipo.tipolicenciapermiso_nombre == LICENCIA_ANUAL_ORDINARIA_NOMBRE:
        adelantada = _tipo_anual_adelantada()
        if adelantada:
            total += _cantidad_registrada(agente, adelantada, anio - 1)

    return total


def saldos_pendientes_agente(agente):
    """Cortes de licencia del agente con saldo > 0 aún sin usar, para alertar sobre
    vencimientos próximos en el control de licencias."""
    cortes = CorteLicencia.objects.filter(
        cortelicencia_licencia__licenciapermiso_agente=agente,
    ).select_related("cortelicencia_licencia", "cortelicencia_licencia__licenciapermiso_tipo")
    return [corte for corte in cortes if corte.dias_restantes > 0]


def balance_tipo(agente, tipo, anio):
    """{correspondientes, usados, disponibles} para `tipo` en `anio`.
    `correspondientes`/`disponibles` quedan en `None` cuando el tope no es fijo.

    Para "Anual Proporcional" (Art. 10), `correspondientes` es el cupo de la Licencia
    Anual Ordinaria del año SIGUIENTE (`anio + 1`) que todavía no esté comprometido por
    licencias "Anual" ya registradas en ese año (los adelantos de este mismo `anio` se
    restan después, vía `usados`, con la fórmula genérica de `disponibles`)."""
    usados = dias_usados(agente, tipo, anio)

    if tipo.tipolicenciapermiso_categoria == "LOR" and tipo.tipolicenciapermiso_nombre == LICENCIA_ANUAL_ORDINARIA_NOMBRE:
        correspondientes = dias_licencia_ordinaria_correspondientes(agente, anio)
    elif tipo.tipolicenciapermiso_categoria == "LOR" and tipo.tipolicenciapermiso_nombre == LICENCIA_ANUAL_ADELANTADA_NOMBRE:
        anio_siguiente = anio + 1
        cupo_siguiente = dias_licencia_ordinaria_correspondientes(agente, anio_siguiente)
        tipo_anual = _tipo_anual_ordinaria()
        usado_siguiente = _cantidad_registrada(agente, tipo_anual, anio_siguiente) if tipo_anual else 0
        correspondientes = max(cupo_siguiente - usado_siguiente, 0)
    elif tipo.tipolicenciapermiso_tope_cantidad is not None and tipo.tipolicenciapermiso_tope_periodo == "ANI":
        correspondientes = tipo.tipolicenciapermiso_tope_cantidad
    else:
        correspondientes = None

    disponibles = (correspondientes - usados) if correspondientes is not None else None

    return {
        "tipo": tipo,
        "correspondientes": correspondientes,
        "usados": usados,
        "disponibles": disponibles,
    }


def resumen_agente(agente, anio):
    """Balance de todos los tipos activos para el agente, en el año dado."""
    tipos = TipoLicenciaPermiso.objects.filter(tipolicenciapermiso_activo=True)
    return [balance_tipo(agente, tipo, anio) for tipo in tipos]
