from functools import wraps

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from ninja.errors import AuthenticationError

User = get_user_model()

# HTTP method -> Django's default model-permission action, matching the
# `permission_required = "<app_label>.<action>_<model_name>"` convention already
# used by the CBVs in carga/views and secretariador/views.
_METHOD_ACTION = {
    "GET": "view",
    "POST": "add",
    "PUT": "change",
    "PATCH": "change",
    "DELETE": "delete",
}


def require_auth(request):
    if not request.user.is_authenticated:
        raise AuthenticationError()
    return request.user


def require_model_perm(model, action=None):
    """Require the standard Django permission for `model` on this endpoint.

    The action is inferred from the HTTP method (GET->view, POST->add,
    PUT/PATCH->change, DELETE->delete) unless explicitly given. The permission
    string is derived from the model itself (`app_label.action_model_name`),
    so it always matches the permission Django actually created for it.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            act = action or _METHOD_ACTION.get(request.method, "view")
            perm = f"{model._meta.app_label}.{act}_{model._meta.model_name}"
            if not request.user.has_perm(perm):
                return JsonResponse({"detail": "Permission denied"}, status=403)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def get_optional_perms(*perms):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not any(request.user.has_perm(p) for p in perms):
                return JsonResponse({"detail": "Permission denied"}, status=403)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def get_group_perms(*groups):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name__in=groups).exists():
                return JsonResponse({"detail": "Group access required"}, status=403)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
