"""
Compara los usuarios activos de polizador contra el Active Directory del IPDUV
y dice cuantos podrian autenticar por LDAP sin tocar nada.

Es de SOLO LECTURA: busca con la cuenta de servicio y no modifica ni la base de
polizador ni el AD.

Desde que existe la vinculacion self-service (core/views_vincular_ad.py, donde
cada usuario prueba su propia cuenta de red con sus credenciales) este comando
ya no es la forma de armar el mapeo: es el panorama previo y el seguimiento
despues. Dice cuanta gente va a vincularse sin friccion, quienes tienen el
username sin relacion con su cuenta de red, y -- lo mas util -- quienes podrian
directamente no tener cuenta en el AD.

django-auth-ldap busca al usuario de Django con "username__iexact" (ver
_get_or_create_user en django_auth_ldap/backend.py), asi que las diferencias de
mayusculas NO cuentan como problema y se reportan aparte.

    python manage.py auditar_usuarios_ad
    python manage.py auditar_usuarios_ad --detalle    # muestra displayName y mail
"""
import unicodedata

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from ldap.filter import escape_filter_chars

from core import ldap_ad
from core.models import LoginEvent

ANR = "(&(objectCategory=person)(objectClass=user)(anr={}))"


class Command(BaseCommand):
    help = "Compara los usuarios activos contra el AD y reporta cuales no tienen match."

    def add_arguments(self, parser):
        parser.add_argument("--detalle", action="store_true", help="Muestra displayName y mail de cada match")

    def handle(self, *args, **options):
        detalle = options["detalle"]
        User = get_user_model()
        activos = list(User.objects.filter(is_active=True).order_by("username"))

        try:
            with ldap_ad.conexion() as conn:
                exactos, por_case, sin_match = [], [], []
                for u in activos:
                    entrada = ldap_ad.buscar_por_sam(u.username, conn=conn)
                    if entrada is None:
                        sin_match.append(u)
                    elif entrada.get("sAMAccountName") == u.username:
                        exactos.append((u, entrada))
                    else:
                        por_case.append((u, entrada))

                self.stdout.write(f"\nUsuarios activos: {len(activos)}\n")
                for u, entrada in exactos:
                    self._linea("EXACTO", u, entrada, detalle)
                for u, entrada in por_case:
                    self._linea(f"CASE ->{entrada.get('sAMAccountName', '')}", u, entrada, detalle)

                for u in sin_match:
                    nombre = f"{u.first_name} {u.last_name}".strip()
                    vinculado = f"  (ya vinculado a {u.ad_username})" if u.ad_username else ""
                    self.stdout.write(self.style.ERROR(f"  [SIN MATCH] {u.username:28s} {nombre}{vinculado}"))
                    for c in self._sugerir(conn, nombre):
                        self.stdout.write(
                            f"{'':14s}  candidato: {c.get('sAMAccountName', ''):20s} {c.get('displayName', '')}"
                        )
        except (ldap_ad.ADNoConfigurado, ldap_ad.ADNoDisponible) as e:
            raise CommandError(str(e))

        self.stdout.write("")
        self.stdout.write(f"  match exacto             : {len(exactos)}")
        self.stdout.write(f"  match solo por mayusculas: {len(por_case)}  (sirven igual: el lookup es __iexact)")
        self.stdout.write(f"  sin match                : {len(sin_match)}")
        ya = sum(1 for u in activos if u.ad_username)
        self.stdout.write(f"  con ad_username cargado  : {ya}/{len(activos)}  (vinculacion self-service)")
        # Condicion para el paso siguiente: a un usuario solo se le retira la
        # contrasena local despues de haberlo VISTO entrar por LDAP.
        vistos = (
            LoginEvent.objects.filter(backend__endswith="LDAPBackend", user__in=activos)
            .values_list("user_id", flat=True).distinct().count()
        )
        self.stdout.write(f"  ya entraron por LDAP     : {vistos}/{len(activos)}  (listos para set_unusable_password)")
        if sin_match:
            self.stdout.write("")
            self.stdout.write("Sin match por username: " + ", ".join(u.username for u in sin_match))

    def _sugerir(self, conn, nombre):
        """Candidatos de AD por ANR (Ambiguous Name Resolution, la busqueda
        difusa propia de AD: matchea cn, displayName, givenName, sn y
        sAMAccountName a la vez).

        Primero con el nombre completo; si no da nada, token por token. Hay que
        consultar TODOS los tokens y no cortar en el primero que devuelva algo:
        el token distintivo suele ser el apellido, y los 5 primeros resultados
        de un nombre comun ("Alejandro") tapaban al que se buscaba ("Melis").
        Despues se ordena por cuantas palabras del nombre comparten, sin
        acentos, porque "Ramírez" y "Ramirez" conviven en los dos sistemas.
        """
        if not nombre:
            return []
        encontrados = ldap_ad.buscar(ANR.format(escape_filter_chars(nombre)), 5, conn=conn)
        if encontrados:
            return encontrados

        por_sam = {}
        for token in nombre.split():
            if len(token) < 4:
                continue
            for c in ldap_ad.buscar(ANR.format(escape_filter_chars(token)), 10, conn=conn):
                sam = c.get("sAMAccountName", "")
                if sam:
                    por_sam.setdefault(sam, c)

        buscados = {self._normalizar(t) for t in nombre.split() if len(t) >= 4}

        def puntaje(c):
            return len(buscados & {self._normalizar(p) for p in c.get("displayName", "").split()})

        ordenados = sorted(por_sam.values(), key=puntaje, reverse=True)
        # Un candidato sin ninguna palabra en comun es ruido del token mas comun.
        return [c for c in ordenados if puntaje(c) > 0][:5]

    @staticmethod
    def _normalizar(texto):
        descompuesto = unicodedata.normalize("NFKD", texto or "")
        return "".join(c for c in descompuesto if not unicodedata.combining(c)).lower()

    def _linea(self, etiqueta, u, entrada, detalle):
        extra = ""
        if detalle:
            extra = f"  {entrada.get('displayName', ''):32s} {entrada.get('mail', '')}"
        self.stdout.write(self.style.SUCCESS(f"  [{etiqueta:22s}] {u.username:28s}{extra}"))
