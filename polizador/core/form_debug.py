import re

from django import forms
from django.utils.module_loading import import_string

MATRIZ_FIELD_RE = re.compile(r"^item_(\d+)_col_(\d+)$")
FORMSET_FIELD_RE = re.compile(r"^([\w-]+)-(\d+)-(.+)$")


def resolve_class(dotted_path):
    """import_string tolerante: devuelve None si el path esta vacio o ya no
    se puede importar (renombrado, form dinamico sin path estable, etc.)."""
    if not dotted_path:
        return None
    try:
        return import_string(dotted_path)
    except (ImportError, AttributeError, ValueError):
        return None


def humanize_value(field, raw_values):
    """Convierte una lista de valores crudos de POST a texto legible, segun el
    tipo del `field` original. `field` puede ser None (no se pudo resolver la
    form_class) -> siempre cae al dump por defecto."""
    if field is None:
        return ", ".join(raw_values) if raw_values else "—"

    if isinstance(field, forms.BooleanField):
        return "Sí" if raw_values else "No"

    if isinstance(field, forms.ModelMultipleChoiceField):
        try:
            objs = field.queryset.in_bulk(raw_values)
        except (ValueError, TypeError):
            objs = {}
        return ", ".join(str(objs[v]) if v in objs else v for v in raw_values) if raw_values else "—"

    if isinstance(field, forms.ModelChoiceField):
        if not raw_values:
            return "—"
        pk = raw_values[0]
        try:
            obj = field.queryset.filter(pk=pk).first()
        except (ValueError, TypeError):
            obj = None
        return str(obj) if obj else pk

    if getattr(field, "choices", None):
        choices = dict(field.choices)
        return ", ".join(str(choices.get(v, v)) for v in raw_values) if raw_values else "—"

    if isinstance(field, forms.MultiValueField):
        try:
            compressed = field.compress(raw_values)
            return str(compressed) if compressed not in (None, "") else "—"
        except Exception:
            return ", ".join(raw_values) if raw_values else "—"

    return ", ".join(raw_values) if raw_values else "—"


def group_formset_rows(raw_data):
    """Separa las claves 'prefix-N-campo' en {(prefix, row_index): {campo: valores}},
    devuelve (filas, resto_top_level_sin_agrupar)."""
    rows = {}
    remaining = {}
    for key, values in raw_data.items():
        match = FORMSET_FIELD_RE.match(key)
        if not match:
            remaining[key] = values
            continue
        prefix, index, field_name = match.group(1), int(match.group(2)), match.group(3)
        if field_name in ("TOTAL_FORMS", "INITIAL_FORMS", "MIN_NUM_FORMS", "MAX_NUM_FORMS"):
            continue
        rows.setdefault((prefix, index), {})[field_name] = values
    return rows, remaining


def group_matriz_fields(raw_data):
    """Agrupa claves item_<pk>_col_<n> en {item_pk: {col_index: valor}}."""
    grid = {}
    for key, values in raw_data.items():
        match = MATRIZ_FIELD_RE.match(key)
        if not match:
            continue
        item_pk, col = int(match.group(1)), int(match.group(2))
        grid.setdefault(item_pk, {})[col] = values[0] if values else ""
    return grid


def _humanize_fields(fields_dict, field_source):
    """`fields_dict` es {nombre: [valores]}; `field_source` es un dict de
    nombre->forms.Field (declared_fields de la form_class, o {} si no se pudo
    resolver) usado para elegir el humanizador correcto por campo."""
    return [
        {"name": name, "label": getattr(field_source.get(name), "label", None) or name,
         "value": humanize_value(field_source.get(name), values)}
        for name, values in fields_dict.items()
    ]


def build_ficha(record):
    """Punto de entrada: transforma un FormValidationError en una estructura
    lista para el template de detalle."""
    matriz = group_matriz_fields(record.raw_data)
    if matriz:
        return {
            "kind": "matriz",
            "rows": sorted(
                ({"item_pk": pk, "cols": sorted(cols.items())} for pk, cols in matriz.items()),
                key=lambda r: r["item_pk"],
            ),
        }

    form_cls = resolve_class(record.form_class_path)
    form_fields = getattr(form_cls, "declared_fields", {}) if form_cls else {}

    formset_rows_raw, remaining = group_formset_rows(record.raw_data)

    formset_field_sources = {}
    for meta in record.formsets:
        formset_cls = resolve_class(meta.get("class_path"))
        row_form_cls = getattr(formset_cls, "form", None) if formset_cls else None
        formset_field_sources[meta.get("prefix")] = getattr(row_form_cls, "declared_fields", {})

    formset_rows = [
        {
            "prefix": prefix,
            "index": index,
            "fields": _humanize_fields(fields, formset_field_sources.get(prefix, {})),
        }
        for (prefix, index), fields in sorted(formset_rows_raw.items())
    ]

    return {
        "kind": "form",
        "fields": _humanize_fields(remaining, form_fields),
        "formset_rows": formset_rows,
    }
