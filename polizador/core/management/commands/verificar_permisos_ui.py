"""
Verifica que cada gate de la UI, ahora expresado como PERMISO de Django, le de
acceso exactamente al mismo conjunto de usuarios activos que le daba el nombre
de GRUPO que reemplazo.

Existe porque los gates por nombre de grupo ("gciaoperativa_usuarios" in groups)
fallan en silencio: un grupo renombrado o un typo evaluan a falso/verdadero sin
error (ver el bug historico de templates/index.html:6, donde "group" en singular
-- variable inexistente -- hacia que la condicion fuera siempre verdadera). Un
permiso mal escrito en cambio es simplemente falso y se nota, pero el momento
peligroso es la migracion en si: hay que probar que el permiso elegido cubre a
la misma gente. Eso es lo que mide este comando.

Correrlo contra una replica de produccion ANTES de desplegar un cambio de gates,
y de nuevo despues. Sale con codigo 1 si algun gate cambio de alcance, asi sirve
en un paso de CI o como chequeo previo manual.

    python manage.py verificar_permisos_ui
    python manage.py verificar_permisos_ui --detalle     # lista usernames
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

# Cada entrada documenta un gate de la UI y su traduccion.
#   modo "alguno":  el usuario pasa si esta en ALGUNO de `grupos`
#   modo "ninguno": el usuario pasa si no esta en NINGUNO de `grupos`
#   superuser_en_grupos: si el template viejo tenia "or request.user.is_superuser"
#   y_permisos: permisos que la version VIEJA exigia ADEMAS del grupo (AND), como
#       en los endpoints de la API que combinaban get_group_perms con require_model_perm
#   acepta_superusuarios: diferencias compuestas SOLO por superusuarios son
#       esperadas y no marcan fallo (has_perm() siempre es True para ellos, asi
#       que la version con permisos los incluye aunque el grupo no los tuviera)
EQUIVALENCIAS = [
    {
        "ubicacion": "templates/navbar.html:20",
        "gate": "Menu Obras",
        "grupos": ["gciaoperativa_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": True,
        "permisos": ["carga.view_obra"],
    },
    {
        "ubicacion": "templates/navbar.html:70",
        "gate": "Menu Localidades",
        "grupos": ["localidades_todos_los_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": True,
        "permisos": ["carga.view_localidad"],
    },
    {
        "ubicacion": "templates/navbar.html:93",
        "gate": "Menu RRHH",
        "grupos": ["rrhh_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": True,
        # view_agente NO sirve: lo tiene tambien gciaoperativa_usuarios (+7 usuarios).
        # add_agente es de rrhh_usuarios en exclusiva.
        "permisos": ["personalizador.add_agente"],
    },
    {
        "ubicacion": "templates/navbar.html:145",
        "gate": "Menu Viaticos",
        "grupos": ["dirgral_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": True,
        "permisos": ["secretariador.view_comisionadosolicitud"],
    },
    {
        "ubicacion": "templates/navbar.html:178",
        "gate": "Menu Herramientas",
        "grupos": ["gciaoperativa_usuarios", "dirgral_usuarios", "rrhh_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": True,
        "permisos": [
            "carga.view_obra",
            "secretariador.view_comisionadosolicitud",
            "personalizador.add_agente",
        ],
    },
    {
        "ubicacion": "templates/navbar.html:193",
        "gate": "Menu Reportes",
        "grupos": ["gciaoperativa_usuarios", "dirgral_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": True,
        "permisos": ["carga.view_obra", "secretariador.view_comisionadosolicitud"],
    },
    {
        "ubicacion": "templates/navbar.html:200",
        "gate": "Reportes > tarjetas de obra",
        "grupos": ["gciaoperativa_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": True,
        "permisos": ["carga.view_obra"],
    },
    {
        "ubicacion": "templates/navbar.html:220",
        "gate": "Reportes > tarjetas de viaticos",
        "grupos": ["dirgral_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": True,
        "permisos": ["secretariador.view_comisionadosolicitud"],
    },
    {
        "ubicacion": "templates/index.html:21",
        "gate": "Home de inspeccion",
        "grupos": ["inspeccion"],
        "modo": "alguno",
        "superuser_en_grupos": False,
        # view_contrato NO sirve: lo tiene tambien gciaoperativa_usuarios (+7).
        "permisos": ["carga.change_fojademedicion"],
        "acepta_superusuarios": True,
    },
    {
        "ubicacion": "templates/index.html:24",
        "gate": "Home de certificadores",
        "grupos": ["certificadores"],
        "modo": "alguno",
        "superuser_en_grupos": False,
        "permisos": ["carga.add_certificado"],
        "acepta_superusuarios": True,
    },
    {
        "ubicacion": "templates/index.html:6",
        "gate": "Aviso 'su cuenta no posee permisos'",
        "grupos": ["gciaoperativa_usuarios", "dirgral_usuarios", "rrhh_usuarios"],
        "modo": "ninguno",
        "superuser_en_grupos": False,
        "permisos": [
            "carga.view_obra",
            "secretariador.view_comisionadosolicitud",
            "personalizador.add_agente",
        ],
        "acepta_superusuarios": True,
    },
    {
        "ubicacion": "api/views/carga_views.py:1264",
        "gate": "GET /certificados/",
        "grupos": ["gciaoperativa_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": False,
        # require_model_perm(Certificado) sobre GET ya exige view_certificado, y ese
        # permiso solo lo tiene gciaoperativa_usuarios -> el gate por grupo era redundante.
        "y_permisos": ["carga.view_certificado"],
        "permisos": ["carga.view_certificado"],
    },
    {
        "ubicacion": "api/views/secretariador_views.py:801",
        "gate": "GET /comisionados-solicitudes/",
        "grupos": ["dirgral_usuarios"],
        "modo": "alguno",
        "superuser_en_grupos": False,
        "y_permisos": ["secretariador.view_comisionadosolicitud"],
        "permisos": ["secretariador.view_comisionadosolicitud"],
    },
]


class Command(BaseCommand):
    help = "Compara los gates de la UI por nombre de grupo contra su equivalente por permiso."

    def add_arguments(self, parser):
        parser.add_argument("--detalle", action="store_true", help="Lista los usernames que difieren")

    def handle(self, *args, **options):
        User = get_user_model()
        activos = list(
            User.objects.filter(is_active=True).prefetch_related("groups", "user_permissions")
        )
        self.stdout.write(f"Usuarios activos evaluados: {len(activos)}\n")

        fallos = 0
        for eq in EQUIVALENCIAS:
            faltantes = [p for p in eq["permisos"] if not self._existe(p)]
            if faltantes:
                self.stdout.write(self.style.ERROR(
                    f"[ERROR ] {eq['ubicacion']:30s} {eq['gate']:35s} permiso inexistente: {faltantes}"
                ))
                fallos += 1
                continue

            por_grupo = {u.username for u in activos if self._pasa_grupos(u, eq)}
            por_permiso = {u.username for u in activos if self._pasa_permisos(u, eq)}
            ganan = por_permiso - por_grupo
            pierden = por_grupo - por_permiso
            difieren = ganan | pierden

            solo_su = difieren and all(
                u.is_superuser for u in activos if u.username in difieren
            )
            if not difieren:
                estado, estilo = "OK    ", self.style.SUCCESS
            elif solo_su and eq.get("acepta_superusuarios"):
                estado, estilo = "OK-SU ", self.style.WARNING
            else:
                estado, estilo = "DIFIERE", self.style.ERROR
                fallos += 1

            self.stdout.write(estilo(
                f"[{estado}] {eq['ubicacion']:30s} {eq['gate']:35s} "
                f"grupo={len(por_grupo):3d} permiso={len(por_permiso):3d}"
            ))
            if difieren and options["detalle"]:
                if ganan:
                    self.stdout.write(f"{'':11s}+ ganan acceso : {sorted(ganan)}")
                if pierden:
                    self.stdout.write(f"{'':11s}- pierden      : {sorted(pierden)}")

        self.stdout.write("")
        if fallos:
            self.stdout.write(self.style.ERROR(f"{fallos} gate(s) cambiaron de alcance -- NO desplegar"))
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS("Todos los gates cubren el mismo conjunto de usuarios"))

    @staticmethod
    def _existe(perm):
        app, codename = perm.split(".")
        return Permission.objects.filter(content_type__app_label=app, codename=codename).exists()

    @staticmethod
    def _pasa_grupos(user, eq):
        nombres = {g.name for g in user.groups.all()}
        en_alguno = bool(nombres & set(eq["grupos"]))
        if eq["modo"] == "ninguno":
            return not en_alguno
        if not all(user.has_perm(p) for p in eq.get("y_permisos", [])):
            return False
        return en_alguno or (eq["superuser_en_grupos"] and user.is_superuser)

    @staticmethod
    def _pasa_permisos(user, eq):
        tiene = any(user.has_perm(p) for p in eq["permisos"])
        return (not tiene) if eq["modo"] == "ninguno" else tiene
