import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.middleware.csrf import get_token
from django.test import RequestFactory, TestCase, Client
from ninja.testing import TestClient
from api.router import api

UserModel = get_user_model()


class HealthCheckTest(TestCase):
    def setUp(self):
        self.client = TestClient(api)

    def test_health_check(self):
        resp = self.client.get("__version__")
        assert resp.status_code == 200
        data = resp.json()
        assert "version" in data and data["version"] == "1.0.0"


class AuthTest(TestCase):
    """Test that unauthenticated requests to protected endpoints return 401."""

    def setUp(self):
        self.client = TestClient(api)

    def test_receptors_requires_auth(self):
        resp = self.client.get("receptores/")
        assert resp.status_code == 401

    def test_aseguradoras_requires_auth(self):
        resp = self.client.get("aseguradoras/")
        assert resp.status_code == 401

    def test_users_requires_auth(self):
        resp = self.client.get("users/")
        assert resp.status_code == 401


class LoadDataMixin:
    """Shared mixin to pre-load reference data for tests."""

    def setUp(self):
        super().setUp()
        from carga.models import (
            Aseguradora, Empresa, Obra, Programa, Region,
            CertificadoRubro, CertificadoFinanciamiento,
        )
        from personalizador.models import CargoTipo, Directorio, Gerencia, Direccion

        self.aseguradora = Aseguradora.objects.create(aseguradora_nombre="Aseguradora Test")
        self.programa = Programa.objects.create(programa_nombre="Programa Test")
        self.region = Region.objects.create(region_numero="1")
        self.empresas = Empresa.objects.create(empresa_nombre="Empresa Test", empresa_cuit="12345678901")
        self.rubro = CertificadoRubro.objects.create(certificadorubro_nombre="Vivienda", certificadorubro_nombre_corto="V")
        self.finan = CertificadoFinanciamiento.objects.create(
            certificadofinanciamiento_nombre="Nación",
            certificadofinanciamiento_nombre_corto="N"
        )

        CargoTipo.objects.get_or_create(cargotipo="Arquitecto")
        directorio, _ = Directorio.objects.get_or_create(directorio_nombre="Presidencia", directorio_cuof="D001")
        Gerencia.objects.get_or_create(
            gerencia_nombre="Gerencia Test", gerencia_cuof="G001", gerencia_directorio=directorio,
        )


class ObraAPITest(LoadDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient(api)

    def test_list_obras_empty(self):
        resp = self.client.get("obras/")
        assert resp.status_code == 401

    def test_create_obra_fails_unauth(self):
        resp = self.client.post(
            "obras/",
            json={
                "obra_nombre": "Nueva Obra Test",
                "empresa_id": self.empresas.id,
                "programa_id": self.programa.id,
                "expediente": "EXP-2026-001",
            },
        )
        # Auth failure or validation error expected (not 201)
        assert resp.status_code != 201


class ModeloAPITest(LoadDataMixin, TestCase):
    """Test CRUD for several models."""

    def setUp(self):
        super().setUp()
        self.client = TestClient(api)

    def test_list_aseguradoras_empty(self):
        resp = self.client.get("aseguradoras/")
        assert resp.status_code == 401


class SchemaTest(TestCase):
    """Test that schemas import correctly."""

    def test_carga_schemas_import(self):
        from api.schemas.carga_schemas import (
            AseguradoraOut, EmpresaOut, ObraOut, CertificadoOut,
        )
        assert AseguradoraOut.model_fields is not None
        assert len(AseguradoraOut.model_fields) > 0

    def test_secretariador_schemas_import(self):
        from api.schemas.secretariador_schemas import (
            SolicitudOut, ComisionadoOut,
        )
        assert SolicitudOut.model_fields is not None

    def test_personalizador_schemas_import(self):
        from api.schemas.personalizador_schemas import (
            GerenciaOut, DireccionOut, DepartamentoPerOut, CustomUserOut,
        )
        assert GerenciaOut.model_fields is not None
        assert CustomUserOut.model_fields is not None


class OpenAPITest(TestCase):
    """Test that OpenAPI schema is accessible via Django URLconf."""

    def setUp(self):
        self.client = Client()

    def test_openapi_schema_available(self):
        # /v1/api/openapi.json is staff-only too (same docs_decorator as /docs).
        staff = UserModel.objects.create_user(username="openapi_staff", password="pass1234!", is_staff=True)
        self.client.login(username="openapi_staff", password="pass1234!")
        resp = self.client.get("/v1/api/openapi.json")
        assert resp.status_code == 200
        data = resp.json()
        assert "paths" in data or "info" in data

    def test_docs_url_available(self):
        # /v1/api/docs is staff-only (docs_decorator=staff_member_required in api/router.py).
        staff = UserModel.objects.create_user(username="docs_staff", password="pass1234!", is_staff=True)
        self.client.login(username="docs_staff", password="pass1234!")
        resp = self.client.get("/v1/api/docs")
        # Should return HTML (status 200) for Swagger UI
        assert resp.status_code == 200


class ModelPermissionEnforcementTest(TestCase):
    """A logged-in user with no Django permissions must be rejected (403);
    granting the matching `carga.<action>_receptor` permission must let it through."""

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.client.login(username="plain_user", password="pass1234!")

    def test_create_receptor_forbidden_without_permission(self):
        resp = self.client.post(
            "/v1/api/receptores/",
            data=json.dumps({"receptor_nombre": "Test"}),
            content_type="application/json",
        )
        assert resp.status_code == 403

    def test_create_receptor_allowed_with_permission(self):
        perm = Permission.objects.get(codename="add_receptor", content_type__app_label="carga")
        self.user.user_permissions.add(perm)
        resp = self.client.post(
            "/v1/api/receptores/",
            data=json.dumps({"receptor_nombre": "Test"}),
            content_type="application/json",
        )
        assert resp.status_code in (200, 201)

    def test_list_receptores_forbidden_without_view_permission(self):
        resp = self.client.get("/v1/api/receptores/")
        assert resp.status_code == 403

    def test_delete_receptor_forbidden_without_permission(self):
        from carga.models import Receptor

        r = Receptor.objects.create(receptor_nombre="Test")
        resp = self.client.delete(f"/v1/api/receptor/{r.id}/")
        assert resp.status_code == 403


class CsrfEnforcementTest(TestCase):
    """POST/PUT/DELETE must be rejected without a valid CSRF token, even for an
    authenticated + permissioned user, since the API relies on session cookies."""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = UserModel.objects.create_user(username="csrf_user", password="pass1234!")
        perm = Permission.objects.get(codename="add_receptor", content_type__app_label="carga")
        self.user.user_permissions.add(perm)
        self.client.login(username="csrf_user", password="pass1234!")

    def test_post_without_csrf_token_rejected(self):
        resp = self.client.post(
            "/v1/api/receptores/",
            data=json.dumps({"receptor_nombre": "Test"}),
            content_type="application/json",
        )
        assert resp.status_code == 403

    def test_post_with_valid_csrf_token_accepted(self):
        token = get_token(RequestFactory().get("/"))
        self.client.cookies["csrftoken"] = token
        resp = self.client.post(
            "/v1/api/receptores/",
            data=json.dumps({"receptor_nombre": "Test"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        assert resp.status_code in (200, 201)
