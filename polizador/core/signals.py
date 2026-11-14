import logging

from django.contrib.auth.signals import user_logged_in
from django.db import transaction
from django.dispatch import receiver

from .client_ip import client_ip
from .models import LoginEvent

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    """Registra cada inicio de sesión para poder graficar actividad de usuarios en el dashboard.

    Guarda además con qué backend entró: django.contrib.auth.authenticate() deja
    la ruta en user.backend antes de que se emita esta señal (ver
    django/contrib/auth/__init__.py), así que acá ya está disponible. Es la
    evidencia de que alguien ya puede entrar por LDAP, que es la condición para
    retirarle después la contraseña local.

    Es un registro auxiliar: si no se puede guardar, se deja constancia del error y el
    login sigue. El atomic() es un savepoint, para que un INSERT fallido no deje
    abortada la transacción en la que corre el login.
    """
    try:
        with transaction.atomic():
            LoginEvent.objects.create(
                user=user,
                ip_address=client_ip(request),
                backend=getattr(user, "backend", "") or "",
            )
    except Exception:
        logger.exception("No se pudo registrar el inicio de sesión de %s", user)
