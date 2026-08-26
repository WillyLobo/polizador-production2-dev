# Core admin API views: infra cross-app usada por pantallas de /administracion/.
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ninja import Router
from ninja.decorators import decorate_view

from api.permissions import require_superuser
from api.views.generics import parse_order_by
from core.form_debug import build_ficha
from core.models import FormValidationError

router = Router(tags=["core"])

_ORDER_FIELDS = {
    "id": "id",
    "created_at": "created_at",
    "user": "user__username",
    "view_name": "view_name",
    "path": "path",
}


def _row(o):
    return {
        "id": o.id,
        "created_at": o.created_at.strftime("%Y-%m-%d %H:%M"),
        "user": str(o.user) if o.user_id else "—",
        "view_name": o.view_name.rsplit(".", 1)[-1],
        "path": o.path,
    }


@router.get("/datatables/errores-validacion/")
@decorate_view(require_superuser)
def datatable_errores_validacion(
    request, draw: int = 1, start: int = 0, length: int = 50, search: str = "", order_by: str = "-created_at",
):
    qs = FormValidationError.objects.select_related("user")
    records_total = qs.count()

    if search:
        qs = qs.filter(
            Q(view_name__icontains=search) | Q(path__icontains=search) | Q(user__username__icontains=search)
        )
    records_filtered = qs.count()

    qs = qs.order_by(*parse_order_by(order_by, _ORDER_FIELDS))
    page = qs[start:] if length == -1 else qs[start:start + length]

    return {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": [_row(o) for o in page],
    }


@router.get("/datatables/errores-validacion/{id}/detalle/")
@decorate_view(require_superuser)
def datatable_errores_validacion_detalle(request, id: int):
    record = get_object_or_404(FormValidationError.objects.select_related("user"), id=id)
    html = render_to_string(
        "ajax_datatable/core/formvalidationerror/render_row_details.html",
        {"record": record, "ficha": build_ficha(record)},
        request=request,
    )
    return {"html": html}
