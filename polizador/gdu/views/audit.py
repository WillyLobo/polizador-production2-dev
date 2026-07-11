import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from gdu.models import AuditLogs


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    return forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")


@login_required
@require_POST
def post_log(request):
    """
    Equivalente a controllers/audit.js::postLog. A diferencia del original (un POST
    completamente público, sin passport.authenticate ni CSRF), acá se exige sesión
    Django autenticada + token CSRF estándar.
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = request.POST

    user_id = data.get("user_id")
    username = data.get("username")
    action = data.get("action")
    metadata = data.get("metadata")

    if not (user_id and username and action and metadata):
        return JsonResponse(
            {"errors": "faltan campos requeridos (user_id, username, action, metadata)"}, status=400,
        )

    AuditLogs.objects.create(
        tstamp=timezone.now(),
        user_id=user_id,
        username=username,
        action=action,
        client_addr=_client_ip(request),
        metadata=metadata,
    )
    return JsonResponse({"ok": True})
