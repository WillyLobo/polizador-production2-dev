"""Cálculo de saldos de licencias y permisos (Ley 645-A).

Funciones puras que no dependen de vistas: reciben un `Agente` y devuelven la
cantidad de días/horas correspondientes, usados y disponibles para un tipo de
licencia/permiso en un año calendario dado.

Los 3 tipos "año-vencido" (Anual, Anual Proporcional y Anual de Invierno) anclan su
año a un `PeriodoLicencia` explícito (`personalizador.models.PeriodoLicencia`), en vez
de inferirlo implícitamente de `licenciapermiso_fecha_desde.year`. Anual y Anual
Proporcional además COMPARTEN el mismo `PeriodoLicencia` de un año dado: Anual
Proporcional (Art. 10) no tiene cupo propio, adelanta días del mismo pozo de la Anual
Ordinaria (Art. 7) — ver `periodo_objetivo`. El resto de los tipos (Permisos, Motivos
de Salud, etc.) sigue infiriendo el año directamente de `fecha_desde.year`, como antes.
"""
from datetime import date

from django.core.exceptions import ValidationError

from personalizador.models import CorteLicencia, LicenciaPermiso, PeriodoLicencia, PeriodoLicenciaAgente, TipoLicenciaPermiso

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

# tipo.tipolicenciapermiso_nombre -> PeriodoLicencia.categoria. Los 3 tipos apuntan
# al período de su propio fecha_desde.year (año de devengamiento, "año vencido": el
# período <año> recién abre el 15/12/<año> y se goza mayormente en <año + 1>, pero
# sigue siendo el período <año>). Anual Proporcional (Art. 10) es un adelanto sobre
# el mismo pozo de Anual (Art. 7) -- por eso comparten categoría LOR_ANUAL en vez de
# tener cupo propio; Invierno usa su propia categoría porque no comparte ese pozo.
# Nota: la planilla de RRHH (ver importar_control_licencias.py) rotula la columna de
# adelanto con año+1 (ej. "adelanto 2026" en la hoja "L.O.A. 2025"), pero es una
# etiqueta coloquial por el año en que mayormente se goza, no el año de devengamiento
# -- el período sigue siendo el de fecha_desde.year.
_MAPEO_CATEGORIA = {
    LICENCIA_ANUAL_ORDINARIA_NOMBRE: "LOR_ANUAL",
    LICENCIA_ANUAL_ADELANTADA_NOMBRE: "LOR_ANUAL",
    LICENCIA_ANUAL_INVIERNO_NOMBRE: "LOR_INVIERNO",
}


def _tipo_anual_adelantada():
    return TipoLicenciaPermiso.objects.filter(
        tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre=LICENCIA_ANUAL_ADELANTADA_NOMBRE,
    ).first()


def _tipo_anual_ordinaria():
    return TipoLicenciaPermiso.objects.filter(
        tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre=LICENCIA_ANUAL_ORDINARIA_NOMBRE,
    ).first()


def periodo_objetivo(tipo_nombre, anio_base):
    """(categoria, anio) del PeriodoLicencia que corresponde a `tipo_nombre` cuando
    `anio_base` es el año de referencia (típicamente fecha_desde.year, o el `anio`
    pasado por un caller de reporting como balance_tipo/dias_usados). Devuelve None
    si `tipo_nombre` no es uno de los 3 tipos año-vencido."""
    categoria = _MAPEO_CATEGORIA.get(tipo_nombre)
    if categoria is None:
        return None
    return categoria, anio_base


def get_periodo(categoria, anio):
    """PeriodoLicencia existente para (categoria, anio), o None. No crea nada."""
    return PeriodoLicencia.objects.filter(
        periodolicencia_categoria=categoria, periodolicencia_anio=anio,
    ).first()


def get_or_create_periodo_agente(agente, periodo):
    """Congelado perezoso del cupo por antigüedad de `agente` contra `periodo`
    (solo tiene sentido para periodo.categoria == "LOR_ANUAL": Invierno no tiene
    cupo por antigüedad). La primera vez que se necesita, se calcula con
    `dias_licencia_ordinaria_correspondientes` y se guarda; llamadas siguientes
    siempre devuelven el valor ya guardado, sin recalcular -- para que una
    corrección posterior de `agente.fecha_ingreso` no altere retroactivamente
    balances de períodos ya otorgados."""
    return PeriodoLicenciaAgente.objects.get_or_create(
        periodolicenciaagente_agente=agente,
        periodolicenciaagente_periodo=periodo,
        defaults={
            "periodolicenciaagente_dias_correspondientes": dias_licencia_ordinaria_correspondientes(
                agente, periodo.periodolicencia_anio,
            ),
        },
    )[0]


def resolver_periodo_para_licencia(tipo, fecha_desde):
    """Usado desde `LicenciaPermiso.clean()` para completar
    `licenciapermiso_periodo`. Si `tipo` no es uno de los 3 tipos año-vencido,
    devuelve None sin levantar error (el campo queda sin usar para ese tipo). Si lo
    es, resuelve el `PeriodoLicencia` correspondiente; si todavía no existe, levanta
    ValidationError pidiendo crearlo primero -- no se autocrea, porque apertura/
    fecha límite (o los turnos de Invierno) son datos legales reales que el sistema
    no debe inventar en silencio."""
    if tipo.tipolicenciapermiso_categoria != "LOR":
        return None
    resultado = periodo_objetivo(tipo.tipolicenciapermiso_nombre, fecha_desde.year)
    if resultado is None:
        return None
    categoria, anio = resultado
    periodo = get_periodo(categoria, anio)
    if periodo is None:
        categoria_display = dict(PeriodoLicencia.CATEGORIA).get(categoria, categoria)
        raise ValidationError(
            f"No existe el período de licencia '{categoria_display} {anio}'. Debe crearlo "
            "primero en Licencias > Períodos antes de cargar esta licencia."
        )
    return periodo


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
    `anio`, sin aplicar ninguna regla de re-imputación entre años calendario. Se usa
    para los tipos que NO son año-vencido (no tienen PeriodoLicencia); para los 3
    que sí lo son, usar `_cantidad_registrada_periodo`.

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


def _cantidad_registrada_periodo(agente, tipo, periodo):
    """Igual que `_cantidad_registrada`, pero filtrando por `licenciapermiso_periodo`
    en vez de `fecha_desde__year` -- usada para los 3 tipos año-vencido, que anclan
    su año a un PeriodoLicencia explícito en vez de inferirlo de la fecha."""
    registros = LicenciaPermiso.objects.filter(
        licenciapermiso_agente=agente,
        licenciapermiso_tipo=tipo,
        licenciapermiso_anulada=False,
        licenciapermiso_saldo_de_corte__isnull=True,
        licenciapermiso_periodo=periodo,
    ).select_related("corte")
    return sum(
        registro.corte.cortelicencia_dias_gozados if hasattr(registro, "corte") else registro.licenciapermiso_cantidad
        for registro in registros
    )


def dias_usados(agente, tipo, anio):
    """Cantidad de `tipo` usada por `agente`, imputada al año `anio`. Para los 3
    tipos año-vencido se resuelve contra el `PeriodoLicencia` explícito (ver
    `periodo_objetivo`); si ese período todavía no existe, devuelve 0 (no puede
    haber ninguna `LicenciaPermiso` apuntando a un período inexistente). Para el
    resto de los tipos, sigue infiriendo por `fecha_desde__year`.

    Para la Licencia Anual Ordinaria, además de lo registrado directamente contra
    el período, suma los adelantos (Art. 10, tipo "Anual Proporcional") tomados
    contra ESE MISMO período: como Anual y Anual Proporcional comparten
    PeriodoLicencia, ya no hace falta ningún corrimiento de año a mano."""
    resultado = periodo_objetivo(tipo.tipolicenciapermiso_nombre, anio)
    if resultado is None:
        return _cantidad_registrada(agente, tipo, anio)

    categoria, anio_periodo = resultado
    periodo = get_periodo(categoria, anio_periodo)
    if periodo is None:
        return 0

    total = _cantidad_registrada_periodo(agente, tipo, periodo)

    if tipo.tipolicenciapermiso_categoria == "LOR" and tipo.tipolicenciapermiso_nombre == LICENCIA_ANUAL_ORDINARIA_NOMBRE:
        adelantada = _tipo_anual_adelantada()
        if adelantada:
            total += _cantidad_registrada_periodo(agente, adelantada, periodo)

    return total


def saldos_pendientes_agente(agente):
    """Cortes de licencia del agente con saldo > 0 aún sin usar, para alertar sobre
    vencimientos próximos en el control de licencias."""
    cortes = CorteLicencia.objects.filter(
        cortelicencia_licencia__licenciapermiso_agente=agente,
    ).select_related("cortelicencia_licencia", "cortelicencia_licencia__licenciapermiso_tipo")
    return [corte for corte in cortes if corte.dias_restantes > 0]


def _cupo_periodo(agente, periodo, anio_periodo):
    """Días correspondientes por antigüedad para `agente` en `periodo`: lee el
    snapshot congelado (PeriodoLicenciaAgente) si ya existe; si no, hace un
    fallback de SOLO LECTURA (no crea nada) al cálculo en vivo, para poder mostrar
    una estimación antes de que exista snapshot (el snapshot recién se crea desde
    `LicenciaPermiso.clean()`, al guardar la primera licencia contra ese período)."""
    snapshot = PeriodoLicenciaAgente.objects.filter(
        periodolicenciaagente_agente=agente, periodolicenciaagente_periodo=periodo,
    ).first()
    if snapshot:
        return snapshot.periodolicenciaagente_dias_correspondientes
    return dias_licencia_ordinaria_correspondientes(agente, anio_periodo)


def balance_tipo(agente, tipo, anio):
    """{correspondientes, usados, disponibles} para `tipo` en `anio`.
    `correspondientes`/`disponibles` quedan en `None` cuando el tope no es fijo.

    Para "Anual Proporcional" (Art. 10), `correspondientes` es el cupo de la Licencia
    Anual Ordinaria del MISMO período (`anio`, comparte pozo con "Anual") que
    todavía no esté comprometido por licencias "Anual" ya registradas contra ese
    período (los adelantos de este mismo `anio` se restan después, vía `usados`, con
    la fórmula genérica de `disponibles`)."""
    if tipo.tipolicenciapermiso_categoria == "LOR" and tipo.tipolicenciapermiso_nombre == LICENCIA_ANUAL_ORDINARIA_NOMBRE:
        categoria, anio_periodo = periodo_objetivo(tipo.tipolicenciapermiso_nombre, anio)
        periodo = get_periodo(categoria, anio_periodo)
        correspondientes = _cupo_periodo(agente, periodo, anio_periodo) if periodo else dias_licencia_ordinaria_correspondientes(agente, anio_periodo)
    elif tipo.tipolicenciapermiso_categoria == "LOR" and tipo.tipolicenciapermiso_nombre == LICENCIA_ANUAL_ADELANTADA_NOMBRE:
        categoria, anio_periodo = periodo_objetivo(tipo.tipolicenciapermiso_nombre, anio)
        periodo = get_periodo(categoria, anio_periodo)
        cupo_periodo = _cupo_periodo(agente, periodo, anio_periodo) if periodo else dias_licencia_ordinaria_correspondientes(agente, anio_periodo)
        tipo_anual = _tipo_anual_ordinaria()
        usado_periodo = _cantidad_registrada_periodo(agente, tipo_anual, periodo) if (tipo_anual and periodo) else 0
        correspondientes = max(cupo_periodo - usado_periodo, 0)
    elif tipo.tipolicenciapermiso_tope_cantidad is not None and tipo.tipolicenciapermiso_tope_periodo == "ANI":
        correspondientes = tipo.tipolicenciapermiso_tope_cantidad
    else:
        correspondientes = None

    usados = dias_usados(agente, tipo, anio)
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
