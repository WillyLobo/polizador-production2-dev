import csv
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

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv-sin-match",
            default="sin_match_agente.csv",
            help="Ruta del CSV donde se listan los usuarios sin candidatos a Agente (default: sin_match_agente.csv)",
        )
        parser.add_argument(
            "--csv-correcciones",
            default=None,
            help=(
                "Ruta a un CSV previamente generado por --csv-sin-match con la columna "
                "'agente_id_manual' completada a mano. Las filas con ese campo lleno se "
                "toman como match único, en vez de volver a intentar el matching automático."
            ),
        )
        parser.add_argument(
            "--completar-match-agente",
            action="store_true",
            help=(
                "Además de reportar, persiste el vínculo Agente.agente_usuario para los "
                "usuarios con match único (automático o tomado de --csv-correcciones), "
                "completando la prueba exploratoria de matching."
            ),
        )

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

        self.reportar_match_agente(
            options["csv_sin_match"], options["csv_correcciones"], options["completar_match_agente"],
        )

    def reportar_match_agente(self, csv_sin_match, csv_correcciones=None, completar=False):
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
        ids_agente_validos = {aid for aid, _, _ in agentes}
        correcciones = self._leer_csv_correcciones(csv_correcciones, ids_agente_validos) if csv_correcciones else {}
        migrados_por_vu_id = {
            m.visualizador_user_id: m.usuario for m in UsuarioMigrado.objects.select_related("usuario")
        }

        unicos = ambiguos = sin_match = corregidos = vinculados = 0
        a_revisar = []
        a_revisar_csv = []
        for vu in VisualizadorUser.objects.select_related("area"):
            if vu.id in correcciones:
                candidatos_ids = {correcciones[vu.id]}
                corregidos += 1
            else:
                candidatos_ids = self._candidatos_agente_todos_los_cortes(vu.nombre, agentes)
                if not candidatos_ids:
                    candidatos_ids = self._candidatos_agente_por_username(vu.username, agentes)
            cantidad = len(candidatos_ids)

            if cantidad == 1:
                unicos += 1
                if completar:
                    agente_id = next(iter(candidatos_ids))
                    vinculados += self._vincular_agente(vu, agente_id, migrados_por_vu_id.get(vu.id))
            elif cantidad == 0:
                sin_match += 1
                a_revisar.append(f"'{vu.nombre}' (username={vu.username}): sin candidatos")
                a_revisar_csv.append((vu, candidatos_ids))
            else:
                ambiguos += 1
                a_revisar.append(f"'{vu.nombre}' (username={vu.username}): {cantidad} candidatos")
                a_revisar_csv.append((vu, candidatos_ids))

        self.stdout.write(self.style.WARNING(
            f"Match contra Agente (exploratorio): {unicos} único, {ambiguos} ambiguos, "
            f"{sin_match} sin match ({corregidos} tomados de {csv_correcciones})."
        ))
        for item in a_revisar:
            self.stdout.write(f"  - {item}")

        if completar:
            self.stdout.write(self.style.SUCCESS(
                f"Agente.agente_usuario vinculado para {vinculados} de {unicos} matches únicos."
            ))

        self._escribir_csv_sin_match(csv_sin_match, a_revisar_csv)
        self.stdout.write(self.style.SUCCESS(
            f"CSV de usuarios sin match o ambiguos escrito en '{csv_sin_match}' ({len(a_revisar_csv)} filas)."
        ))

    def _vincular_agente(self, vu, agente_id, usuario):
        """
        Persiste Agente.agente_usuario para un match único. No pisa un vínculo
        existente hacia otro usuario (podría ser un dato cargado a mano en
        personalizador que no tenga que ver con esta migración).
        """
        if usuario is None:
            self.stderr.write(self.style.WARNING(
                f"'{vu.username}': no tiene UsuarioMigrado, se omite (correr sin --csv-correcciones "
                "primero para migrar usuarios)."
            ))
            return 0

        agente = Agente.objects.get(id=agente_id)
        if agente.agente_usuario_id == usuario.id:
            return 0
        if agente.agente_usuario_id:
            self.stderr.write(self.style.WARNING(
                f"Agente #{agente_id} ya está vinculado a otro usuario "
                f"({agente.agente_usuario}), se omite '{vu.username}'."
            ))
            return 0

        agente.agente_usuario = usuario
        agente.save(update_fields=["agente_usuario"])
        return 1

    def _leer_csv_correcciones(self, ruta, ids_agente_validos):
        """
        Lee un CSV con el formato generado por _escribir_csv_sin_match (columnas
        visualizador_user_id, username, nombre, area, agente_id_manual) y devuelve
        {visualizador_user_id: agente_id} sólo para las filas donde se completó
        agente_id_manual con un id de Agente que existe.
        """
        correcciones = {}
        with open(ruta, newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                valor = (fila.get("agente_id_manual") or "").strip()
                if not valor:
                    continue
                vu_id = int(fila["visualizador_user_id"])
                agente_id = int(valor)
                if agente_id not in ids_agente_validos:
                    self.stderr.write(self.style.WARNING(
                        f"'{ruta}': visualizador_user_id={vu_id} referencia agente_id={agente_id} "
                        "que no existe, se ignora."
                    ))
                    continue
                correcciones[vu_id] = agente_id
        return correcciones

    def _escribir_csv_sin_match(self, ruta, filas):
        """
        `filas` es una lista de (VisualizadorUser, candidatos_ids) — tanto los que
        quedaron sin ningún candidato como los ambiguos (más de uno), para poder
        revisar y completar 'agente_id_manual' a mano en ambos casos.
        """
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "visualizador_user_id", "username", "nombre", "area",
                "candidatos_ids", "agente_id_manual",
            ])
            for vu, candidatos_ids in filas:
                writer.writerow([
                    vu.id,
                    vu.username,
                    vu.nombre or "",
                    vu.area.nombre if vu.area_id else "",
                    ",".join(str(aid) for aid in sorted(candidatos_ids)),
                    "",
                ])

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
