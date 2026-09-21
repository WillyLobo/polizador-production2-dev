"""
Acceso de solo lectura al Active Directory del IPDUV.

Dos usos, los dos sin django-auth-ldap de por medio:

- `buscar_por_sam()`: lo usa core/management/commands/auditar_usuarios_ad.py
  para saber que usuarios de polizador tienen cuenta de red.
- `verificar_credenciales()`: lo usa la vista de vinculacion
  (core/views_vincular_ad.py). Un usuario YA logueado en polizador escribe su
  usuario y contrasena de red; si el bind funciona, queda probado que las dos
  identidades son de la misma persona y se guarda el sAMAccountName real que
  devolvio el AD en CustomUser.ad_username.

Por que no se reusa LDAPBackend para verificar: django-auth-ldap, despues de
autenticar, busca el CustomUser correspondiente y, si no lo encuentra, corta con
AUTH_LDAP_NO_NEW_USERS. Justamente lo que falta en ese momento es ese vinculo
-- es lo que se esta por crear -- asi que el backend no puede usarse para
crearlo. Aca solo interesa la pregunta "esta contrasena es la de esta cuenta de
red?", que es un bind y nada mas.

El bind es search-then-bind, igual que django-auth-ldap: se busca la entrada con
la cuenta de servicio para obtener su DN y despues se hace bind con ESE DN y la
contrasena del usuario. No se arma el DN a mano ni se usa el formato NT4
("IPDUV\\usuario"), que es lo que GeoServer necesito por otras razones (ver
geoserver/README.md en visualizador-gdu).

La configuracion sale de las variables GDU_LDAP_* del .env, leidas de
os.environ: en main todavia no existen como settings de Django.
"""
import os
from contextlib import contextmanager

import ldap
from ldap.filter import escape_filter_chars

ATRIBUTOS = ["sAMAccountName", "displayName", "mail"]
TIMEOUT = 10

VARIABLES = (
    "GDU_LDAP_SERVER_URL",
    "GDU_LDAP_BIND_DN",
    "GDU_LDAP_BIND_CREDENTIALS",
    "GDU_LDAP_SEARCH_BASE",
)


class ADNoConfigurado(RuntimeError):
    """Faltan variables GDU_LDAP_* en el .env."""


class ADNoDisponible(RuntimeError):
    """El AD no responde, o la cuenta de servicio no pudo hacer bind."""


def hay_configuracion():
    return all(os.environ.get(v) for v in VARIABLES)


def _config():
    faltan = [v for v in VARIABLES if not os.environ.get(v)]
    if faltan:
        raise ADNoConfigurado(f"Faltan variables en el .env: {', '.join(faltan)}")
    return tuple(os.environ[v] for v in VARIABLES)


def _conectar(url, timeout=TIMEOUT):
    conn = ldap.initialize(url)
    # OPT_REFERRALS=0: AD devuelve referrals que python-ldap no sigue bien y
    # terminan como entradas con dn=None. Los timeouts evitan que una consulta a
    # un AD caido cuelgue el request de un usuario.
    conn.set_option(ldap.OPT_REFERRALS, 0)
    conn.set_option(ldap.OPT_NETWORK_TIMEOUT, timeout)
    conn.set_option(ldap.OPT_TIMEOUT, timeout)
    return conn


def _entradas(crudo, limite):
    salida = []
    for dn, attrs in crudo:
        if dn is None or not isinstance(attrs, dict):
            continue   # referral, no una entrada real
        datos = {k: attrs[k][0].decode("utf-8", "replace") for k in ATRIBUTOS if attrs.get(k)}
        datos["dn"] = dn
        salida.append(datos)
        if len(salida) >= limite:
            break
    return salida


@contextmanager
def conexion(timeout=TIMEOUT):
    """Conexion ya bindeada con la cuenta de servicio, para hacer varias
    busquedas sin re-bindear en cada una (lo usa auditar_usuarios_ad, que hace
    una busqueda por usuario mas las de sugerencias)."""
    url, bind_dn, password, _ = _config()
    conn = _conectar(url, timeout)
    try:
        conn.simple_bind_s(bind_dn, password)
    except ldap.LDAPError as e:
        raise ADNoDisponible(str(e)) from e
    try:
        yield conn
    finally:
        try:
            conn.unbind_s()
        except ldap.LDAPError:
            pass


def buscar(filtro, limite=5, timeout=TIMEOUT, conn=None):
    """Busca en el AD con la cuenta de servicio. Devuelve lista de dicts.

    Con `conn` reusa una conexion abierta con conexion(); sin ella abre y cierra
    una propia.
    """
    if conn is None:
        with conexion(timeout) as propia:
            return buscar(filtro, limite, timeout, propia)
    _, _, _, base = _config()
    try:
        crudo = conn.search_s(base, ldap.SCOPE_SUBTREE, filtro, ATRIBUTOS)
    except ldap.LDAPError as e:
        raise ADNoDisponible(str(e)) from e
    return _entradas(crudo, limite)


def buscar_por_sam(username, timeout=TIMEOUT, conn=None):
    """La entrada de AD cuyo sAMAccountName es `username`, o None."""
    entradas = buscar(f"(sAMAccountName={escape_filter_chars(username)})", 1, timeout, conn)
    return entradas[0] if entradas else None


def verificar_credenciales(username, password, timeout=TIMEOUT):
    """Devuelve la entrada de AD si `password` es la contrasena de `username`.

    None si el usuario no existe o la contrasena es incorrecta -- los dos casos
    se devuelven igual a proposito, para no decirle a quien prueba cual de las
    dos cosas fallo.

    Levanta ADNoDisponible si el problema es del AD y no de las credenciales,
    para poder mostrar "el servidor no responde" en vez de "contrasena
    incorrecta" cuando el AD esta caido.
    """
    if not username or not password:
        return None

    url, _, _, _ = _config()
    entrada = buscar_por_sam(username, timeout)
    if entrada is None:
        return None

    conn = _conectar(url, timeout)
    try:
        conn.simple_bind_s(entrada["dn"], password)
    except ldap.INVALID_CREDENTIALS:
        return None
    except ldap.LDAPError as e:
        raise ADNoDisponible(str(e)) from e
    finally:
        try:
            conn.unbind_s()
        except ldap.LDAPError:
            pass
    return entrada
