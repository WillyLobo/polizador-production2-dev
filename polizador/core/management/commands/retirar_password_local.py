"""
Le retira la contrasena local a los usuarios que ya demostraron poder entrar por
LDAP, para que de ahi en mas la unica via sea la cuenta de red del IPDUV.

El criterio no es "tiene ad_username cargado" sino "se lo VIO entrar por LDAP al
menos una vez" (LoginEvent.backend termina en LDAPBackend). Tener el vinculo
cargado prueba que las credenciales de red existen; haber entrado prueba que la
cadena entera funciona para esa persona -- el backend, el USER_QUERY_FIELD, sus
permisos. Recien ahi se puede sacar la puerta vieja sin arriesgar un lockout.

IRREVERSIBLE por usuario: set_unusable_password() pisa el hash y el anterior no
se puede recuperar. Si alguien queda afuera (el AD se cae, la cuenta de red se
desactiva), la salida es que un administrador le ponga una contrasena nueva
desde /admin/personalizador/customuser/. Por eso, a diferencia del resto de los
comandos del repo, este NO hace nada salvo que se le pase --aplicar.

Tambien cierra las sesiones abiertas de ese usuario: get_session_auth_hash() es
un HMAC del campo password, asi que al cambiarlo las cookies de sesion dejan de
validar. Van a tener que volver a entrar, ahora con sus credenciales del IPDUV.

    python manage.py retirar_password_local                      # dry-run
    python manage.py retirar_password_local --aplicar
    python manage.py retirar_password_local --usuario globo --aplicar
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import LoginEvent


class Command(BaseCommand):
    help = "Retira la contrasena local de los usuarios que ya entraron por LDAP (dry-run por defecto)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--aplicar", action="store_true",
            help="Ejecuta los cambios. Sin esto solo informa que haria.",
        )
        parser.add_argument(
            "--usuario", default=None,
            help="Limita la operacion a un username de polizador (para ir de a uno).",
        )
        parser.add_argument(
            "--incluir-superusuarios", action="store_true",
            help=(
                "Incluye superusuarios, que por defecto se saltean: conviene dejar al menos "
                "una cuenta con contrasena local como acceso de emergencia si el AD falla."
            ),
        )

    def handle(self, *args, **options):
        aplicar = options["aplicar"]
        User = get_user_model()

        qs = User.objects.filter(is_active=True)
        if options["usuario"]:
            qs = qs.filter(username=options["usuario"])
            if not qs.exists():
                self.stdout.write(self.style.ERROR(f"No hay un usuario activo '{options['usuario']}'"))
                return

        vistos_por_ldap = set(
            LoginEvent.objects.filter(backend__endswith="LDAPBackend")
            .values_list("user_id", flat=True).distinct()
        )

        a_retirar, salteados = [], []
        for u in qs.order_by("username"):
            motivo = self._motivo_para_saltear(u, vistos_por_ldap, options["incluir_superusuarios"])
            (salteados if motivo else a_retirar).append((u, motivo))

        for u, motivo in salteados:
            self.stdout.write(f"  [-] {u.username:28s} {motivo}")
        for u, _ in a_retirar:
            self.stdout.write(self.style.WARNING(
                f"  [x] {u.username:28s} entra por LDAP como '{u.ad_username}' -- se le retira la contrasena local"
            ))

        self.stdout.write("")
        if not a_retirar:
            self.stdout.write("No hay usuarios en condiciones. Nadie fue modificado.")
            return

        if not aplicar:
            self.stdout.write(self.style.WARNING(
                f"DRY-RUN: {len(a_retirar)} usuario(s) quedarian solo con LDAP. "
                "Volve a correrlo con --aplicar para hacerlo."
            ))
            return

        with transaction.atomic():
            for u, _ in a_retirar:
                u.set_unusable_password()
                u.save(update_fields=["password"])
        self.stdout.write(self.style.SUCCESS(
            f"{len(a_retirar)} usuario(s) quedaron solo con LDAP. Sus sesiones abiertas dejaron de valer: "
            "la proxima vez entran con sus credenciales del IPDUV."
        ))

    @staticmethod
    def _motivo_para_saltear(u, vistos_por_ldap, incluir_superusuarios):
        if u.is_superuser and not incluir_superusuarios:
            return "superusuario (se saltea salvo --incluir-superusuarios)"
        if not u.has_usable_password():
            return "ya no tiene contrasena local"
        if not u.ad_username:
            return "todavia no vinculo su cuenta de red"
        if u.id not in vistos_por_ldap:
            return f"vinculado a '{u.ad_username}' pero todavia no se lo vio entrar por LDAP"
        return None
