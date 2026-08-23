from datetime import timedelta

import requests
from django.conf import settings
from django.core.cache import cache
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
            entries.append({
                "fecha": h.history_date,
                "usuario": h.history_user,
                "tipo": HISTORY_TYPE_LABELS.get(h.history_type, h.history_type),
                "modelo": label,
                "objeto": str(instance),
            })
    entries.sort(key=lambda e: e["fecha"], reverse=True)
    return entries[:limit]


def record_throughput(app_label, months=12):
    since = timezone.now() - timedelta(days=30 * months)
    series = {}
    for model, history_attr, label in TRACKED_MODELS[app_label]:
        history_manager = getattr(model, history_attr)
        rows = (
            history_manager.filter(history_type="+", history_date__gte=since)
            .annotate(month=TruncMonth("history_date"))
            .values("month")
            .annotate(total=Count("pk"))
            .order_by("month")
        )
        series[label] = [(row["month"].strftime("%Y-%m"), row["total"]) for row in rows]
    return series


def recent_logins(limit=15):
    return list(
        LoginEvent.objects.select_related("user")
        .order_by("-timestamp")[:limit]
        .values("user__username", "timestamp", "ip_address")
    )


def login_summary():
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    return {
        "today": LoginEvent.objects.filter(timestamp__gte=today_start).count(),
        "week": LoginEvent.objects.filter(timestamp__gte=week_start).count(),
    }


DASHBOARD_CACHE_TIMEOUT = 60  # segundos


def sentry_health():
    """Cantidad de issues sin resolver en los últimos 14 días, vía la API de Sentry.

    Devuelve None si no está configurado (por ejemplo en desarrollo, donde
    tampoco se inicializa el SDK de Sentry). El resultado se cachea porque implica
    una llamada HTTP sincrónica a un servicio externo en cada carga del dashboard.
    """
    return cache.get_or_set("dashboard:sentry_health", _fetch_sentry_health, DASHBOARD_CACHE_TIMEOUT)


def _fetch_sentry_health():
    if not (settings.SENTRY_AUTH_TOKEN and settings.SENTRY_ORG and settings.SENTRY_PROJECT):
        return None

    # This account's DSN is on the US data region (o....ingest.us.sentry.io),
    # whose API lives on us.sentry.io rather than the legacy sentry.io host.
    url = f"https://us.sentry.io/api/0/projects/{settings.SENTRY_ORG}/{settings.SENTRY_PROJECT}/issues/"
    try:
        response = requests.get(
            url,
            params={"statsPeriod": "14d", "query": "is:unresolved"},
            headers={"Authorization": f"Bearer {settings.SENTRY_AUTH_TOKEN}"},
            timeout=5,
        )
        response.raise_for_status()
        issues = response.json()
    except requests.RequestException:
        return None
    return {
        "unresolved_count": len(issues),
        "top_issues": [
            {"title": issue["title"], "count": issue["count"], "url": issue["permalink"]}
            for issue in issues[:5]
        ],
    }


def db_health():
    """Estado de la base vía las vistas pg_stat_* incorporadas de PostgreSQL
    (no requiere ninguna extensión, a diferencia de pg_stat_statements).
    Cacheado: es una foto del estado del servidor, no datos por-usuario."""
    return cache.get_or_set("dashboard:db_health", _fetch_db_health, DASHBOARD_CACHE_TIMEOUT)


def _fetch_db_health():
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
        db_size = cursor.fetchone()[0]

        cursor.execute(
            "SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()"
        )
        active_connections = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT xact_commit, xact_rollback, deadlocks, blks_hit, blks_read
            FROM pg_stat_database WHERE datname = current_database()
            """
        )
        xact_commit, xact_rollback, deadlocks, blks_hit, blks_read = cursor.fetchone()
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
        "active_connections": active_connections,
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
