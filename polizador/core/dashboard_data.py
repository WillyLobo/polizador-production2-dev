from collections import defaultdict
from datetime import datetime, timedelta

import requests
from django.apps import apps
from django.conf import settings
from django.contrib.gis.db.models import GeometryField
from django.core.cache import cache
from django.db import connection
from django.db.models import Count, IntegerField, Model, Value, prefetch_related_objects
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.utils.text import capfirst

from .history import history_manager
from .models import LoginEvent

HISTORY_TYPE_LABELS = {"+": "Creado", "~": "Modificado", "-": "Eliminado"}

CHANGES_PAGE_SIZE = 50
# Modelos que el gráfico de altas muestra por separado; el resto va sumado en "Otros".
THROUGHPUT_TOP_MODELS = 5
THROUGHPUT_OTHERS_LABEL = "Otros"


def tracked_apps():
    """{app_label: [modelos]} con todo modelo instalado que tenga historial
    (simple_history), en el orden de INSTALLED_APPS y, dentro de cada app, por nombre.

    No hay lista que mantener: una app o un modelo nuevo con HistoricalRecords aparece
    solo. Para sacar uno ruidoso, sumarlo a settings.DASHBOARD_EXCLUDED_MODELS como
    "app_label.Modelo".
    """
    excluded = {label.lower() for label in getattr(settings, "DASHBOARD_EXCLUDED_MODELS", ())}
    tracked = {}
    for config in apps.get_app_configs():
        models = [
            model for model in config.get_models()
            if history_manager(model) is not None and model._meta.label_lower not in excluded
        ]
        if models:
            tracked[config.label] = sorted(models, key=lambda model: model_label(model).lower())
    return tracked


def model_label(model):
    return capfirst(str(model._meta.verbose_name_plural))


def _heavy_fields(historical_model):
    """Campos que no hace falta traer para mostrar un cambio en el feed y pesan: las
    geometrías (un polígono de parcela son varios KB por fila)."""
    return [field.name for field in historical_model._meta.fields if isinstance(field, GeometryField)]


def _light_instance(h, model):
    """Rebuild a model instance from a historical row without going through
    HistoricalRecords' `.instance` property: for models declared with
    HistoricalRecords(excluded_fields=...) (Obra, Certificado), that property issues one
    extra query PER ROW to refetch the excluded fields live from the current table, even
    though changes_feed only needs the instance for __str__(), which never reads them.
    Fields not present on the historical row (i.e. excluded ones) and the ones the feed
    deferred (see _heavy_fields) are simply left at their model default."""
    deferred = h.get_deferred_fields()
    attrs = {}
    for field in model._meta.fields:
        if field.attname in deferred:
            continue  # leerlo dispararía una consulta por fila
        try:
            attrs[field.attname] = getattr(h, field.attname)
        except AttributeError:
            pass
    return model(**attrs)


def _related_paths(instance, prefix="", depth=0):
    """Caminos de relacionados ("fk__otra_fk") que ya se leyeron desde `instance`: Django
    guarda en fields_cache cada relacionado al que se accede, así que después de un
    str(instance) esto dice exactamente qué recorrió su __str__."""
    paths = []
    if depth > 8:  # un ciclo (A -> B -> A) no debería darse, pero que no cuelgue
        return paths
    for name, related in instance._state.fields_cache.items():
        if isinstance(related, Model):
            path = prefix + name
            paths.extend(_related_paths(related, path + "__", depth + 1) or [path])
    return paths


def _describe(instances, model):
    """str() de cada instancia, sin una consulta por fila.

    Las instancias se arman desde filas históricas, sin select_related, y muchos __str__
    recorren relacionados (un ítem de etapa nombra su ítem, su rubro, su plan y su obra):
    con 50 filas eran cientos de consultas. Se describe la primera, se mira qué
    relacionados usó su __str__ y se precargan esos mismos para las demás, con una
    consulta por nivel. No hay lista que mantener: sigue a los __str__ tal como estén.
    """
    texts = []
    learned = False
    for position, instance in enumerate(instances):
        try:
            text = str(instance)
        except Exception:
            # El __str__ no se pudo armar desde la fila histórica: típicamente un
            # relacionado que ya no existe (filas "-" de registros borrados en cascada),
            # o un __str__ que no tolera un campo vacío. Un texto de menos no justifica
            # perder el feed entero.
            text = f"{capfirst(str(model._meta.verbose_name))} #{instance.pk}"
        else:
            if not learned:
                learned = True
                paths = _related_paths(instance)
                rest = instances[position + 1:]
                if paths and rest:
                    prefetch_related_objects(rest, *paths)
        texts.append(text)
    return texts


def changes_feed(app_label, model_name=None, limit=CHANGES_PAGE_SIZE, offset=0):
    """Últimos cambios de los modelos con historial de una app (o de uno solo, si se pasa
    `model_name`), del más nuevo al más viejo. Devuelve (cambios, hay_mas).

    En dos pasos, para que el costo no dependa de cuántos modelos tenga la app:
    1. una sola consulta (UNION ALL) trae fecha e id de las filas históricas de todos los
       modelos y se queda con las `limit` de la página;
    2. solo de esas se cargan las filas completas, agrupadas por modelo.
    """
    models = tracked_apps()[app_label]
    if model_name is not None:
        models = [model for model in models if model._meta.model_name == model_name]

    keys = [
        history_manager(model)
        .order_by()
        .annotate(model_index=Value(index, output_field=IntegerField()))
        .values_list("history_date", "history_id", "model_index")
        for index, model in enumerate(models)
    ]
    if not keys:
        return [], False
    combined = keys[0].union(*keys[1:], all=True) if len(keys) > 1 else keys[0]
    # limit + 1: la fila de más solo dice si hay otra página
    page = list(combined.order_by("-history_date", "-history_id", "model_index")[offset:offset + limit + 1])
    has_more = len(page) > limit
    page = page[:limit]

    ids_by_model = defaultdict(list)
    for _, history_id, model_index in page:
        ids_by_model[model_index].append(history_id)

    entries = {}
    for model_index, history_ids in ids_by_model.items():
        model = models[model_index]
        label = model_label(model)
        manager = history_manager(model)
        history_rows = list(
            manager.filter(history_id__in=history_ids)
            .select_related("history_user")
            .defer(*_heavy_fields(manager.model))
        )
        instances = [_light_instance(h, model) for h in history_rows]
        for h, objeto in zip(history_rows, _describe(instances, model)):
            entries[(model_index, h.history_id)] = {
                "fecha": h.history_date,
                "usuario": h.history_user,
                "tipo": HISTORY_TYPE_LABELS.get(h.history_type, h.history_type),
                "modelo": label,
                "objeto": objeto,
            }
    return [entries[(model_index, history_id)] for _, history_id, model_index in page], has_more


def _month_starts(months):
    """Primer día (hora local) de cada uno de los últimos `months` meses calendario,
    del más viejo al actual."""
    today = timezone.localdate()
    current = today.year * 12 + today.month - 1
    return [
        timezone.make_aware(datetime(index // 12, index % 12 + 1, 1))
        for index in range(current - months + 1, current + 1)
    ]


def record_throughput(app_label, months=12, top=THROUGHPUT_TOP_MODELS):
    """Altas hechas por usuarios, por mes calendario, de los modelos con historial de la app.

    Solo cuenta las filas "+" con history_user: las que no lo tienen no vienen de un
    pedido web sino de cargas en bloque (el poblado inicial del historial, importadores,
    comandos), que meten miles de altas en un día y aplastan la escala del gráfico.
    Devuelve todos los meses de la ventana, también los que no tuvieron altas (con 0),
    para que el eje del gráfico no tenga saltos.

    Con decenas de modelos el gráfico apilado no se lee: van por separado los `top` con
    más altas en la ventana y el resto sumado en "Otros". Los que no tuvieron ninguna
    no aparecen.
    """
    month_starts = _month_starts(months)
    periods = [start.strftime("%Y-%m") for start in month_starts]
    since = month_starts[0]
    totals_by_label = {}
    for model in tracked_apps()[app_label]:
        rows = (
            history_manager(model)
            .filter(history_type="+", history_user__isnull=False, history_date__gte=since)
            .order_by()
            .annotate(month=TruncMonth("history_date"))
            .values("month")
            .annotate(total=Count("pk"))
        )
        totals = {row["month"].strftime("%Y-%m"): row["total"] for row in rows}
        if totals:
            totals_by_label[model_label(model)] = totals

    # de mayor a menor; a igual cantidad, por nombre, para que el orden sea estable
    ranked = sorted(totals_by_label, key=lambda label: (-sum(totals_by_label[label].values()), label))
    series = {
        label: [(period, totals_by_label[label].get(period, 0)) for period in periods]
        for label in ranked[:top]
    }
    others = ranked[top:]
    if others:
        series[THROUGHPUT_OTHERS_LABEL] = [
            (period, sum(totals_by_label[label].get(period, 0) for label in others)) for period in periods
        ]
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
