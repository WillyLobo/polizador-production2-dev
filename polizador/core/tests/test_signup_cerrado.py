"""
Tests del cierre del alta de cuentas por la web (core/adapters.py).

Lo importante es la asimetria: /accounts/signup/ deja de crear usuarios, pero
todo lo que hacen los usuarios que YA existen -- entrar con usuario y contrasena
-- tiene que seguir funcionando igual. Un cierre que ademas rompa el login seria
una caida total del sistema.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class SignupCerradoTest(TestCase):
    def test_get_signup_muestra_la_pagina_de_cierre_y_no_el_formulario(self):
        resp = self.client.get("/accounts/signup/")
        assert resp.status_code == 200, resp.status_code
        self.assertContains(resp, "Alta de cuentas cerrada")
        self.assertNotContains(resp, 'name="password1"')

    def test_post_signup_no_crea_usuario(self):
        antes = UserModel.objects.count()
        self.client.post(
            "/accounts/signup/",
            {
                "username": "intruso",
                "email": "intruso@example.com",
                "password1": "unaClaveLarga123!",
                "password2": "unaClaveLarga123!",
            },
        )
        assert UserModel.objects.count() == antes
        assert not UserModel.objects.filter(username="intruso").exists()

    def test_login_de_usuario_existente_sigue_funcionando(self):
        UserModel.objects.create_user(username="ya_existe", password="unaClaveLarga123!")
        ok = self.client.login(username="ya_existe", password="unaClaveLarga123!")
        assert ok, "el usuario existente no pudo entrar"

    def test_login_por_formulario_sigue_funcionando(self):
        UserModel.objects.create_user(username="por_form", password="unaClaveLarga123!")
        resp = self.client.post(
            "/accounts/login/",
            {"login": "por_form", "password": "unaClaveLarga123!"},
            follow=True,
        )
        assert resp.context["user"].is_authenticated, "el login por formulario dejo de andar"

    def test_admin_puede_dar_de_alta_usuarios(self):
        # La via de alta que reemplaza al signup: el panel de Django.
        UserModel.objects.create_superuser(username="jefe", password="unaClaveLarga123!")
        self.client.login(username="jefe", password="unaClaveLarga123!")
        resp = self.client.get("/admin/personalizador/customuser/add/")
        assert resp.status_code == 200, resp.status_code

    def test_navbar_de_allauth_no_ofrece_boton_de_alta(self):
        resp = self.client.get("/accounts/login/")
        self.assertNotContains(resp, "/accounts/signup/")
