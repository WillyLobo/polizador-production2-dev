from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from personalizador.licencias import (
    antiguedad_meses, balance_tipo, dias_licencia_ordinaria_correspondientes,
)
from personalizador.models import Agente, GeneroAgente, LicenciaPermiso, TipoLicenciaPermiso

UserModel = get_user_model()


class DiasLicenciaOrdinariaTest(TestCase):
    """Art. 8, Ley 645-A: tope de días corridos de licencia anual ordinaria según
    antigüedad acreditada al 31/12 de cada año."""

    def setUp(self):
        self.genero = GeneroAgente.objects.create(generoagente_nombre="Test")

    def _agente(self, fecha_ingreso):
        return Agente.objects.create(
            agente_nombres="Juan", agente_apellidos="Perez",
            sexo=self.genero, dni=30111222, cuil="20301112223",
            fecha_ingreso=fecha_ingreso,
        )

    def test_sin_antiguedad_no_tiene_licencia(self):
        agente = self._agente(date(2024, 7, 1))
        self.assertEqual(dias_licencia_ordinaria_correspondientes(agente, 2024), 0)

    def test_justo_en_6_meses(self):
        agente = self._agente(date(2024, 1, 1))
        self.assertEqual(antiguedad_meses(agente, date(2024, 7, 1)), 6)
        self.assertEqual(dias_licencia_ordinaria_correspondientes(agente, 2024), 23)

    def test_hasta_5_anios(self):
        agente = self._agente(date(2019, 12, 31))
        self.assertEqual(dias_licencia_ordinaria_correspondientes(agente, 2024), 23)

    def test_mas_de_5_hasta_10_anios(self):
        agente = self._agente(date(2019, 1, 1))
        self.assertEqual(dias_licencia_ordinaria_correspondientes(agente, 2024), 28)

    def test_mas_de_10_hasta_18_anios(self):
        agente = self._agente(date(2010, 1, 1))
        self.assertEqual(dias_licencia_ordinaria_correspondientes(agente, 2024), 42)

    def test_mas_de_18_anios(self):
        agente = self._agente(date(2000, 1, 1))
        self.assertEqual(dias_licencia_ordinaria_correspondientes(agente, 2024), 49)

    def test_sin_fecha_ingreso(self):
        agente = self._agente(None)
        self.assertEqual(dias_licencia_ordinaria_correspondientes(agente, 2024), 0)


class BalanceTipoTest(TestCase):
    """balance_tipo no debe computar los registros anulados."""

    def setUp(self):
        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.agente = Agente.objects.create(
            agente_nombres="Ana", agente_apellidos="Gomez",
            sexo=genero, dni=30222333, cuil="27302223334",
            fecha_ingreso=date(2000, 1, 1),
        )
        self.tipo_anual = TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre="Anual",
            tipolicenciapermiso_unidad="DC", tipolicenciapermiso_tope_periodo="VAR",
        )
        self.tipo_fijo = TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre="Donación de Sangre",
            tipolicenciapermiso_unidad="DH", tipolicenciapermiso_tope_cantidad=1,
            tipolicenciapermiso_tope_periodo="VEZ",
        )

    def _licencia(self, tipo, cantidad, anulada=False, fecha_desde=date(2024, 3, 1)):
        return LicenciaPermiso.objects.create(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=tipo,
            licenciapermiso_fecha_desde=fecha_desde, licenciapermiso_cantidad=cantidad,
            licenciapermiso_anulada=anulada,
        )

    def test_licencia_anual_usa_antiguedad(self):
        self._licencia(self.tipo_anual, 10)
        balance = balance_tipo(self.agente, self.tipo_anual, 2024)
        self.assertEqual(balance["correspondientes"], 49)
        self.assertEqual(balance["usados"], 10)
        self.assertEqual(balance["disponibles"], 39)

    def test_registro_anulado_no_descuenta(self):
        self._licencia(self.tipo_anual, 10, anulada=True)
        balance = balance_tipo(self.agente, self.tipo_anual, 2024)
        self.assertEqual(balance["usados"], 0)
        self.assertEqual(balance["disponibles"], 49)

    def test_tipo_con_tope_fijo_por_evento_sin_correspondientes(self):
        self._licencia(self.tipo_fijo, 1)
        balance = balance_tipo(self.agente, self.tipo_fijo, 2024)
        # tope_periodo="VEZ" (no "ANI"): no hay un correspondiente anual fijo
        self.assertIsNone(balance["correspondientes"])
        self.assertIsNone(balance["disponibles"])
        self.assertEqual(balance["usados"], 1)


class LicenciaPermisoViewsPermissionTest(TestCase):
    """Las vistas de licencias exigen los permisos correspondientes: sin login
    redirigen, y las funciones basadas en @permission_required(raise_exception=True)
    devuelven 403 a un usuario logueado sin el permiso."""

    def setUp(self):
        self.user = UserModel.objects.create_user(username="licencias_user", password="pass1234!")

    def test_crear_licencia_requiere_login(self):
        resp = self.client.get(reverse("personalizador:crear-licenciapermiso"))
        self.assertEqual(resp.status_code, 302)

    def test_lista_licenciapermisos_403_sin_permiso(self):
        self.client.login(username="licencias_user", password="pass1234!")
        resp = self.client.get(reverse("personalizador:lista-licenciapermisos"))
        self.assertEqual(resp.status_code, 403)

    def test_lista_licenciapermisos_ok_con_permiso(self):
        perm = Permission.objects.get(codename="view_licenciapermiso", content_type__app_label="personalizador")
        self.user.user_permissions.add(perm)
        self.client.login(username="licencias_user", password="pass1234!")
        resp = self.client.get(reverse("personalizador:lista-licenciapermisos"))
        self.assertEqual(resp.status_code, 200)
