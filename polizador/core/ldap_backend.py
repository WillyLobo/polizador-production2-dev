"""
Backend de LDAP de polizador.

Existe por una sola razon: decidir que hacer cuando alguien con cuenta en el AD
del IPDUV se loguea y todavia no tiene CustomUser. La politica es que pueda
entrar -- sin ningun permiso, que despues le asigna un superusuario desde el
panel -- y eso obliga a resolver dos cosas que django-auth-ldap no resuelve solo
con AUTH_LDAP_NO_NEW_USERS=False.

1. El usuario recien construido vendria con username vacio.

   Con AUTH_LDAP_USER_QUERY_FIELD="ad_username", _get_or_create_user construye
   el usuario nuevo como CustomUser(ad_username=<sAMAccountName>) y despues lo
   puebla con AUTH_LDAP_USER_ATTR_MAP, que a proposito solo mapea ad_username
   (mapear first_name/last_name haria que cada login por LDAP pise los nombres
   curados en polizador). Resultado: username="". El primero se guardaria asi y
   el segundo reventaria con IntegrityError, porque username es unico.

2. Habria cuentas duplicadas para la mitad del padron.

   De 29 usuarios activos, 16 tienen el username igual a su cuenta de red pero
   todavia no vincularon (ad_username sigue en NULL). Si uno de ellos entra con
   sus credenciales del AD antes de vincular, la busqueda por ad_username no lo
   encuentra y se construiria un usuario NUEVO con el mismo username -- otro
   IntegrityError, y en el mejor caso una cuenta duplicada sin permisos al lado
   de la que si los tiene.

   Por eso, antes de dar por nuevo a alguien, se lo busca por username__iexact.
   Si aparece, se adopta esa cuenta: se le completa ad_username y sigue con sus
   grupos y su historia. Es lo mismo que hace django-auth-ldap por defecto
   cuando no hay USER_QUERY_FIELD, y de paso vincula solo a esos 16.

   El supuesto es que un username de polizador y un sAMAccountName iguales son
   la misma persona. Para un padron institucional de 29 cuentas es razonable, y
   el audit (manage.py auditar_usuarios_ad) mostro que en los 16 casos los
   nombres coinciden. Queda registrado en el log por si alguna vez no lo fuera.
"""
import logging

from django.contrib.auth import get_user_model
from django_auth_ldap.backend import LDAPBackend

logger = logging.getLogger(__name__)


def _attr(ldap_user, nombre):
    valores = ldap_user.attrs.get(nombre) or []
    return valores[0] if valores else ""


class PolizadorLDAPBackend(LDAPBackend):
    def get_or_build_user(self, username, ldap_user):
        user, built = super().get_or_build_user(username, ldap_user)
        if not built:
            return user, built

        # El nombre canonico es el que devolvio el AD, no lo que se tipeo en el
        # formulario (que puede venir con otra combinacion de mayusculas).
        sam = _attr(ldap_user, "sAMAccountName") or username

        User = get_user_model()
        existente = User.objects.filter(username__iexact=sam).first()
        if existente is not None:
            logger.info(
                "LDAP: se adopta la cuenta existente '%s' para el usuario de red '%s'",
                existente.username, sam,
            )
            existente.ad_username = sam
            return existente, False

        # Cuenta nueva: sin grupos, sin permisos, sin staff. Que sirva para algo
        # es trabajo de un superusuario desde el panel de Django.
        user.username = sam
        user.first_name = _attr(ldap_user, "givenName")
        user.last_name = _attr(ldap_user, "sn")
        user.email = _attr(ldap_user, "mail")
        logger.warning(
            "LDAP: alta automatica de '%s' (%s) -- entra sin permisos hasta que "
            "un superusuario le asigne grupos",
            sam, _attr(ldap_user, "displayName"),
        )
        return user, True
