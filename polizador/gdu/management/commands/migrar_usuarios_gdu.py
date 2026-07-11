import unicodedata

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from gdu.models import Role, Rolemapping, UsuarioMigrado, VisualizadorUser
from personalizador.models import Agente


def normalizar(texto):
    """Minúsculas y sin acentos, para comparar nombres tolerando 'Rubén' == 'Ruben'."""
    texto = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in texto if not unicodedata.combining(c)).lower()

# visualizador.role.nombre -> codename del permiso gdu equivalente (ver gdu/models/*.py Meta.permissions).
# "relevamiento-ver" usa el permiso view_relevamiento que Django ya genera automáticamente.
ROLE_TO_PERMISSION_CODENAME = {
    "barrios-ver": "ver_barrios",
    "expropiaciones-ver": "ver_expropiaciones",
    "viviendas-ver": "ver_viviendas",
    "viviendas-dispersas-ver": "ver_viviendas_dispersas",
    "plano-mensura-ver": "ver_plano_mensura",
    "catastro-urbano-ver": "ver_catastro_urbano",
    "escriturar-ver": "ver_escriturar",
    "dominio-editar": "editar_dominio",
    "editar-nro_adjudicatario": "editar_nro_adjudicatario",
    "relevamiento-ver": "view_relevamiento",
    "relevamiento-encuestar": "encuestar_relevamiento",
    "admin-user": "admin_gdu_usuarios",
}


class Command(BaseCommand):
    """
    Migra la autenticación heredada de hasura (visualizador.user/role/rolemapping)
    a settings.AUTH_USER_MODEL + Django Groups/Permissions. Idempotente (se puede
    re-correr sin duplicar nada). Las contraseñas NO se copian: los usuarios
    migrados autentican contra LDAP, no contra el hasher de Django.
    Si el username ya existe en el sistema (choca con un CustomUser real de
    polizador), se reutiliza esa cuenta en vez de crear una duplicada.
    """
    help = "Migra usuarios/roles de visualizador.* (hasura) a CustomUser + Groups/Permissions"

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        permisos_gdu = {
            p.codename: p for p in Permission.objects.filter(content_type__app_label="gdu")
        }

        grupo_por_role_id = {}
        for role in Role.objects.all():
            codename = ROLE_TO_PERMISSION_CODENAME.get(role.nombre)
            permiso = permisos_gdu.get(codename) if codename else None
            if not permiso:
                self.stderr.write(self.style.WARNING(f"Rol '{role.nombre}' sin permiso mapeado, se omite"))
                continue
            grupo, _ = Group.objects.get_or_create(name=f"GDU: {role.nombre}")
            grupo.permissions.set([permiso])
            grupo_por_role_id[role.id] = grupo

        creados = reutilizados = 0
        for vu in VisualizadorUser.objects.select_related("area"):
            usuario = User.objects.filter(username__iexact=vu.username).first()
            reutilizado = usuario is not None
            if not usuario:
                date_joined = vu.created_at or timezone.now()
                if timezone.is_naive(date_joined):
                    date_joined = timezone.make_aware(date_joined)
                usuario = User(
                    username=vu.username,
                    first_name=vu.nombre or "",
                    last_name="",
                    is_active=bool(vu.activo),
                    date_joined=date_joined,
                )
                usuario.save()

            UsuarioMigrado.objects.update_or_create(
                visualizador_user_id=vu.id,
                defaults={
                    "usuario": usuario,
                    "area_nombre": vu.area.nombre if vu.area_id else "",
                    "cuenta_reutilizada": reutilizado,
                },
            )
            reutilizados += reutilizado
            creados += not reutilizado

        asignaciones = 0
        migrados_por_vu_id = {
            m.visualizador_user_id: m.usuario for m in UsuarioMigrado.objects.select_related("usuario")
        }
        for rm in Rolemapping.objects.all():
            grupo = grupo_por_role_id.get(rm.role_id)
            usuario = migrados_por_vu_id.get(rm.user_id)
            if not grupo or not usuario:
                continue
            usuario.groups.add(grupo)
            asignaciones += 1

        self.stdout.write(self.style.SUCCESS(
            f"Usuarios: {creados} creados, {reutilizados} reutilizados (ya existían). "
            f"Grupos GDU: {len(grupo_por_role_id)}. Asignaciones usuario-grupo: {asignaciones}."
        ))

        self.reportar_match_agente()

    def reportar_match_agente(self):
        """
        Prueba exploratoria: vu.nombre trae nombre y apellido juntos en un solo campo
        y con orden de palabras variable (ej. "Juan Carlos Perez Gomez"), con máximo
        4 o 5 palabras. Probamos todos los puntos de corte posibles: primeras N
        palabras como nombre, resto como apellido, y juntamos (unión) los Agente que
        matchean en cualquiera de esos cortes, comparando sin distinguir acentos
        (vu.nombre no siempre trae tildes iguales a Agente). Cuando eso no encuentra
        nada (vu.nombre a veces solo trae el/los nombres, sin apellido), probamos con
        el username: por convención es la primera letra del nombre + el apellido
        completo pegado (ej. "rcastro" = R. + Castro). Solo informa por stdout, no
        persiste nada — sirve para evaluar qué tan bien funciona el match antes de
        decidir si conviene usarlo para vincular usuario_migrado <-> Agente.
        """
        agentes = [
            (a.id, normalizar(a.agente_nombres), normalizar(a.agente_apellidos))
            for a in Agente.objects.all()
        ]

        unicos = ambiguos = sin_match = 0
        a_revisar = []
        for vu in VisualizadorUser.objects.all():
            candidatos_ids = self._candidatos_agente_todos_los_cortes(vu.nombre, agentes)
            if not candidatos_ids:
                candidatos_ids = self._candidatos_agente_por_username(vu.username, agentes)
            cantidad = len(candidatos_ids)

            if cantidad == 1:
                unicos += 1
            elif cantidad == 0:
                sin_match += 1
                a_revisar.append(f"'{vu.nombre}' (username={vu.username}): sin candidatos")
            else:
                ambiguos += 1
                a_revisar.append(f"'{vu.nombre}' (username={vu.username}): {cantidad} candidatos")

        self.stdout.write(self.style.WARNING(
            f"Match contra Agente (exploratorio): {unicos} único, {ambiguos} ambiguos, "
            f"{sin_match} sin match."
        ))
        for item in a_revisar:
            self.stdout.write(f"  - {item}")

    def _candidatos_agente_todos_los_cortes(self, nombre_completo, agentes):
        palabras = (nombre_completo or "").split()
        if len(palabras) < 2:
            return set()
        candidatos_ids = set()
        for corte in range(1, len(palabras)):
            nombre = normalizar(" ".join(palabras[:corte]))
            apellido = normalizar(" ".join(palabras[corte:]))
            candidatos_ids.update(
                aid for aid, agente_nombre, agente_apellido in agentes
                if nombre in agente_nombre and apellido in agente_apellido
            )
        return candidatos_ids

    def _candidatos_agente_por_username(self, username, agentes):
        username = normalizar(username)
        # Exigimos un apellido de al menos 3 letras para evitar falsos positivos
        # por coincidencias cortas (ej. "gdu" -> apellido "du" pega con cualquier
        # apellido que contenga esas dos letras).
        if len(username) < 4:
            return set()
        inicial, apellido = username[0], username[1:]
        return {
            aid for aid, agente_nombre, agente_apellido in agentes
            if agente_nombre[:1] == inicial and apellido in agente_apellido.replace(" ", "")
        }
