"""
Tests de core/ldap_backend.PolizadorLDAPBackend: el alta automatica de quien
tiene cuenta en el AD del IPDUV y todavia no la tiene en polizador.

No se habla con el AD: se le pasa al backend un `ldap_user` falso con los
atributos que devolveria el directorio, que es lo unico que get_or_build_user
mira.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from core.ldap_backend import PolizadorLDAPBackend

UserModel = get_user_model()


class FakeLDAPUser:
    def __init__(self, sam, nombre="", apellido="", mail="", display=""):
        self.attrs = {
            "sAMAccountName": [sam],
            "givenName": [nombre],
            "sn": [apellido],
            "mail": [mail],
            "displayName": [display],
        }


class AltaAutomaticaTest(TestCase):
    def setUp(self):
        self.backend = PolizadorLDAPBackend()

    def test_usuario_nuevo_se_crea_con_los_datos_del_ad(self):
        user, built = self.backend.get_or_build_user(
            "jperez", FakeLDAPUser("jperez", "Juan", "Perez", "jperez@ipduv.gov.ar"))
        assert built is True
        assert user.username == "jperez"
        assert user.ad_username == "jperez"
        assert user.first_name == "Juan"
        assert user.last_name == "Perez"
        assert user.email == "jperez@ipduv.gov.ar"

    def test_usuario_nuevo_no_tiene_ningun_permiso(self):
        user, _ = self.backend.get_or_build_user("jperez", FakeLDAPUser("jperez"))
        user.set_unusable_password()
        user.save()
        assert user.groups.count() == 0
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.get_all_permissions() == set()
        assert user.is_active is True, "tiene que poder entrar, aunque no vea nada"

    def test_el_username_nunca_queda_vacio(self):
        """Sin esto el primero se guardaria con username="" y el segundo
        reventaria contra la restriccion unica."""
        u1, _ = self.backend.get_or_build_user("aaa", FakeLDAPUser("aaa"))
        u1.set_unusable_password(); u1.save()
        u2, _ = self.backend.get_or_build_user("bbb", FakeLDAPUser("bbb"))
        u2.set_unusable_password(); u2.save()
        assert u1.username == "aaa" and u2.username == "bbb"
        assert UserModel.objects.filter(username="").count() == 0

    def test_se_adopta_la_cuenta_existente_con_el_mismo_username(self):
        """Los 16 usuarios cuyo username ya coincide con su cuenta de red y que
        todavia no vincularon: tienen que quedarse con SU cuenta, no recibir una
        nueva y vacia al lado."""
        vieja = UserModel.objects.create_user(username="aaguilar", password="x")
        grupo = Group.objects.create(name="un_grupo")
        vieja.groups.add(grupo)

        user, built = self.backend.get_or_build_user("aaguilar", FakeLDAPUser("aaguilar"))
        assert built is False, "no es un alta: es la misma persona"
        assert user.pk == vieja.pk
        assert user.ad_username == "aaguilar"
        assert user.groups.count() == 1, "conserva sus grupos"
        assert UserModel.objects.filter(username__iexact="aaguilar").count() == 1

    def test_la_adopcion_ignora_mayusculas(self):
        """En el padron real hay 'Msbardella' contra 'msbardella' en el AD."""
        vieja = UserModel.objects.create_user(username="Msbardella", password="x")
        user, built = self.backend.get_or_build_user("msbardella", FakeLDAPUser("msbardella"))
        assert built is False
        assert user.pk == vieja.pk
        assert user.username == "Msbardella", "no se le cambia el username"
        assert user.ad_username == "msbardella"

    def test_el_sam_del_ad_gana_sobre_lo_que_se_tipeo(self):
        user, _ = self.backend.get_or_build_user("JPEREZ", FakeLDAPUser("jperez"))
        assert user.username == "jperez"
        assert user.ad_username == "jperez"

    def test_no_pisa_a_quien_ya_estaba_vinculado(self):
        vieja = UserModel.objects.create_user(
            username="willylobo", password="x", first_name="Guillermo Eduardo",
            last_name="Lobo Cecchini", ad_username="globo")
        user, built = self.backend.get_or_build_user("globo", FakeLDAPUser("globo", "Guillermo", "Lobo"))
        assert built is False
        assert user.pk == vieja.pk
        assert user.first_name == "Guillermo Eduardo", "los nombres curados no se tocan"
