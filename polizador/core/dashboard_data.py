from datetime import timedelta

import requests
from django.conf import settings
from django.db import connection
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone

from carga.models import Certificado, FojaDeMedicion, Obra
from personalizador.models import Agente
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
    ],
}

APP_DISPLAY_NAMES = {
    "carga": "Obras",
    "secretariador": "Viáticos",
    "personalizador": "Personal",
}

HISTORY_TYPE_LABELS = {"+": "Creado", "~": "Modificado", "-": "Eliminado"}


def changes_feed(app_label, limit=50):
    entries = []
    for model, history_attr, label in TRACKED_MODELS[app_label]:
        history_manager = getattr(model, history_attr)
        qs = history_manager.select_related("history_user").order_by("-history_date")[:limit]
        for h in qs:
            entries.append({
                "fecha": h.history_date,
                "usuario": h.history_user,
                "tipo": HISTORY_TYPE_LABELS.get(h.history_type, h.history_type),
                "modelo": label,
                "objeto": str(h.instance),
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


def login_activity(days=30):
    since = timezone.now() - timedelta(days=days)
    rows = (
        LoginEvent.objects.filter(timestamp__gte=since)
        .annotate(day=TruncDay("timestamp"))
        .values("day")
        .annotate(total=Count("pk"))
        .order_by("day")
    )
    return [(row["day"].strftime("%Y-%m-%d"), row["total"]) for row in rows]


def login_summary():
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    return {
        "today": LoginEvent.objects.filter(timestamp__gte=today_start).count(),
        "week": LoginEvent.objects.filter(timestamp__gte=week_start).count(),
    }


def sentry_health():
    """Cantidad de issues sin resolver en los últimos 14 días, vía la API de Sentry.

    Devuelve None si no está configurado (por ejemplo en desarrollo, donde
    tampoco se inicializa el SDK de Sentry).
    """
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
    (no requiere ninguna extensión, a diferencia de pg_stat_statements)."""
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
