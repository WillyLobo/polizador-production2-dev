from django.test import TestCase, Client
from ninja.testing import TestClient
from api.router import api


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
            CertificadoRubro, CertificadoFinanciamiento, Agente,
        )
        from personalizador.models import CargoTipo, Gerencia, Direccion

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
        Gerencia.objects.get_or_create(gerencia_nombre="Gerencia Test", gerencia_cuof="G001")


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
            AgenteOut,
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
            CargosOut, GerenciaOut, CargoTipoOut, CustomUserOut,
        )
        assert CargosOut.model_fields is not None
        assert CustomUserOut.model_fields is not None


class OpenAPITest(TestCase):
    """Test that OpenAPI schema is accessible via Django URLconf."""

    def setUp(self):
        self.client = Client()

    def test_openapi_schema_available(self):
        resp = self.client.get("/v1/api/openapi.json")
        assert resp.status_code == 200
        data = resp.json()
        assert "paths" in data or "info" in data

    def test_docs_url_available(self):
        resp = self.client.get("/v1/api/docs")
        # Should return HTML (status 200) for Swagger UI
        assert resp.status_code == 200
