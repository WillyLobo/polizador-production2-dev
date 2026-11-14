import ipaddress
import logging

from django.contrib.auth.signals import user_logged_in
from django.db import transaction
from django.dispatch import receiver

from .models import LoginEvent

logger = logging.getLogger(__name__)


def _client_ip(request):
    """IP del cliente, o None si no hay ninguna válida.

    Se confía en la primera entrada de X-Forwarded-For porque en el servidor nginx la
    pisa con la dirección real del cliente (que a su vez saca de CF-Connecting-IP solo
    cuando el pedido viene del túnel de Cloudflare). No leer CF-Connecting-IP acá: un
    cliente que entra por la LAN, sin pasar por Cloudflare, puede mandar ese header.
    El valor se valida porque fuera de ese nginx (desarrollo, otro proxy) el header lo
    escribe el cliente, y uno que no sea una IP hacía fallar el INSERT y, con él, el login.
    """
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR") or ""
    for candidato in (forwarded_for.split(",")[0].strip(), request.META.get("REMOTE_ADDR")):
        try:
            return str(ipaddress.ip_address(candidato))
        except ValueError:
            continue
    return None


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
                ip_address=_client_ip(request),
                backend=getattr(user, "backend", "") or "",
            )
    except Exception:
        logger.exception("No se pudo registrar el inicio de sesión de %s", user)
