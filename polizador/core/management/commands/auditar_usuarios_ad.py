"""
Compara los usuarios activos de polizador contra el Active Directory del IPDUV
y dice cuales podrian autenticar por LDAP sin tocar nada y cuales habria que
vincular a mano.

Es de SOLO LECTURA: hace un bind con la cuenta de servicio y busca. No modifica
ni la base de polizador ni el AD.

Por que importa: django-auth-ldap busca al usuario de Django con
"username__iexact = <lo que se tipeo en el login>" (ver
django_auth_ldap/backend.py, _get_or_create_user). O sea que la mayuscula/
minuscula NO importa, pero cualquier otra diferencia si: si el username de
Django no es el sAMAccountName de la persona, el login por LDAP le falla
(AUTH_LDAP_NO_NEW_USERS lo rechaza en vez de crear una cuenta nueva) y sigue
entrando con su contrasena local.

Para los que no matchean, el comando propone candidatos usando ANR (Ambiguous
Name Resolution, la busqueda "difusa" propia de AD) sobre el nombre y apellido
que ya tiene cargados el CustomUser.

La configuracion sale de las variables GDU_LDAP_* del .env -- se leen de
os.environ y no de settings porque en main todavia no existen como settings
(LDAP vive en la rama visualizador-gdu).

    python manage.py auditar_usuarios_ad
    python manage.py auditar_usuarios_ad --detalle    # muestra displayName y mail
"""
import os

import ldap
from ldap.filter import escape_filter_chars

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

ATRIBUTOS = ["sAMAccountName", "displayName", "mail"]


class Command(BaseCommand):
    help = "Compara los usuarios activos contra el AD y reporta cuales habria que vincular a mano."

    def add_arguments(self, parser):
        parser.add_argument("--detalle", action="store_true", help="Muestra displayName y mail de cada match")
        parser.add_argument("--timeout", type=int, default=10)

    def handle(self, *args, **options):
        url, bind_dn, password, base = self._config()
        conn = self._conectar(url, bind_dn, password, options["timeout"])

        User = get_user_model()
        activos = User.objects.filter(is_active=True).order_by("username")

        exactos, por_case, sin_match = [], [], []
        for u in activos:
            entrada = self._buscar_sam(conn, base, u.username)
            if entrada is None:
                sin_match.append(u)
                continue
            sam = entrada.get("sAMAccountName", "")
            (exactos if sam == u.username else por_case).append((u, entrada))

        self.stdout.write(f"\nUsuarios activos: {activos.count()}\n")

        for u, entrada in exactos:
            self._linea("EXACTO", u, entrada, options["detalle"], self.style.SUCCESS)
        for u, entrada in por_case:
            self._linea(
                f"CASE  ->{entrada.get('sAMAccountName', '')}", u, entrada,
                options["detalle"], self.style.SUCCESS,
            )

        for u in sin_match:
            nombre = f"{u.first_name} {u.last_name}".strip()
            self.stdout.write(self.style.ERROR(
                f"  [SIN MATCH] {u.username:28s} {nombre}"
            ))
            for c in self._sugerir(conn, base, nombre):
                self.stdout.write(
                    f"{'':14s}  candidato: {c.get('sAMAccountName', ''):20s} "
                    f"{c.get('displayName', '')}"
                )

        conn.unbind_s()

        self.stdout.write("")
        self.stdout.write(f"  match exacto            : {len(exactos)}")
        self.stdout.write(f"  match solo por mayusculas: {len(por_case)}  (sirven igual: el lookup es __iexact)")
        self.stdout.write(f"  sin match               : {len(sin_match)}")
        if sin_match:
            self.stdout.write("")
            self.stdout.write("A vincular a mano: " + ", ".join(u.username for u in sin_match))

    # --- interno ---

    def _config(self):
        faltan = [k for k in (
            "GDU_LDAP_SERVER_URL", "GDU_LDAP_BIND_DN",
            "GDU_LDAP_BIND_CREDENTIALS", "GDU_LDAP_SEARCH_BASE",
        ) if not os.environ.get(k)]
        if faltan:
            raise CommandError(f"Faltan variables en el .env: {', '.join(faltan)}")
        return (
            os.environ["GDU_LDAP_SERVER_URL"],
            os.environ["GDU_LDAP_BIND_DN"],
            os.environ["GDU_LDAP_BIND_CREDENTIALS"],
            os.environ["GDU_LDAP_SEARCH_BASE"],
        )

    def _conectar(self, url, bind_dn, password, timeout):
        ldap.set_option(ldap.OPT_REFERRALS, 0)   # AD devuelve referrals que python-ldap no sigue bien
        ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, timeout)
        conn = ldap.initialize(url)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.set_option(ldap.OPT_NETWORK_TIMEOUT, timeout)
        conn.set_option(ldap.OPT_TIMEOUT, timeout)
        try:
            conn.simple_bind_s(bind_dn, password)
        except ldap.LDAPError as e:
            raise CommandError(f"No se pudo hacer bind como {bind_dn}: {e}")
        return conn

    def _buscar_sam(self, conn, base, username):
        filtro = f"(sAMAccountName={escape_filter_chars(username)})"
        for entrada in self._search(conn, base, filtro, 1):
            return entrada
        return None

    def _sugerir(self, conn, base, nombre):
        """Candidatos de AD para un usuario sin match, por ANR (Ambiguous Name
        Resolution, la busqueda difusa propia de AD: matchea cn, displayName,
        givenName, sn y sAMAccountName a la vez).

        Primero con el nombre completo. Si no da nada, busca por CADA token por
        separado y despues ordena los candidatos por cuantas palabras del nombre
        original aparecen en su displayName. Buscar token por token hace falta
        porque el nombre en polizador y el de AD casi nunca coinciden palabra por
        palabra: sobran nombres del medio ("Christian David Duarte" vs "David
        Duarte"), falta un apellido, o difieren los acentos. Y hay que consultar
        TODOS los tokens, no cortar en el primero que devuelva algo: el token mas
        distintivo suele ser el apellido, y quedarse con los 5 primeros de un
        nombre comun ("Alejandro") tapa al que se estaba buscando ("Melis").
        """
        if not nombre:
            return []
        filtro = "(&(objectCategory=person)(objectClass=user)(anr={}))"
        encontrados = self._search(conn, base, filtro.format(escape_filter_chars(nombre)), 5)
        if encontrados:
            return encontrados

        por_sam = {}
        for token in nombre.split():
            if len(token) < 4:
                continue
            for c in self._search(conn, base, filtro.format(escape_filter_chars(token)), 10):
                sam = c.get("sAMAccountName", "")
                if sam:
                    por_sam.setdefault(sam, c)

        buscados = {self._normalizar(t) for t in nombre.split() if len(t) >= 4}

        def puntaje(c):
            palabras = {self._normalizar(p) for p in c.get("displayName", "").split()}
            return len(buscados & palabras)

        ordenados = sorted(por_sam.values(), key=puntaje, reverse=True)
        # Un candidato que no comparte ninguna palabra con el nombre buscado es
        # ruido del token mas comun; no vale la pena ofrecerlo.
        return [c for c in ordenados if puntaje(c) > 0][:5]

    @staticmethod
    def _normalizar(texto):
        """Minusculas y sin acentos, para que "Ramírez" y "Ramirez" comparen igual."""
        import unicodedata

        descompuesto = unicodedata.normalize("NFKD", texto)
        return "".join(c for c in descompuesto if not unicodedata.combining(c)).lower()

    def _search(self, conn, base, filtro, limite):
        try:
            crudo = conn.search_s(base, ldap.SCOPE_SUBTREE, filtro, ATRIBUTOS)
        except ldap.LDAPError as e:
            self.stderr.write(self.style.WARNING(f"    (busqueda fallida: {e})"))
            return []
        salida = []
        for dn, attrs in crudo:
            if dn is None or not isinstance(attrs, dict):
                continue   # referral, no una entrada real
            salida.append({k: attrs[k][0].decode("utf-8", "replace") for k in ATRIBUTOS if attrs.get(k)})
            if len(salida) >= limite:
                break
        return salida

    def _linea(self, etiqueta, u, entrada, detalle, estilo):
        extra = ""
        if detalle:
            extra = f"  {entrada.get('displayName', ''):32s} {entrada.get('mail', '')}"
        self.stdout.write(estilo(f"  [{etiqueta:22s}] {u.username:28s}{extra}"))
