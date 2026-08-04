from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from ninja.testing import TestClient

from api.router import api

UserModel = get_user_model()


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def test_anonymous_redirected_to_login(self):
        resp = self.client.get("/administracion/dashboard/")
        assert resp.status_code == 302

    def test_regular_user_forbidden(self):
        self.client.login(username="plain_user", password="pass1234!")
        resp = self.client.get("/administracion/dashboard/")
        assert resp.status_code == 403

    def test_superuser_allowed(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/dashboard/")
        assert resp.status_code == 200


class DashboardApiTest(TestCase):
    def setUp(self):
        self.anon_client = TestClient(api)
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def test_requires_auth(self):
        resp = self.anon_client.get("dashboard/sentry/")
        assert resp.status_code == 401

    def test_regular_user_forbidden(self):
        self.client.login(username="plain_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/sentry/")
        assert resp.status_code == 403

    def test_superuser_allowed(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/sentry/")
        assert resp.status_code == 200

    def test_throughput_unknown_app_label(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/throughput/not-an-app/")
        assert resp.status_code == 404

    def test_throughput_known_app_label(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/throughput/carga/")
        assert resp.status_code == 200
        assert "series" in resp.json()

    @override_settings(SENTRY_AUTH_TOKEN=None, SENTRY_ORG=None, SENTRY_PROJECT=None)
    def test_sentry_not_configured(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/v1/api/dashboard/sentry/")
        assert resp.status_code == 200
        assert resp.json()["configured"] is False
