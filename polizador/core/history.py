import os
from collections import defaultdict
from datetime import date, datetime, timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import capfirst

HISTORY_TYPES = {
    "+": ("Creado", "success"),
    "~": ("Modificado", "primary"),
    "-": ("Eliminado", "danger"),
}

# Cambios consecutivos del mismo usuario separados por menos que esto se muestran
# como un solo bloque (p. ej. los cientos de celdas que guarda la matriz de Etapas).
GROUP_GAP = timedelta(minutes=2)

# CustomUser.password guarda el hash: se informa que cambió, nunca su valor.
REDACTED_FIELDS = {"password"}
# Cada login reescribe last_login y deja una fila histórica en CustomUser.
IGNORED_FIELDS = {"last_login"}

# Tope de filas históricas que se leen por modelo en las fuentes genéricas.
ROWS_PER_SOURCE = 1000


class HistorySource:
    """Filas históricas de un modelo, con la etiqueta a mostrar y una función que
    describe cada fila usando solo datos de la fila (o mapas armados de antemano),
    para no hacer una consulta por fila ni depender de que el objeto siga existiendo."""

    def __init__(self, label, rows, describe):
        self.label = label
        self.rows = rows
        self.describe = describe


def history_manager(model):
    attr = getattr(model._meta, "simple_history_manager_attribute", None)
    return getattr(model, attr) if attr else None


# modelo -> función(obj) que devuelve las HistorySource a mostrar para ese objeto.
_REGISTRY = {}


def register(model, children=(), sources=None):
    """Por defecto un objeto muestra solo su propio historial. `children` suma el de
    los modelos que lo referencian por FK (partes del objeto, p. ej. los movimientos
    de una póliza); `sources` reemplaza todo por una función propia."""
    _REGISTRY[model] = sources or (lambda obj: [own_source(obj)] + [child_source(obj, c) for c in children])


def sources_for(obj):
    fn = _REGISTRY.get(type(obj))
    return fn(obj) if fn else [own_source(obj)]


def _default_describe(model):
    campo = next(
        (
            f for f in history_manager(model).model.tracked_fields
            if isinstance(f, models.CharField) and not f.choices and not f.primary_key
        ),
        None,
    )

    def describe(row):
        valor = getattr(row, campo.attname) if campo else None
        return str(valor) if valor else f"#{getattr(row, model._meta.pk.attname)}"

    return describe


def _rows(queryset):
    return list(queryset.select_related("history_user").order_by("-history_date")[:ROWS_PER_SOURCE])


def own_source(obj):
    model = type(obj)
    rows = _rows(history_manager(model).filter(**{model._meta.pk.attname: obj.pk}))
    texto = str(obj)
    return HistorySource(capfirst(model._meta.verbose_name), rows, lambda r: texto)


def child_source(obj, child_model):
    fks = [
        f for f in child_model._meta.fields
        if (f.many_to_one or f.one_to_one) and f.related_model is type(obj)
    ]
    filtro = Q()
    for f in fks:
        filtro |= Q(**{f.attname: getattr(obj, f.target_field.attname)})
    rows = _rows(history_manager(child_model).filter(filtro))
    return HistorySource(capfirst(child_model._meta.verbose_name_plural), rows, _default_describe(child_model))


def _diff_fields(historical_model):
    # tracked_fields, no los del modelo: deja afuera los HistoricalRecords(excluded_fields=...).
    return [
        f for f in historical_model.tracked_fields
        if not f.primary_key and not isinstance(f, models.UUIDField) and f.name not in IGNORED_FIELDS
    ]


def _format(field, value, fk_labels):
    if value is None or value == "":
        return "—"
    if field.is_relation:
        return fk_labels.get((field.related_model, value), f"#{value} (eliminado)")
    if field.choices:
        return str(dict(field.flatchoices).get(value, value))
    if isinstance(value, bool):
        return "Sí" if value else "No"
    if isinstance(value, datetime):
        return timezone.localtime(value).strftime("%d/%m/%Y %H:%M")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    if isinstance(field, models.FileField):
        return os.path.basename(str(value))
    return str(value)


def build_timeline(sources, limit=500):
    """Arma la línea de tiempo (más reciente primero) de varias fuentes históricas,
    agrupada en bloques por usuario. Cada "Modificado" lleva el diff campo a campo
    contra la versión anterior del mismo objeto; los guardados sin cambios se omiten."""
    entries = []
    fk_ids = defaultdict(set)

    for source in sources:
        if not source.rows:
            continue
        model = type(source.rows[0]).instance_type
        fields = _diff_fields(type(source.rows[0]))
        by_object = defaultdict(list)
        for row in sorted(source.rows, key=lambda r: (r.history_date, r.history_id)):
            by_object[getattr(row, model._meta.pk.attname)].append(row)

        for versions in by_object.values():
            prev = None
            for row in versions:
                changes = []
                if row.history_type == "~" and prev is not None:
                    for f in fields:
                        old, new = getattr(prev, f.attname), getattr(row, f.attname)
                        if old != new:
                            changes.append((f, old, new))
                            if f.is_relation:
                                fk_ids[f.related_model].update(v for v in (old, new) if v is not None)
                prev = row
                if row.history_type == "~" and not changes:
                    continue
                tipo, color = HISTORY_TYPES.get(row.history_type, (row.history_type, "secondary"))
                entries.append({
                    "fecha": row.history_date,
                    "usuario": row.history_user,
                    "tipo": tipo,
                    "color": color,
                    "modelo": source.label,
                    "objeto": source.describe(row),
                    "cambios": changes,
                })

    entries.sort(key=lambda e: e["fecha"], reverse=True)
    truncated = len(entries) > limit
    entries = entries[:limit]

    fk_labels = {}
    for related_model, ids in fk_ids.items():
        for pk, obj in related_model._default_manager.in_bulk(ids).items():
            fk_labels[(related_model, pk)] = str(obj)
    for e in entries:
        e["cambios"] = [
            {
                "campo": f.verbose_name,
                "antes": "(oculto)" if f.name in REDACTED_FIELDS else _format(f, old, fk_labels),
                "despues": "(oculto)" if f.name in REDACTED_FIELDS else _format(f, new, fk_labels),
            }
            for f, old, new in e["cambios"]
        ]

    groups = []
    for e in entries:
        last = groups[-1] if groups else None
        if last and last["usuario"] == e["usuario"] and last["_desde"] - e["fecha"] <= GROUP_GAP:
            last["entradas"].append(e)
            last["_desde"] = e["fecha"]
        else:
            groups.append({"usuario": e["usuario"], "fecha": e["fecha"], "_desde": e["fecha"], "entradas": [e]})

    for g in groups:
        por_modelo = defaultdict(int)
        for e in g["entradas"]:
            por_modelo[e["modelo"]] += 1
        g["resumen"] = ", ".join(f"{modelo} ({n})" for modelo, n in por_modelo.items())

    counts = defaultdict(int)
    for e in entries:
        counts[e["modelo"]] += 1
    return {
        "grupos": groups,
        "modelos": [(s.label, counts[s.label]) for s in sources if counts[s.label]],
        "truncado": truncated,
        "limite": limit,
    }


def can_view_history(user, model):
    opts = model._meta
    return user.has_perm(f"{opts.app_label}.view_{opts.model_name}") or user.has_perm(
        f"{opts.app_label}.change_{opts.model_name}"
    )
