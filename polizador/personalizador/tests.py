from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from django.core.exceptions import ValidationError

from personalizador.licencias import (
    antiguedad_meses, balance_tipo, dias_licencia_ordinaria_correspondientes, dias_usados,
)
from personalizador.models import (
    Agente, CorteLicencia, GeneroAgente, LicenciaPermiso, PeriodoLicencia, PeriodoLicenciaAgente, TipoLicenciaPermiso,
)

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
        PeriodoLicencia.objects.create(
            periodolicencia_categoria="LOR_ANUAL", periodolicencia_anio=2024,
            periodolicencia_apertura=date(2024, 12, 15), periodolicencia_fecha_limite_solicitud=date(2025, 3, 31),
        )

    def _licencia(self, tipo, cantidad, anulada=False, fecha_desde=date(2024, 3, 1)):
        licencia = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=tipo,
            licenciapermiso_fecha_desde=fecha_desde, licenciapermiso_cantidad=cantidad,
            licenciapermiso_anulada=anulada,
        )
        licencia.full_clean()
        licencia.save()
        return licencia

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


class CorteLicenciaTest(TestCase):
    """Corte de una Licencia Anual: los días gozados antes del reintegro cuentan para
    el balance del año de la licencia; el saldo pendiente no se descuenta hasta que se
    use, y las fracciones que lo consumen no vuelven a descontar del cupo anual."""

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
        PeriodoLicencia.objects.create(
            periodolicencia_categoria="LOR_ANUAL", periodolicencia_anio=2024,
            periodolicencia_apertura=date(2024, 12, 15), periodolicencia_fecha_limite_solicitud=date(2025, 3, 31),
        )
        PeriodoLicencia.objects.create(
            periodolicencia_categoria="LOR_ANUAL", periodolicencia_anio=2025,
            periodolicencia_apertura=date(2025, 12, 15), periodolicencia_fecha_limite_solicitud=date(2026, 3, 31),
        )
        self.licencia = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_anual,
            licenciapermiso_fecha_desde=date(2024, 1, 5), licenciapermiso_cantidad=21,
        )
        self.licencia.full_clean()
        self.licencia.save()

    def _corte(self, dias_gozados=10, dias_pendientes=11, fecha_reintegro=date(2024, 1, 15)):
        return CorteLicencia.objects.create(
            cortelicencia_licencia=self.licencia,
            cortelicencia_fecha_reintegro=fecha_reintegro,
            cortelicencia_dias_gozados=dias_gozados,
            cortelicencia_dias_pendientes=dias_pendientes,
            cortelicencia_fecha_vencimiento=date(2025, 4, 30),
        )

    def test_dias_usados_cuenta_solo_los_gozados_antes_del_corte(self):
        self._corte()
        self.assertEqual(dias_usados(self.agente, self.tipo_anual, 2024), 10)

    def test_dias_restantes_baja_al_cargar_una_fraccion(self):
        corte = self._corte()
        LicenciaPermiso.objects.create(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_anual,
            licenciapermiso_fecha_desde=date(2024, 6, 1), licenciapermiso_cantidad=3,
            licenciapermiso_saldo_de_corte=corte,
        )
        self.assertEqual(corte.dias_restantes, 8)

    def test_fraccion_no_descuenta_del_cupo_anual_del_ano_en_que_se_usa(self):
        corte = self._corte()
        LicenciaPermiso.objects.create(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_anual,
            licenciapermiso_fecha_desde=date(2024, 6, 1), licenciapermiso_cantidad=3,
            licenciapermiso_saldo_de_corte=corte,
        )
        self.assertEqual(dias_usados(self.agente, self.tipo_anual, 2024), 10)

    def test_fraccion_puede_cruzar_al_ano_calendario_siguiente(self):
        corte = self._corte()
        fraccion = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_anual,
            licenciapermiso_fecha_desde=date(2025, 2, 1), licenciapermiso_cantidad=5,
            licenciapermiso_saldo_de_corte=corte,
        )
        fraccion.full_clean()
        fraccion.save()
        self.assertEqual(corte.dias_restantes, 6)
        self.assertEqual(dias_usados(self.agente, self.tipo_anual, 2025), 0)

    def test_fraccion_no_puede_superar_el_saldo_pendiente(self):
        corte = self._corte()
        fraccion = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_anual,
            licenciapermiso_fecha_desde=date(2024, 6, 1), licenciapermiso_cantidad=12,
            licenciapermiso_saldo_de_corte=corte,
        )
        with self.assertRaises(ValidationError):
            fraccion.full_clean()

    def test_fraccion_no_puede_superar_fecha_de_vencimiento(self):
        corte = self._corte()
        fraccion = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_anual,
            licenciapermiso_fecha_desde=date(2025, 5, 1), licenciapermiso_cantidad=3,
            licenciapermiso_saldo_de_corte=corte,
        )
        with self.assertRaises(ValidationError):
            fraccion.full_clean()

    def test_corte_no_permitido_sobre_licencia_no_anual(self):
        tipo_otro = TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="PER", tipolicenciapermiso_nombre="Donación de Sangre",
            tipolicenciapermiso_unidad="DH", tipolicenciapermiso_tope_cantidad=1,
            tipolicenciapermiso_tope_periodo="VEZ",
        )
        licencia_otro = LicenciaPermiso.objects.create(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=tipo_otro,
            licenciapermiso_fecha_desde=date(2024, 1, 5), licenciapermiso_cantidad=1,
        )
        corte = CorteLicencia(
            cortelicencia_licencia=licencia_otro,
            cortelicencia_fecha_reintegro=date(2024, 1, 5),
            cortelicencia_dias_gozados=0, cortelicencia_dias_pendientes=1,
            cortelicencia_fecha_vencimiento=date(2025, 4, 30),
        )
        with self.assertRaises(ValidationError):
            corte.full_clean()


class LicenciaAnualAdelantadaTest(TestCase):
    """Art. 10, Ley 645-A: la Licencia Anual Ordinaria puede adelantarse, total o
    parcialmente, contra el cupo del PROPIO período de fecha_desde (año vencido: el
    período <año> recién abre el 15/12/<año>, así que tomarlo antes es "adelantarlo"),
    no contra el año siguiente."""

    def setUp(self):
        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.agente = Agente.objects.create(
            agente_nombres="Ana", agente_apellidos="Gomez",
            sexo=genero, dni=30222333, cuil="27302223334",
            fecha_ingreso=date(2000, 1, 1),  # +18 años -> 49 días/año
        )
        self.tipo_anual = TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre="Anual",
            tipolicenciapermiso_unidad="DC", tipolicenciapermiso_tope_periodo="VAR",
        )
        self.tipo_adelantada = TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre="Anual Proporcional",
            tipolicenciapermiso_unidad="DC", tipolicenciapermiso_tope_periodo="VAR",
        )
        self.periodo_2024 = PeriodoLicencia.objects.create(
            periodolicencia_categoria="LOR_ANUAL", periodolicencia_anio=2024,
            periodolicencia_apertura=date(2024, 12, 15), periodolicencia_fecha_limite_solicitud=date(2025, 3, 31),
        )
        self.periodo_2025 = PeriodoLicencia.objects.create(
            periodolicencia_categoria="LOR_ANUAL", periodolicencia_anio=2025,
            periodolicencia_apertura=date(2025, 12, 15), periodolicencia_fecha_limite_solicitud=date(2026, 3, 31),
        )

    def _guardar(self, tipo, fecha_desde, cantidad):
        licencia = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=tipo,
            licenciapermiso_fecha_desde=fecha_desde, licenciapermiso_cantidad=cantidad,
        )
        licencia.full_clean()
        licencia.save()
        return licencia

    def test_balance_adelantada_sin_uso_muestra_cupo_del_propio_periodo(self):
        balance = balance_tipo(self.agente, self.tipo_adelantada, 2025)
        self.assertEqual(balance["correspondientes"], 49)
        self.assertEqual(balance["usados"], 0)
        self.assertEqual(balance["disponibles"], 49)

    def test_adelanto_consume_cupo_del_propio_periodo(self):
        self._guardar(self.tipo_adelantada, date(2025, 8, 18), 10)
        self.assertEqual(dias_usados(self.agente, self.tipo_anual, 2024), 0)
        self.assertEqual(dias_usados(self.agente, self.tipo_anual, 2025), 10)

        balance_2025 = balance_tipo(self.agente, self.tipo_anual, 2025)
        self.assertEqual(balance_2025["correspondientes"], 49)
        self.assertEqual(balance_2025["disponibles"], 39)

    def test_adelanto_no_puede_superar_cupo_disponible(self):
        licencia = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_adelantada,
            licenciapermiso_fecha_desde=date(2025, 8, 18), licenciapermiso_cantidad=50,
        )
        with self.assertRaises(ValidationError):
            licencia.full_clean()

    def test_adelanto_descuenta_cupo_ya_comprometido_por_licencia_anual_normal(self):
        self._guardar(self.tipo_anual, date(2025, 1, 10), 40)
        balance = balance_tipo(self.agente, self.tipo_adelantada, 2025)
        self.assertEqual(balance["correspondientes"], 9)

    def test_editar_adelanto_no_se_descuenta_dos_veces_contra_si_mismo(self):
        licencia = self._guardar(self.tipo_adelantada, date(2025, 8, 18), 20)
        licencia.licenciapermiso_cantidad = 25
        licencia.full_clean()
        licencia.save()
        self.assertEqual(dias_usados(self.agente, self.tipo_anual, 2025), 25)

    def test_periodo_compartido_entre_anual_y_art10(self):
        """Art. 7 y Art. 10 comparten el mismo PeriodoLicencia LOR_ANUAL de un año
        dado: Art. 10 no tiene cupo propio, adelanta días del mismo pozo de Art. 7."""
        anual = self._guardar(self.tipo_anual, date(2025, 1, 10), 20)
        adelanto = self._guardar(self.tipo_adelantada, date(2025, 8, 18), 10)

        self.assertEqual(anual.licenciapermiso_periodo, self.periodo_2025)
        self.assertEqual(adelanto.licenciapermiso_periodo, self.periodo_2025)
        self.assertEqual(dias_usados(self.agente, self.tipo_anual, 2025), 30)

    def test_congelado_no_cambia_si_se_corrige_fecha_ingreso_despues(self):
        """El cupo por antigüedad se congela (PeriodoLicenciaAgente) la primera vez
        que se usa un período: una corrección posterior de fecha_ingreso no debe
        alterar retroactivamente el balance ya otorgado."""
        self._guardar(self.tipo_anual, date(2024, 3, 1), 10)
        self.assertEqual(balance_tipo(self.agente, self.tipo_anual, 2024)["correspondientes"], 49)

        self.agente.fecha_ingreso = date(2023, 1, 1)  # antigüedad << 5 años -> otro tramo (23 días)
        self.agente.save()

        self.assertEqual(balance_tipo(self.agente, self.tipo_anual, 2024)["correspondientes"], 49)

    def test_clean_falla_si_no_existe_periodo(self):
        licencia = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_anual,
            licenciapermiso_fecha_desde=date(2030, 1, 10), licenciapermiso_cantidad=10,
        )
        with self.assertRaises(ValidationError):
            licencia.full_clean()


class AdelantoBloqueadoPorSaldoPendienteTest(TestCase):
    """No se puede tomar un adelanto de Art. 10 contra el período P (el propio año
    de fecha_desde) mientras quede saldo pendiente sin resolver de un corte de un
    período LOR_ANUAL anterior (estrictamente) a P."""

    def setUp(self):
        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.agente = Agente.objects.create(
            agente_nombres="Ana", agente_apellidos="Gomez",
            sexo=genero, dni=30222333, cuil="27302223334",
            fecha_ingreso=date(2000, 1, 1),  # +18 años -> 49 días/año
        )
        self.tipo_anual = TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre="Anual",
            tipolicenciapermiso_unidad="DC", tipolicenciapermiso_tope_periodo="VAR",
        )
        self.tipo_adelantada = TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre="Anual Proporcional",
            tipolicenciapermiso_unidad="DC", tipolicenciapermiso_tope_periodo="VAR",
        )
        for anio in (2023, 2024, 2025):
            PeriodoLicencia.objects.create(
                periodolicencia_categoria="LOR_ANUAL", periodolicencia_anio=anio,
                periodolicencia_apertura=date(anio, 12, 15), periodolicencia_fecha_limite_solicitud=date(anio + 1, 3, 31),
            )

    def _licencia_con_corte(self, fecha_desde, cantidad, dias_gozados, dias_pendientes):
        licencia = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_anual,
            licenciapermiso_fecha_desde=fecha_desde, licenciapermiso_cantidad=cantidad,
        )
        licencia.full_clean()
        licencia.save()
        CorteLicencia.objects.create(
            cortelicencia_licencia=licencia,
            cortelicencia_fecha_reintegro=fecha_desde,
            cortelicencia_dias_gozados=dias_gozados,
            cortelicencia_dias_pendientes=dias_pendientes,
            cortelicencia_fecha_vencimiento=date(fecha_desde.year + 2, 4, 30),
        )
        return licencia

    def test_art10_bloqueado_por_saldo_de_corte_pendiente_de_periodo_anterior(self):
        self._licencia_con_corte(date(2023, 1, 10), 42, dias_gozados=10, dias_pendientes=32)

        adelanto = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_adelantada,
            licenciapermiso_fecha_desde=date(2024, 3, 1), licenciapermiso_cantidad=5,
        )
        with self.assertRaises(ValidationError):
            adelanto.full_clean()

    def test_art10_permitido_si_corte_pendiente_es_del_mismo_periodo_destino(self):
        """Un saldo pendiente del propio período que se está adelantando (P, no
        anterior a P) no bloquea el adelanto."""
        self._licencia_con_corte(date(2024, 1, 10), 42, dias_gozados=10, dias_pendientes=32)

        adelanto = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_adelantada,
            licenciapermiso_fecha_desde=date(2024, 8, 1), licenciapermiso_cantidad=5,
        )
        adelanto.full_clean()  # no debe levantar ValidationError
        adelanto.save()


class LicenciaInviernoTest(TestCase):
    """Anual de Invierno usa su propia categoría de PeriodoLicencia (turnos fijos
    por decreto) y no participa del congelado de cupo por antigüedad."""

    def setUp(self):
        genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.agente = Agente.objects.create(
            agente_nombres="Ana", agente_apellidos="Gomez",
            sexo=genero, dni=30222333, cuil="27302223334",
            fecha_ingreso=date(2000, 1, 1),
        )
        self.tipo_invierno = TipoLicenciaPermiso.objects.create(
            tipolicenciapermiso_categoria="LOR", tipolicenciapermiso_nombre="Anual de Invierno",
            tipolicenciapermiso_unidad="DC", tipolicenciapermiso_tope_periodo="VAR",
        )
        self.periodo_invierno_2025 = PeriodoLicencia.objects.create(
            periodolicencia_categoria="LOR_INVIERNO", periodolicencia_anio=2025,
            periodolicencia_turno1_desde=date(2025, 7, 16), periodolicencia_turno1_hasta=date(2025, 7, 25),
            periodolicencia_turno2_desde=date(2025, 7, 28), periodolicencia_turno2_hasta=date(2025, 8, 6),
        )

    def test_invierno_no_genera_periodolicenciaagente(self):
        licencia = LicenciaPermiso(
            licenciapermiso_agente=self.agente, licenciapermiso_tipo=self.tipo_invierno,
            licenciapermiso_fecha_desde=date(2025, 7, 16), licenciapermiso_cantidad=10,
        )
        licencia.full_clean()
        licencia.save()

        self.assertEqual(licencia.licenciapermiso_periodo, self.periodo_invierno_2025)
        self.assertFalse(PeriodoLicenciaAgente.objects.filter(periodolicenciaagente_agente=self.agente).exists())


class PeriodoLicenciaModelTest(TestCase):
    """PeriodoLicencia.clean() exige los campos según categoría (Ley 645-A: fechas
    reales de decreto, no inventadas por el sistema)."""

    def test_anual_requiere_apertura_y_limite(self):
        periodo = PeriodoLicencia(periodolicencia_categoria="LOR_ANUAL", periodolicencia_anio=2030)
        with self.assertRaises(ValidationError):
            periodo.full_clean()

    def test_invierno_requiere_los_4_campos_de_turno(self):
        periodo = PeriodoLicencia(
            periodolicencia_categoria="LOR_INVIERNO", periodolicencia_anio=2030,
            periodolicencia_turno1_desde=date(2030, 7, 16), periodolicencia_turno1_hasta=date(2030, 7, 25),
        )
        with self.assertRaises(ValidationError):
            periodo.full_clean()

    def test_invierno_turno2_debe_empezar_despues_del_turno1(self):
        periodo = PeriodoLicencia(
            periodolicencia_categoria="LOR_INVIERNO", periodolicencia_anio=2030,
            periodolicencia_turno1_desde=date(2030, 7, 16), periodolicencia_turno1_hasta=date(2030, 7, 25),
            periodolicencia_turno2_desde=date(2030, 7, 20), periodolicencia_turno2_hasta=date(2030, 8, 6),
        )
        with self.assertRaises(ValidationError):
            periodo.full_clean()


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

    def test_crear_licenciapermiso_ok_con_permiso(self):
        """El formulario (con el cálculo automático de días vía la API de balance)
        debe renderizar sin errores de template."""
        perm = Permission.objects.get(codename="add_licenciapermiso", content_type__app_label="personalizador")
        self.user.user_permissions.add(perm)
        self.client.login(username="licencias_user", password="pass1234!")
        resp = self.client.get(reverse("personalizador:crear-licenciapermiso"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "licenciapermiso-balance/")


class InstrumentosAgenteTest(TestCase):
    """Vinculacion de los instrumentos legales del Agente (personalizador/instrumentos.py)."""

    def setUp(self):
        from secretariador.models import InstrumentosLegalesDecretos, InstrumentosLegalesResoluciones
        self.genero = GeneroAgente.objects.create(generoagente_nombre="Test")
        self.res_presidencia = InstrumentosLegalesResoluciones.objects.create(
            instrumentolegalresoluciones_tipo="P", instrumentolegalresoluciones_numero=38,
            instrumentolegalresoluciones_ano="2021",
        )
        self.res_directorio = InstrumentosLegalesResoluciones.objects.create(
            instrumentolegalresoluciones_tipo="D", instrumentolegalresoluciones_numero=940,
            instrumentolegalresoluciones_acta="32", instrumentolegalresoluciones_ano="2015",
        )
        self.decreto = InstrumentosLegalesDecretos.objects.create(
            instrumentolegaldecretos_tipo="P", instrumentolegaldecretos_numero=1458,
            instrumentolegaldecretos_ano="2012",
        )

    def _agente(self, **kwargs):
        return Agente.objects.create(
            agente_nombres="Juan", agente_apellidos="Perez", sexo=self.genero,
            dni=30111222, cuil="20301112223", **kwargs,
        )

    def test_parsear(self):
        from personalizador.instrumentos import parsear
        self.assertEqual(parsear("940/32/2015"), (940, "32", "2015"))
        self.assertEqual(parsear("0038-21"), (38, None, "2021"))
        self.assertEqual(parsear("2760/97"), (2760, None, "1997"))
        self.assertIsNone(parsear("1570"))
        self.assertIsNone(parsear("RES. ANSES 26"))

    def test_buscar_por_tipo(self):
        from personalizador.instrumentos import buscar, AMBIGUO, SIN_MATCH, RES, DEC
        self.assertEqual(buscar(RES, "0038/21").instrumento, self.res_presidencia)
        self.assertEqual(buscar(RES, "940/32/2015").instrumento, self.res_directorio)
        self.assertEqual(buscar(RES, "940/2015").motivo, SIN_MATCH)
        self.assertEqual(buscar(DEC, "1458/12").instrumento, self.decreto)
        self.assertEqual(buscar(None, "1458/2012").tipo, DEC)
        self.assertEqual(buscar("DIS", "1458/2012").motivo, SIN_MATCH)

        from secretariador.models import InstrumentosLegalesDecretos
        InstrumentosLegalesDecretos.objects.create(
            instrumentolegaldecretos_tipo="P", instrumentolegaldecretos_numero=38,
            instrumentolegaldecretos_ano="2021",
        )
        self.assertEqual(buscar(None, "38/2021").motivo, AMBIGUO)

    def test_clean_rechaza_dos_instrumentos_del_mismo_concepto(self):
        agente = self._agente(
            instrumento_bonificacion_resolucion=self.res_presidencia,
            instrumento_bonificacion_decreto=self.decreto,
        )
        with self.assertRaises(ValidationError):
            agente.clean()

    def test_form_descarta_la_fk_del_tipo_no_elegido_y_limpia_heredado(self):
        from core.validators import get_cuil
        from personalizador.forms.agenteforms import AgenteForm
        agente = self._agente(instrumento_bonificacion="1458/2012", instrumento_bonificacion_tipo="DEC")
        data = {
            "agente_nombres": "Juan", "agente_apellidos": "Perez", "sexo": self.genero.pk,
            "dni": 30111222, "cuil": get_cuil("30111222", "M"), "activdad_central": "1",
            "tipo_instrumento_bonificacion": "DEC",
            "instrumento_bonificacion_resolucion": self.res_presidencia.pk,
            "instrumento_bonificacion_decreto": self.decreto.pk,
        }
        form = AgenteForm(data, instance=agente)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        agente.refresh_from_db()
        self.assertEqual(agente.instrumento_bonificacion_decreto, self.decreto)
        self.assertIsNone(agente.instrumento_bonificacion_resolucion)
        self.assertIsNone(agente.instrumento_bonificacion)
        self.assertIsNone(agente.instrumento_bonificacion_tipo)

    def test_comando_vincular(self):
        from io import StringIO
        from django.core.management import call_command
        agente = self._agente(
            n_decreto="1458/2012",
            instrumento_contrato_de_servicio="940/32/2015", instrumento_contrato_de_servicio_tipo="RES",
            instrumento_bonificacion="9999/2020", instrumento_bonificacion_tipo="RES",
        )

        call_command("vincular_instrumentos_agente", "--dry-run", stdout=StringIO())
        agente.refresh_from_db()
        self.assertIsNone(agente.instrumento_pase_planta_decreto)
        self.assertEqual(agente.n_decreto, "1458/2012")

        call_command("vincular_instrumentos_agente", stdout=StringIO())
        agente.refresh_from_db()
        self.assertEqual(agente.instrumento_pase_planta_decreto, self.decreto)
        self.assertIsNone(agente.n_decreto)
        self.assertEqual(agente.instrumento_contrato_servicio_resolucion, self.res_directorio)
        self.assertIsNone(agente.instrumento_contrato_de_servicio_tipo)
        # Sin coincidencia: queda como dato heredado.
        self.assertEqual(agente.instrumento_bonificacion, "9999/2020")
        self.assertTrue(Agente.objects.filter(Agente.q_instrumentos_sin_vincular(), pk=agente.pk).exists())

    def test_popup_resolucion_acta(self):
        from secretariador.forms.instrumentoslegalesform import InstrumentosLegalesResolucionesPopupForm
        base = {
            "instrumentolegalresoluciones_numero": 12, "instrumentolegalresoluciones_ano": "2026",
            "instrumentolegalresoluciones_fecha_aprobacion": "2026-01-10",
        }
        form = InstrumentosLegalesResolucionesPopupForm({**base, "instrumentolegalresoluciones_tipo": "D"})
        self.assertIn("instrumentolegalresoluciones_acta", form.errors)

        form = InstrumentosLegalesResolucionesPopupForm({**base, "instrumentolegalresoluciones_tipo": "D", "instrumentolegalresoluciones_acta": "5"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().instrumentolegalresoluciones_acta, "05")

        form = InstrumentosLegalesResolucionesPopupForm({**base, "instrumentolegalresoluciones_tipo": "P", "instrumentolegalresoluciones_acta": "7"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().instrumentolegalresoluciones_acta, "")

    def test_paginas_y_filtro_sin_vincular(self):
        import json
        usuario = UserModel.objects.create_superuser("admin", "admin@example.com", "x")
        self.client.force_login(usuario)
        vinculado = self._agente(instrumento_pase_planta_decreto=self.decreto)
        heredado = Agente.objects.create(
            agente_nombres="Ana", agente_apellidos="Gomez", sexo=self.genero,
            dni=30111333, cuil="27301113334", instrumento_bonificacion="0074/05/2014", instrumento_bonificacion_tipo="RES",
        )

        respuesta = self.client.get(reverse("personalizador:update-agente", args=[heredado.pk]))
        self.assertContains(respuesta, "Dato heredado sin vincular")
        self.assertContains(respuesta, 'name="tipo_instrumento_bonificacion"')

        respuesta = self.client.get(reverse("personalizador:ficha-agente", args=[vinculado.pk]))
        self.assertContains(respuesta, reverse("secretariador:update-decreto", args=[self.decreto.pk]))
        respuesta = self.client.get(reverse("personalizador:ficha-agente", args=[heredado.pk]))
        self.assertContains(respuesta, "sin vincular")

        respuesta = self.client.get("/v1/api/datatables/agentes/", {"filters": json.dumps({"instrumentos_sin_vincular": "true"})})
        self.assertEqual([fila["id"] for fila in respuesta.json()["data"]], [heredado.pk])

        respuesta = self.client.get(reverse("secretariador:crear-resolucion"), {"_popup": "1"})
        self.assertContains(respuesta, "popupCreateForm")
        respuesta = self.client.get(reverse("personalizador:crear-instrumentoagente"), {"_popup": "1"})
        self.assertNotContains(respuesta, 'type="file"')
        respuesta = self.client.get(reverse("personalizador:lista-instrumentoagentes"))
        self.assertEqual(respuesta.status_code, 200)
