import json
from typing import Any, List, Optional

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.html import escape
from ninja import Field, Schema
from ninja.decorators import decorate_view
from ninja.pagination import PaginationBase

from api.permissions import require_model_perm


class PerPagePagination(PaginationBase):
    """Replicates this API's original `?page=&per_page=` contract
    (`{count, next, previous, results}`) on top of ninja's pagination hook."""

    class Input(Schema):
        page: int = Field(1, ge=1)
        per_page: int = Field(50, ge=1, le=200)

    class Output(Schema):
        count: int
        next: Optional[str] = None
        previous: Optional[str] = None
        results: List[Any]

    items_attribute = "results"

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        per_page = pagination.per_page
        start = (page - 1) * per_page
        end = start + per_page
        total = self._items_count(queryset)
        return {
            "results": queryset[start:end],
            "count": total,
            "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
            "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        }


def parse_order_by(order_by: str, fields_map: dict, default_field: str = "id") -> list:
    """Turns a comma-separated, optionally '-'-prefixed list of datatable column
    keys (as sent by ninja-datatable.js) into ORM `order_by()` clauses, mapping
    each key through `fields_map` (falling back to `default_field`)."""
    clauses = []
    for part in filter(None, (p.strip() for p in order_by.split(","))):
        desc = part.startswith("-")
        key = part[1:] if desc else part
        field = fields_map.get(key, default_field)
        clauses.append(f"-{field}" if desc else field)
    return clauses or [default_field]


def clip_value_html(text, max_length: int) -> str:
    """Replicates ajax_datatable's `max_length` column truncation: wraps the value
    in a `<span title="full text">` and clips the visible text with an ellipsis."""
    text = str(text)
    short = text if len(text) <= max_length else text[:max_length]
    html = f'<span title="{escape(text)}">{escape(short)}'
    if len(text) > max_length:
        html += "&hellip;"
    return html + "</span>"


def format_thousands(value) -> str:
    """Formats a number with '.' as thousands separator and ',' as decimal mark,
    replicating the `locale.format_string("%.2f", value, True)` used by the
    legacy ajax_datatable views without touching the process-wide locale."""
    return f"{float(value):,.2f}".translate(str.maketrans({",": "X", ".": ","})).replace("X", ".")


def render_datatable_row_details(model, obj, request) -> str:
    """Renders the row-detail expansion HTML for a datatable row: a model-specific
    `ajax_datatable/<app>/<model>/render_row_details.html` template if one exists,
    falling back to a generic field/value dump (mirrors AjaxDatatableView's
    `render_row_details` default behavior)."""
    template_name = f"ajax_datatable/{model._meta.app_label}/{model._meta.model_name}/render_row_details.html"
    try:
        return render_to_string(template_name, {"model": model, "object": obj}, request=request)
    except TemplateDoesNotExist:
        m2m_names = {f.name for f in model._meta.get_fields() if f.many_to_many and f.concrete}
        rows = []
        for f in model._meta.get_fields():
            if not f.concrete:
                continue
            if f.name in m2m_names:
                value = ", ".join(str(x) for x in getattr(obj, f.name).all())
            else:
                try:
                    value = getattr(obj, f.name)
                except AttributeError:
                    continue
            rows.append(f"<tr><td>{escape(f.name)}</td><td>{escape(value)}</td></tr>")
        return '<table class="row-details">' + "".join(rows) + "</table>"


def register_simple_datatable(
    router,
    model,
    url_slug: str,
    *,
    order_fields: dict,
    filter_fields: dict,
    search_lookups: list,
    row_builder,
    default_order: str = "id",
    queryset=None,
    with_detail: bool = True,
    boolean_filter_keys: frozenset = frozenset(),
):
    """Registers `GET /datatables/<url_slug>/` (+ `.../<{id}>/detalle/` unless
    `with_detail=False`) for a "simple" list: one model, a handful of columns,
    permission-gated action links, no bespoke per-row computation beyond
    `row_builder(obj, user) -> dict`. Covers the ~10 lookup-table style listings
    (Aseguradora, Programa, Departamento, ...) that were otherwise near-identical
    copies of the same AjaxDatatableView boilerplate.

    `boolean_filter_keys` names the `filter_fields` keys backed by a BooleanField:
    the "true"/"false" strings sent by a <select> filter get coerced before
    `.filter()`, same as the dedicated Solicitud/Obra endpoints do inline."""
    base_qs = model.objects.all() if queryset is None else queryset

    @router.get(f"/datatables/{url_slug}/", operation_id=f"datatable_{url_slug}_list")
    @decorate_view(require_model_perm(model))
    def _list(
        request,
        draw: int = 1,
        start: int = 0,
        length: int = 50,
        search: str = "",
        order_by: str = default_order,
        filters: str = "{}",
    ):
        qs = base_qs
        records_total = qs.count()

        try:
            active_filters = json.loads(filters)
        except (TypeError, ValueError):
            active_filters = {}
        for key, value in active_filters.items():
            lookup = filter_fields.get(key)
            if not lookup or value in (None, ""):
                continue
            if key in boolean_filter_keys:
                qs = qs.filter(**{lookup: value in ("true", "True", "1")})
            else:
                qs = qs.filter(**{lookup: value})

        if search and search_lookups:
            search_q = Q()
            for lookup in search_lookups:
                search_q |= Q(**{lookup: search})
            qs = qs.filter(search_q).distinct()

        records_filtered = qs.count()
        qs = qs.order_by(*parse_order_by(order_by, order_fields), "id")
        page = qs[start:] if length == -1 else qs[start:start + length]

        return {
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": [row_builder(o, request.user) for o in page],
        }

    if not with_detail:
        return _list, None

    @router.get(f"/datatables/{url_slug}/{{id}}/detalle/", operation_id=f"datatable_{url_slug}_detalle")
    @decorate_view(require_model_perm(model))
    def _detalle(request, id: int):
        obj = get_object_or_404(model, id=id)
        return {"html": render_datatable_row_details(model, obj, request)}

    return _list, _detalle
