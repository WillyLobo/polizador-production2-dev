"""
Tests de la vinculacion de la cuenta de polizador con la cuenta de red
(core/views_vincular_ad.py y core/middleware_vincular_ad.py).

El AD real no se toca: se mockea core.ldap_ad.verificar_credenciales, que es el
unico punto por donde la vista habla con el directorio.
"""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from core.ldap_ad import ADNoDisponible

UserModel = get_user_model()

ENTRADA_AD = {
    "sAMAccountName": "globo",
    "displayName": "Guillermo Lobo Cechini",
    "mail": "globo@ipduv.gov.ar",
    "dn": "CN=Guillermo Lobo,OU=Usuarios,DC=ipduv,DC=gov,DC=ar",
}


class VincularADViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="willylobo", password="claveLocal123!",
            first_name="Guillermo Eduardo", last_name="Lobo Cecchini",
        )
        self.client.login(username="willylobo", password="claveLocal123!")
        self.url = reverse("vincular_ad")

    def test_requiere_estar_logueado(self):
        self.client.logout()
        resp = self.client.get(self.url)
        assert resp.status_code == 302
        assert "/accounts/login/" in resp["Location"]

    def test_prefill_con_el_username_actual(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 200
        assert resp.context["form"].initial["ad_username"] == "willylobo"

    @patch("core.ldap_ad.verificar_credenciales", return_value=ENTRADA_AD)
    def test_credenciales_validas_guardan_el_sam_que_devolvio_el_ad(self, mock_ver):
        # El usuario tipea "GLOBO"; se guarda lo que dice el AD, no lo tipeado.
        resp = self.client.post(self.url, {"ad_username": "GLOBO", "ad_password": "claveDeRed"})
        assert resp.status_code == 302
        self.user.refresh_from_db()
        assert self.user.ad_username == "globo"
        assert self.user.ad_vinculado_en is not None
        assert self.user.ad_sin_cuenta_red is False

    @patch("core.ldap_ad.verificar_credenciales", return_value=None)
    def test_credenciales_invalidas_no_vinculan(self, mock_ver):
        resp = self.client.post(self.url, {"ad_username": "globo", "ad_password": "mala"})
        assert resp.status_code == 200
        self.user.refresh_from_db()
        assert self.user.ad_username is None
        self.assertContains(resp, "incorrectos")

    @patch("core.ldap_ad.verificar_credenciales", side_effect=ADNoDisponible("timeout"))
    def test_ad_caido_no_se_confunde_con_contrasena_mala(self, mock_ver):
        resp = self.client.post(self.url, {"ad_username": "globo", "ad_password": "loQueSea"})
        assert resp.status_code == 200
        self.assertContains(resp, "No se pudo contactar")
        self.assertNotContains(resp, "incorrectos")

    @patch("core.ldap_ad.verificar_credenciales", return_value=ENTRADA_AD)
    def test_una_cuenta_de_red_no_se_vincula_a_dos_usuarios(self, mock_ver):
        UserModel.objects.create_user(username="otro", password="x", ad_username="globo")
        resp = self.client.post(self.url, {"ad_username": "globo", "ad_password": "claveDeRed"})
        assert resp.status_code == 200
        self.user.refresh_from_db()
        assert self.user.ad_username is None
        self.assertContains(resp, "ya está vinculada")

    @patch("core.ldap_ad.verificar_credenciales", return_value=ENTRADA_AD)
    def test_ya_vinculado_no_vuelve_a_pedirlo(self, mock_ver):
        self.user.ad_username = "globo"
        self.user.save(update_fields=["ad_username"])
        resp = self.client.get(self.url)
        assert resp.status_code == 302

    def test_declarar_que_no_tiene_cuenta_de_red(self):
        resp = self.client.post(reverse("vincular_ad_sin_cuenta"))
        assert resp.status_code == 302
        self.user.refresh_from_db()
        assert self.user.ad_sin_cuenta_red is True
        assert self.user.ad_username is None

    def test_varios_usuarios_pueden_quedar_sin_vincular(self):
        # ad_username es unique: con null (no "") esto tiene que poder repetirse.
        UserModel.objects.create_user(username="a", password="x")
        UserModel.objects.create_user(username="b", password="x")
        assert UserModel.objects.filter(ad_username__isnull=True).count() == 3


@override_settings(AD_VINCULACION_OBLIGATORIA=True)
class VincularADMiddlewareTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="pepe", password="claveLocal123!")
        self.client.login(username="pepe", password="claveLocal123!")

    def test_redirige_la_navegacion_normal(self):
        resp = self.client.get("/home/")
        assert resp.status_code == 302
        assert resp["Location"] == reverse("vincular_ad")

    def test_no_redirige_si_ya_esta_vinculado(self):
        self.user.ad_username = "pperez"
        self.user.save(update_fields=["ad_username"])
        resp = self.client.get("/home/")
        assert resp.status_code != 302 or resp["Location"] != reverse("vincular_ad")

    def test_no_redirige_si_declaro_no_tener_cuenta(self):
        self.user.ad_sin_cuenta_red = True
        self.user.save(update_fields=["ad_sin_cuenta_red"])
        resp = self.client.get("/home/")
        assert resp.status_code != 302 or resp["Location"] != reverse("vincular_ad")

    def test_no_redirige_la_api(self):
        # Un redirect sobre JSON no lo ve nadie y rompe en silencio.
        resp = self.client.get("/v1/api/certificados/")
        assert resp.status_code != 302

    def test_no_redirige_ajax(self):
        resp = self.client.get("/home/", headers={"x-requested-with": "XMLHttpRequest"})
        assert resp.status_code != 302 or resp["Location"] != reverse("vincular_ad")

    def test_no_redirige_el_logout(self):
        resp = self.client.get("/accounts/logout/")
        assert resp.status_code != 302 or resp["Location"] != reverse("vincular_ad")

    def test_no_redirige_la_propia_pagina_de_vinculacion(self):
        resp = self.client.get(reverse("vincular_ad"))
        assert resp.status_code == 200

    @override_settings(AD_VINCULACION_OBLIGATORIA=False)
    def test_apagado_no_molesta_a_nadie(self):
        resp = self.client.get("/home/")
        assert resp.status_code != 302 or resp["Location"] != reverse("vincular_ad")
