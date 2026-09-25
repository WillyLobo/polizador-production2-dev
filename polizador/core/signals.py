from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import LoginEvent


def _client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    """Registra cada inicio de sesión para poder graficar actividad de usuarios en el dashboard.

    Guarda además con qué backend entró: django.contrib.auth.authenticate() deja
    la ruta en user.backend antes de que se emita esta señal (ver
    django/contrib/auth/__init__.py), así que acá ya está disponible. Es la
    evidencia de que alguien ya puede entrar por LDAP, que es la condición para
    retirarle después la contraseña local.
    """
    LoginEvent.objects.create(
        user=user,
        ip_address=_client_ip(request),
        backend=getattr(user, "backend", "") or "",
    )
