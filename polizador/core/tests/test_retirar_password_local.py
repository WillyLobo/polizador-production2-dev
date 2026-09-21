"""
Tests de core/management/commands/retirar_password_local.py.

La operacion es irreversible (set_unusable_password pisa el hash), asi que lo
que mas importa probar es a quien NO toca.
"""
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from core.models import LoginEvent

UserModel = get_user_model()
LDAP = "django_auth_ldap.backend.LDAPBackend"
LOCAL = "django.contrib.auth.backends.ModelBackend"


def _correr(**kwargs):
    salida = StringIO()
    call_command("retirar_password_local", stdout=salida, **kwargs)
    return salida.getvalue()


class RetirarPasswordLocalTest(TestCase):
    def setUp(self):
        # Listo: vinculado y visto entrando por LDAP.
        self.listo = UserModel.objects.create_user(
            username="listo", password="clave123!", ad_username="jperez")
        LoginEvent.objects.create(user=self.listo, backend=LDAP)

        # Vinculado pero nunca entro por LDAP.
        self.sin_probar = UserModel.objects.create_user(
            username="sin_probar", password="clave123!", ad_username="mgomez")
        LoginEvent.objects.create(user=self.sin_probar, backend=LOCAL)

        # Ni siquiera vinculo.
        self.sin_vincular = UserModel.objects.create_user(username="sin_vincular", password="clave123!")

    def test_dry_run_no_modifica_nada(self):
        salida = _correr()
        self.listo.refresh_from_db()
        assert self.listo.has_usable_password()
        assert "DRY-RUN" in salida

    def test_aplicar_solo_afecta_al_que_ya_entro_por_ldap(self):
        _correr(aplicar=True)
        self.listo.refresh_from_db()
        self.sin_probar.refresh_from_db()
        self.sin_vincular.refresh_from_db()
        assert not self.listo.has_usable_password()
        assert self.sin_probar.has_usable_password(), "no se lo vio entrar por LDAP: no se toca"
        assert self.sin_vincular.has_usable_password(), "sin vincular: no se toca"

    def test_vinculado_pero_sin_login_ldap_se_explica(self):
        salida = _correr()
        assert "todavia no se lo vio entrar por LDAP" in salida

    def test_superusuario_se_saltea_por_defecto(self):
        jefe = UserModel.objects.create_superuser(
            username="jefe", password="clave123!", ad_username="jjefe")
        LoginEvent.objects.create(user=jefe, backend=LDAP)
        _correr(aplicar=True)
        jefe.refresh_from_db()
        assert jefe.has_usable_password(), "el acceso de emergencia no se retira sin pedirlo"

    def test_superusuario_se_incluye_si_se_pide(self):
        jefe = UserModel.objects.create_superuser(
            username="jefe", password="clave123!", ad_username="jjefe")
        LoginEvent.objects.create(user=jefe, backend=LDAP)
        _correr(aplicar=True, incluir_superusuarios=True)
        jefe.refresh_from_db()
        assert not jefe.has_usable_password()

    def test_filtrar_por_usuario(self):
        otro = UserModel.objects.create_user(
            username="otro", password="clave123!", ad_username="ootro")
        LoginEvent.objects.create(user=otro, backend=LDAP)
        _correr(aplicar=True, usuario="listo")
        self.listo.refresh_from_db()
        otro.refresh_from_db()
        assert not self.listo.has_usable_password()
        assert otro.has_usable_password(), "solo se pidio 'listo'"

    def test_es_idempotente(self):
        _correr(aplicar=True)
        salida = _correr(aplicar=True)
        assert "ya no tiene contrasena local" in salida

    def test_retirar_la_contrasena_invalida_las_sesiones(self):
        # get_session_auth_hash() es un HMAC del password: al cambiarlo, la
        # cookie de sesion deja de validar y el usuario tiene que volver a entrar.
        antes = self.listo.get_session_auth_hash()
        _correr(aplicar=True)
        self.listo.refresh_from_db()
        assert self.listo.get_session_auth_hash() != antes

    def test_el_usuario_no_puede_entrar_con_la_clave_vieja(self):
        _correr(aplicar=True)
        assert not self.client.login(username="listo", password="clave123!")
