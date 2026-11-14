from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Count, prefetch_related_objects
from django.db.models.functions import TruncMonth
from django.utils import timezone

from carga.models import Certificado, FojaDeMedicion, Obra
from personalizador.models import (
    Agente,
    CorteLicencia,
    DevolucionHorasPermiso,
    LicenciaPermiso,
    TipoLicenciaPermiso,
)
from secretariador.models import Incorporacion, Solicitud

from .models import LoginEvent

TRACKED_MODELS = {
    "carga": [
        (Obra, "obra_history", "Obras"),
        (Certificado, "certificado_history", "Certificados"),
        (FojaDeMedicion, "foja_history", "Fojas de Medición"),
    ],
    "secretariador": [
        (Solicitud, "solicitud_history", "Solicitudes"),
        (Incorporacion, "incorporacion_history", "Incorporaciones"),
    ],
    "personalizador": [
        (Agente, "agente_history", "Agentes"),
        (TipoLicenciaPermiso, "tipolicenciapermiso_history", "Tipos de Licencia"),
        (LicenciaPermiso, "licenciapermiso_history", "Licencias/Permisos"),
        (CorteLicencia, "cortelicencia_history", "Cortes de Licencia"),
        (DevolucionHorasPermiso, "devolucionhoras_history", "Devoluciones de Horas"),
    ],
}

APP_DISPLAY_NAMES = {
    "carga": "Obras",
    "secretariador": "Viáticos",
    "personalizador": "Personal",
}

HISTORY_TYPE_LABELS = {"+": "Creado", "~": "Modificado", "-": "Eliminado"}

# FK paths each model's __str__ dereferences, so changes_feed() can resolve them in one
# bulk query per model instead of one query per row: h.instance rebuilds a bare instance
# from the historical row with no select_related, so any FK access in __str__ would
# otherwise hit the DB again for every one of the `limit` rows. Keep in sync with the
# __str__ methods of the models listed in TRACKED_MODELS.
STR_RELATED_FIELDS = {
    Obra: ["obra_empresa"],
    Certificado: ["certificado_obra__obra_empresa", "certificado_rubro_db"],
    FojaDeMedicion: ["foja_rubro__rubro_plan__trabajos_obra__obra_empresa"],
    LicenciaPermiso: ["licenciapermiso_tipo", "licenciapermiso_agente"],
    CorteLicencia: [
        "cortelicencia_licencia__licenciapermiso_tipo",
        "cortelicencia_licencia__licenciapermiso_agente",
    ],
}


def _light_instance(h, model):
    """Rebuild a model instance from a historical row without going through
    HistoricalRecords' `.instance` property: for models declared with
    HistoricalRecords(excluded_fields=...) (Obra, Certificado), that property issues one
    extra query PER ROW to refetch the excluded fields live from the current table, even
    though changes_feed only needs the instance for __str__(), which never reads them.
    Fields not present on the historical row (i.e. excluded ones) are simply left at
    their model default."""
    attrs = {}
    for field in model._meta.fields:
        try:
            attrs[field.attname] = getattr(h, field.attname)
        except AttributeError:
            pass
    return model(**attrs)


def changes_feed(app_label, limit=50):
    entries = []
    for model, history_attr, label in TRACKED_MODELS[app_label]:
        history_manager = getattr(model, history_attr)
        history_rows = list(
            history_manager.select_related("history_user").order_by("-history_date")[:limit]
        )
        instances = [_light_instance(h, model) for h in history_rows]
        related_fields = STR_RELATED_FIELDS.get(model)
        if related_fields and instances:
            prefetch_related_objects(instances, *related_fields)
        for h, instance in zip(history_rows, instances):
            try:
                objeto = str(instance)
            except ObjectDoesNotExist:
                # A related object __str__ depends on (e.g. a cascade-deleted parent) no
                # longer exists, even though this historical row does. Typically happens
                # for history_type "-" rows of records deleted via cascade.
                objeto = f"{label} #{instance.pk}"
            entries.append({
                "fecha": h.history_date,
                "usuario": h.history_user,
                "tipo": HISTORY_TYPE_LABELS.get(h.history_type, h.history_type),
                "modelo": label,
                "objeto": objeto,
            })
    entries.sort(key=lambda e: e["fecha"], reverse=True)
    return entries[:limit]


def _month_starts(months):
    """Primer día (hora local) de cada uno de los últimos `months` meses calendario,
    del más viejo al actual."""
    today = timezone.localdate()
    current = today.year * 12 + today.month - 1
    return [
        timezone.make_aware(datetime(index // 12, index % 12 + 1, 1))
        for index in range(current - months + 1, current + 1)
    ]


def record_throughput(app_label, months=12):
    """Altas hechas por usuarios, por mes calendario, de cada modelo seguido.

    Solo cuenta las filas "+" con history_user: las que no lo tienen no vienen de un
    pedido web sino de cargas en bloque (el poblado inicial del historial, importadores,
    comandos), que meten miles de altas en un día y aplastan la escala del gráfico.
    Devuelve todos los meses de la ventana, también los que no tuvieron altas (con 0),
    para que el eje del gráfico no tenga saltos.
    """
    month_starts = _month_starts(months)
    periods = [start.strftime("%Y-%m") for start in month_starts]
    since = month_starts[0]
    series = {}
    for model, history_attr, label in TRACKED_MODELS[app_label]:
        history_manager = getattr(model, history_attr)
        rows = (
            history_manager.filter(
                history_type="+", history_user__isnull=False, history_date__gte=since
            )
            .annotate(month=TruncMonth("history_date"))
            .values("month")
            .annotate(total=Count("pk"))
            .order_by("month")
        )
        totals = {row["month"].strftime("%Y-%m"): row["total"] for row in rows}
        series[label] = [(period, totals.get(period, 0)) for period in periods]
    return series


def recent_logins(limit=15):
    return list(
        LoginEvent.objects.order_by("-timestamp")[:limit].values("user__username", "timestamp")
    )


def login_summary():
    # Medianoche local, no UTC: timezone.now() está en UTC y su medianoche cae a las
    # 21:00 del día anterior en Argentina.
    today_start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    return {
        "today": LoginEvent.objects.filter(timestamp__gte=today_start).count(),
        "week": LoginEvent.objects.filter(timestamp__gte=week_start).count(),
    }


DASHBOARD_CACHE_TIMEOUT = 60  # segundos


SENTRY_ISSUES_LIMIT = 100  # máximo que admite la API por página


def sentry_health():
    """Issues sin resolver vistos en los últimos 14 días, vía la API de Sentry.

    Devuelve None si no está configurado (por ejemplo en desarrollo, donde tampoco se
    inicializa el SDK de Sentry) y {"error": True} si la consulta falló, para que el
    dashboard no muestre una falla como "No configurado". El resultado se cachea porque
    implica una llamada HTTP sincrónica a un servicio externo en cada carga del dashboard.
    """
    return cache.get_or_set("dashboard:sentry_health", _fetch_sentry_health, DASHBOARD_CACHE_TIMEOUT)


def _fetch_sentry_health():
    if not (settings.SENTRY_AUTH_TOKEN and settings.SENTRY_ORG and settings.SENTRY_PROJECT):
        return None

    # This account's DSN is on the US data region (o....ingest.us.sentry.io),
    # whose API lives on us.sentry.io rather than the legacy sentry.io host.
    # Endpoint de organización y no el de proyecto (obsoleto): en el de proyecto
    # statsPeriod solo elige las estadísticas que acompañan a cada issue, acá es la
    # ventana de tiempo de la búsqueda.
    url = f"https://us.sentry.io/api/0/organizations/{settings.SENTRY_ORG}/issues/"
    try:
        response = requests.get(
            url,
            params={
                "project": settings.SENTRY_PROJECT,
                "statsPeriod": "14d",
                "query": "is:unresolved",
                "sort": "freq",
                "limit": SENTRY_ISSUES_LIMIT,
            },
            headers={"Authorization": f"Bearer {settings.SENTRY_AUTH_TOKEN}"},
            timeout=5,
        )
        response.raise_for_status()
        issues = response.json()
        top_issues = [
            {"title": issue["title"], "count": str(issue["count"]), "url": issue["permalink"]}
            for issue in issues[:5]
        ]
        # La respuesta trae una sola página. El total real viene en X-Hits; si no viene
        # y hay otra página, lo contado es un piso ("100+").
        hits = response.headers.get("X-Hits", "")
        has_more = response.links.get("next", {}).get("results") == "true"
    except (requests.RequestException, KeyError, TypeError, ValueError, AttributeError):
        return {"error": True}
    if hits.isdigit():
        return {"unresolved_count": int(hits), "truncated": False, "top_issues": top_issues}
    return {"unresolved_count": len(issues), "truncated": has_more, "top_issues": top_issues}


def db_health():
    """Estado de la base vía las vistas pg_stat_* incorporadas de PostgreSQL
    (no requiere ninguna extensión, a diferencia de pg_stat_statements).
    Cacheado: es una foto del estado del servidor, no datos por-usuario."""
    return cache.get_or_set("dashboard:db_health", _fetch_db_health, DASHBOARD_CACHE_TIMEOUT)


def _fetch_db_health():
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
        db_size = cursor.fetchone()[0]

        # pg_stat_activity lista todas las conexiones a la base, también las ociosas
        # (y esta misma): "activas" son solo las que están ejecutando algo.
        cursor.execute(
            """
            SELECT count(*), count(*) FILTER (WHERE state = 'active')
            FROM pg_stat_activity WHERE datname = current_database()
            """
        )
        total_connections, active_connections = cursor.fetchone()

        cursor.execute(
            """
            SELECT xact_commit, xact_rollback, deadlocks, blks_hit, blks_read, stats_reset
            FROM pg_stat_database WHERE datname = current_database()
            """
        )
        xact_commit, xact_rollback, deadlocks, blks_hit, blks_read, stats_reset = cursor.fetchone()
        total_blocks = blks_hit + blks_read
        cache_hit_ratio = round(100 * blks_hit / total_blocks, 1) if total_blocks else None

        cursor.execute(
            """
            SELECT relname, pg_size_pretty(pg_total_relation_size(relid)), n_live_tup, n_dead_tup
            FROM pg_stat_user_tables
            ORDER BY pg_total_relation_size(relid) DESC
            LIMIT 5
            """
        )
        top_tables = [
            {"name": name, "size": size, "live_rows": live, "dead_rows": dead}
            for name, size, live, dead in cursor.fetchall()
        ]

    return {
        "size": db_size,
        "total_connections": total_connections,
        "active_connections": active_connections,
        # Desde cuándo acumulan commits, rollbacks y deadlocks (None: nunca se reiniciaron).
        "stats_reset": stats_reset,
        "commits": xact_commit,
        "rollbacks": xact_rollback,
        "deadlocks": deadlocks,
        "cache_hit_ratio": cache_hit_ratio,
        "top_tables": top_tables,
    }


def db_performance(limit=10):
    """Consultas más costosas vía pg_stat_statements.

    Devuelve None si la extensión no está instalada (por ejemplo en un entorno
    donde todavía no se corrió `CREATE EXTENSION pg_stat_statements`).
    Cacheado: es una foto del estado del servidor, no datos por-usuario.
    """
    return cache.get_or_set(
        f"dashboard:db_performance:{limit}", lambda: _fetch_db_performance(limit), DASHBOARD_CACHE_TIMEOUT
    )


def _fetch_db_performance(limit):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements'")
        if cursor.fetchone() is None:
            return None

        cursor.execute(
            """
            SELECT query, calls, round(total_exec_time::numeric, 1), round(mean_exec_time::numeric, 2)
            FROM pg_stat_statements
            WHERE query != '<insufficient privilege>'
              -- pg_stat_statements es de todo el cluster: sin esto se mezclan las
              -- consultas de las otras bases del servidor
              AND dbid = (SELECT oid FROM pg_database WHERE datname = current_database())
            ORDER BY total_exec_time DESC
            LIMIT %s
            """,
            [limit],
        )
        top_queries = [
            {
                "query": " ".join(query.split())[:200],
                "calls": calls,
                "total_ms": total_ms,
                "mean_ms": mean_ms,
            }
            for query, calls, total_ms, mean_ms in cursor.fetchall()
        ]

    return {"top_queries": top_queries}
