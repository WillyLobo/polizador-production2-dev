"""
Tests de las dos vias por las que un usuario ya migrado a LDAP podia volver a
tener contrasena local, anulando el sentido de habersela retirado (la idea es
que desactivar a alguien en el AD le quite el acceso, y una contrasena local
nueva sobrevive a esa baja).

Las dos estaban abiertas y se verificaron en vivo antes de cerrarlas:
  /accounts/password/change/ -> 302 a /accounts/password/set/, y ahi
  SetPasswordForm no pide la contrasena anterior.
  /accounts/password/reset/  -> allauth mandaba el link igual, porque
  filter_users_by_email() no mira has_usable_password().
"""
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

UserModel = get_user_model()
CLAVE = "ClaveLocal123!"
NUEVA = "OtraClaveLocal123!"


class SoloLdapTest(TestCase):
    def setUp(self):
        self.migrado = UserModel.objects.create_user(
            username="migrado", email="migrado@ipduv.gov.ar", password=CLAVE, ad_username="jperez")
        self.migrado.set_unusable_password()
        self.migrado.save(update_fields=["password"])

        # Vinculado pero todavia con contrasena local: esta en transicion y no
        # hay que molestarlo.
        self.transicion = UserModel.objects.create_user(
            username="transicion", email="transicion@ipduv.gov.ar", password=CLAVE, ad_username="mgomez")

        # Ni vinculado ni migrado.
        self.local = UserModel.objects.create_user(
            username="local", email="local@ipduv.gov.ar", password=CLAVE)

    def test_solo_ldap_distingue_al_migrado(self):
        assert self.migrado.solo_ldap is True
        assert self.transicion.solo_ldap is False
        assert self.local.solo_ldap is False

    # --- set password ---

    def test_migrado_no_puede_ponerse_una_contrasena_local(self):
        self.client.force_login(self.migrado)
        resp = self.client.post(
            "/accounts/password/set/", {"password1": NUEVA, "password2": NUEVA})
        self.migrado.refresh_from_db()
        assert not self.migrado.has_usable_password(), "volvio a tener contrasena local"
        assert not self.client.login(username="migrado", password=NUEVA)
        assert resp.status_code == 200

    def test_al_migrado_se_le_explica_en_vez_de_darle_un_formulario(self):
        self.client.force_login(self.migrado)
        resp = self.client.get("/accounts/password/set/")
        self.assertContains(resp, "contraseña de red")
        self.assertNotContains(resp, 'name="password1"')

    def test_cambiar_contrasena_lleva_a_la_explicacion(self):
        # allauth redirige change -> set; la sombra tiene que atajarlo ahi.
        self.client.force_login(self.migrado)
        resp = self.client.get("/accounts/password/change/", follow=True)
        self.assertContains(resp, "contraseña de red")

    def test_el_que_conserva_contrasena_local_no_se_ve_afectado(self):
        self.client.force_login(self.transicion)
        resp = self.client.get("/accounts/password/set/", follow=True)
        # allauth manda set -> change cuando la contrasena existe: sigue su curso.
        assert resp.status_code == 200
        self.assertNotContains(resp, "Tu contraseña es la de red del IPDUV")

    def test_el_que_conserva_contrasena_local_puede_cambiarla(self):
        self.client.force_login(self.transicion)
        self.client.post("/accounts/password/change/", {
            "oldpassword": CLAVE, "password1": NUEVA, "password2": NUEVA})
        self.client.logout()
        assert self.client.login(username="transicion", password=NUEVA)

    # --- reset por mail ---

    def test_al_migrado_no_se_le_manda_un_link_de_reset(self):
        mail.outbox = []
        self.client.post("/accounts/password/reset/", {"email": "migrado@ipduv.gov.ar"})
        assert len(mail.outbox) == 1, "se contesta igual, para no revelar que cuentas existen"
        cuerpo = mail.outbox[0].body
        assert "/accounts/password/reset/key/" not in cuerpo, "le llego un link para ponerse contrasena local"
        assert "red del IPDUV" in cuerpo

    def test_al_que_conserva_contrasena_local_le_llega_el_link_de_siempre(self):
        mail.outbox = []
        self.client.post("/accounts/password/reset/", {"email": "local@ipduv.gov.ar"})
        assert len(mail.outbox) == 1
        assert "/accounts/password/reset/key/" in mail.outbox[0].body
