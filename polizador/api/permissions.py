from django.contrib.auth import get_user_model
import datetime as dt
from ninja.errors import HttpError, AuthenticationError, AuthorizationError

User = get_user_model()


def require_auth(request):
    if not request.user.is_authenticated:
        raise AuthenticationError()
    return request.user


def require_staff(request):
    user = require_auth(request)
    if not user.is_staff:
        raise AuthorizationError(status_code=403, message="Staff access required")
    return user


def get_optional_perms(*perms):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user = require_auth(request)
            if not any(user.has_perm(p) for p in perms):
                raise AuthorizationError(status_code=403, message="Permission denied")
            return func(request, *args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def get_group_perms(*groups):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user = require_auth(request)
            if not any(user.groups.filter(name=g).exists() for g in groups):
                raise AuthorizationError(status_code=403, message="Group access required")
            return func(request, *args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator
