"""
Tests del cableado de LDAP en main (settings) y del registro de por que backend
entro cada usuario (core/signals.py).

No se simula una autenticacion LDAP completa: eso depende del AD real y ya se
verifica en vivo. Lo que se fija aca son las dos cosas que romperian en
silencio si alguien toca la configuracion.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import LoginEvent

UserModel = get_user_model()


class ConfiguracionLDAPTest(TestCase):
    def test_modelbackend_va_primero(self):
        """Si LDAP quedara antes que el backend local, un usuario sin vincular
        (o con el AD caido) podria no poder entrar con su contrasena de
        polizador. El orden es la garantia de que nadie pierde acceso."""
        backends = settings.AUTHENTICATION_BACKENDS
        assert backends[0] == "django.contrib.auth.backends.ModelBackend"
        ldap_backend = getattr(settings, "LDAP_BACKEND", "core.ldap_backend.PolizadorLDAPBackend")
        if ldap_backend in backends:
            assert backends.index(ldap_backend) > 0

    def test_user_query_field_esta_en_el_attr_map(self):
        """django-auth-ldap resuelve USER_QUERY_FIELD contra USER_ATTR_MAP
        (query_value = ldap_user.attrs[USER_ATTR_MAP[query_field]][0]). Si el
        campo no esta en el mapa, cada login por LDAP revienta con KeyError."""
        if not getattr(settings, "LDAP_CONFIGURADO", False):
            self.skipTest("LDAP no configurado en este entorno")
        campo = settings.AUTH_LDAP_USER_QUERY_FIELD
        assert campo == "ad_username"
        assert campo in settings.AUTH_LDAP_USER_ATTR_MAP
        assert settings.AUTH_LDAP_USER_ATTR_MAP[campo] == "sAMAccountName"

    def test_el_alta_automatica_usa_el_backend_propio(self):
        """La politica es que cualquiera con cuenta en el AD pueda entrar (sin
        permisos). Eso exige las dos cosas juntas: permitir el alta Y que la
        haga PolizadorLDAPBackend. Con el backend de fabrica, NO_NEW_USERS=False
        guarda al usuario nuevo con username vacio -- el segundo revienta contra
        la restriccion unica -- y duplica las cuentas de quienes ya existen en
        polizador con ese mismo username. Ver core/ldap_backend.py."""
        if not getattr(settings, "LDAP_CONFIGURADO", False):
            self.skipTest("LDAP no configurado en este entorno")
        assert settings.AUTH_LDAP_NO_NEW_USERS is False
        assert settings.LDAP_BACKEND == "core.ldap_backend.PolizadorLDAPBackend"
        assert "django_auth_ldap.backend.LDAPBackend" not in settings.AUTHENTICATION_BACKENDS

    def test_no_se_pisan_los_nombres_con_los_del_ad(self):
        """Mapear first_name/last_name haria que el primer login por LDAP
        reemplace nombres curados en polizador por la ortografia del AD."""
        if not getattr(settings, "LDAP_CONFIGURADO", False):
            self.skipTest("LDAP no configurado en este entorno")
        mapa = settings.AUTH_LDAP_USER_ATTR_MAP
        assert "first_name" not in mapa
        assert "last_name" not in mapa


class RegistroDeBackendTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="pepe", password="claveLocal123!")

    def test_login_local_queda_registrado_con_su_backend(self):
        self.client.login(username="pepe", password="claveLocal123!")
        evento = LoginEvent.objects.get(user=self.user)
        assert evento.backend.endswith("ModelBackend"), evento.backend
        assert evento.por_ldap is False

    def test_por_ldap_detecta_el_backend_de_django_auth_ldap(self):
        evento = LoginEvent.objects.create(
            user=self.user, backend="django_auth_ldap.backend.LDAPBackend"
        )
        assert evento.por_ldap is True

    def test_filtro_que_usa_el_reporte_de_avance(self):
        LoginEvent.objects.create(user=self.user, backend="django_auth_ldap.backend.LDAPBackend")
        LoginEvent.objects.create(user=self.user, backend="django.contrib.auth.backends.ModelBackend")
        listos = (
            LoginEvent.objects.filter(backend__endswith="LDAPBackend")
            .values_list("user_id", flat=True).distinct()
        )
        assert list(listos) == [self.user.id]
