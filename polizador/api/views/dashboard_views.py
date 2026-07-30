# Dashboard app API views: aggregate data for the superuser-only usage dashboard.
from ninja import Router
from ninja.decorators import decorate_view
from ninja.errors import HttpError

from api.permissions import require_superuser
from api.schemas.dashboard_schemas import (
    LoginActivityResponseSchema,
    SentryHealthResponseSchema,
    ThroughputResponseSchema,
)
from core import dashboard_data

router = Router(tags=["dashboard"])


@router.get("/dashboard/throughput/{app_label}/", response=ThroughputResponseSchema)
@decorate_view(require_superuser)
def throughput(request, app_label: str):
    if app_label not in dashboard_data.TRACKED_MODELS:
        raise HttpError(404, f"Unknown app_label: {app_label}")
    series = {
        label: [{"period": period, "total": total} for period, total in points]
        for label, points in dashboard_data.record_throughput(app_label).items()
    }
    return {"series": series}


@router.get("/dashboard/logins/", response=LoginActivityResponseSchema)
@decorate_view(require_superuser)
def logins(request):
    points = dashboard_data.login_activity()
    summary = dashboard_data.login_summary()
    return {
        "series": [{"period": period, "total": total} for period, total in points],
        "today": summary["today"],
        "week": summary["week"],
    }


@router.get("/dashboard/sentry/", response=SentryHealthResponseSchema)
@decorate_view(require_superuser)
def sentry_health(request):
    health = dashboard_data.sentry_health()
    if health is None:
        return {"configured": False}
    return {
        "configured": True,
        "unresolved_count": health["unresolved_count"],
        "top_issues": health["top_issues"],
    }
