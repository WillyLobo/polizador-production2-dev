from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from carga.forms.fojademedicionforms import FojaDeMedicionForm
from carga.models import (
    Certificado,
    CertificadoFinanciamiento,
    CertificadoRubro,
    Contrato,
    ContratoMonto,
    Empresa,
    FojaDeMedicion,
    Obra,
    PlanDeTrabajos,
    PlanDeTrabajosEtapa,
    PlanDeTrabajosEtapaItem,
    PlanDeTrabajosItem,
    PlanDeTrabajosRubro,
    Programa,
    Uvi,
)


class UviPesosEquivalentesTests(TestCase):
    def setUp(self):
        Uvi.objects.create(uvi_fecha=date(2026, 1, 1), uvi_valor=Decimal("100.00"))
        Uvi.objects.create(uvi_fecha=date(2026, 3, 1), uvi_valor=Decimal("120.00"))

    def test_usa_la_cotizacion_exacta_de_la_fecha(self):
        resultado = Uvi.pesos_equivalentes(Decimal("10"), date(2026, 3, 1))
        self.assertEqual(resultado, Decimal("1200.00"))

    def test_usa_la_cotizacion_anterior_mas_cercana(self):
        resultado = Uvi.pesos_equivalentes(Decimal("10"), date(2026, 2, 15))
        self.assertEqual(resultado, Decimal("1000.00"))

    def test_sin_cotizacion_previa_devuelve_none(self):
        resultado = Uvi.pesos_equivalentes(Decimal("10"), date(2025, 1, 1))
        self.assertIsNone(resultado)

    def test_sin_monto_o_fecha_devuelve_none(self):
        self.assertIsNone(Uvi.pesos_equivalentes(None, date(2026, 3, 1)))
        self.assertIsNone(Uvi.pesos_equivalentes(Decimal("10"), None))


class PlanDeTrabajosEtapaTestCase(TestCase):
    def setUp(self):
        empresa = Empresa.objects.create(empresa_nombre="Empresa Test")
        programa = Programa.objects.create(programa_nombre="Programa Test")
        self.obra = Obra.objects.create(
            obra_nombre="Obra Test",
            obra_empresa=empresa,
            obra_programa=programa,
            obra_expediente="EXP-1",
        )
        self.plan = PlanDeTrabajos.objects.create(
            trabajos_obra=self.obra, trabajos_fecha=date(2026, 1, 1)
        )

    def _crear_rubro(self, **kwargs):
        defaults = {"rubro_plan": self.plan, "rubro_nombre": "Vivienda", "rubro_presupuesto": Decimal("1000")}
        defaults.update(kwargs)
        return PlanDeTrabajosRubro.objects.create(**defaults)

    def _crear_contratomonto(self, pesos=Decimal("0"), uvi=Decimal("0"), uvi_fecha=None):
        certificado_rubro = CertificadoRubro.objects.create(
            certificadorubro_nombre="Vivienda", certificadorubro_nombre_corto="V"
        )
        financiamiento = CertificadoFinanciamiento.objects.create(
            certificadofinanciamiento_nombre="Nación", certificadofinanciamiento_nombre_corto="N"
        )
        contrato = Contrato.objects.create(contrato_obra=self.obra, contrato_fecha=date(2026, 1, 1))
        return ContratoMonto.objects.create(
            contratomonto_contrato=contrato,
            contratomonto_rubro=certificado_rubro,
            contratomonto_financiamiento=financiamiento,
            contratomonto_pesos=pesos,
            contratomonto_uvi=uvi,
            contratomonto_uvi_fecha=uvi_fecha,
        )

    def test_monto_base_pesos_usa_rubro_presupuesto_sin_contratomonto(self):
        rubro = self._crear_rubro(rubro_presupuesto=Decimal("5000"))
        self.assertEqual(rubro.monto_base_pesos(), Decimal("5000"))

    def test_monto_base_pesos_usa_contratomonto_en_pesos(self):
        contratomonto = self._crear_contratomonto(pesos=Decimal("8000"))
        rubro = self._crear_rubro(rubro_contratomonto=contratomonto)
        self.assertEqual(rubro.monto_base_pesos(), Decimal("8000"))

    def test_monto_base_pesos_convierte_contratomonto_en_uvi(self):
        Uvi.objects.create(uvi_fecha=date(2026, 1, 1), uvi_valor=Decimal("100"))
        contratomonto = self._crear_contratomonto(uvi=Decimal("50"), uvi_fecha=date(2026, 1, 1))
        rubro = self._crear_rubro(rubro_contratomonto=contratomonto)
        self.assertEqual(rubro.monto_base_pesos(), Decimal("5000"))

    def test_etapa_numero_y_fecha_se_asignan_secuencialmente(self):
        rubro = self._crear_rubro()
        item = PlanDeTrabajosItem.objects.create(
            planitem_rubro=rubro, planitem_nombre="Item 1", planitem_incidencia_pct=Decimal("100")
        )

        etapa1 = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
        etapa2 = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)

        self.assertEqual(etapa1.etapa_numero, 1)
        self.assertEqual(etapa1.etapa_fecha, date(2026, 1, 1))
        self.assertEqual(etapa2.etapa_numero, 2)
        self.assertEqual(etapa2.etapa_fecha, date(2026, 2, 1))

    def test_etapaitem_acumula_contra_la_etapa_anterior(self):
        rubro = self._crear_rubro()
        item = PlanDeTrabajosItem.objects.create(
            planitem_rubro=rubro, planitem_nombre="Item 1", planitem_incidencia_pct=Decimal("100")
        )
        etapa1 = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
        etapa2 = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)

        etapaitem1 = PlanDeTrabajosEtapaItem.objects.create(
            etapaitem_etapa=etapa1, etapaitem_planitem=item, etapaitem_pct_proyectado_mes=Decimal("30")
        )
        etapaitem2 = PlanDeTrabajosEtapaItem.objects.create(
            etapaitem_etapa=etapa2, etapaitem_planitem=item, etapaitem_pct_proyectado_mes=Decimal("20")
        )

        self.assertEqual(etapaitem1.etapaitem_pct_proyectado_acumulado, Decimal("30"))
        self.assertEqual(etapaitem2.etapaitem_pct_proyectado_acumulado, Decimal("50"))

    def test_numeracion_continua_a_traves_de_una_reprogramacion(self):
        """Si el rubro se reprograma, las nuevas etapas continúan numerando (no resetean a 1)."""
        rubro_viejo = self._crear_rubro()
        PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro_viejo)
        PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro_viejo)

        plan_nuevo = PlanDeTrabajos.objects.create(trabajos_obra=self.obra, trabajos_fecha=date(2026, 6, 1))
        rubro_nuevo = PlanDeTrabajosRubro.objects.create(
            rubro_plan=plan_nuevo,
            rubro_nombre="Vivienda",
            rubro_presupuesto=Decimal("1000"),
            rubro_anterior=rubro_viejo,
        )

        etapa3 = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro_nuevo)

        self.assertEqual(etapa3.etapa_numero, 3)
        # La fecha sigue siendo consecutiva a partir de la última etapa de la cadena,
        # no de trabajos_fecha del nuevo plan.
        self.assertEqual(etapa3.etapa_fecha, date(2026, 3, 1))

    def test_etapa_monto_pesos(self):
        contratomonto = self._crear_contratomonto(pesos=Decimal("10000"))
        rubro = self._crear_rubro(rubro_contratomonto=contratomonto)
        item = PlanDeTrabajosItem.objects.create(
            planitem_rubro=rubro, planitem_nombre="Item 1", planitem_incidencia_pct=Decimal("100")
        )
        etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
        PlanDeTrabajosEtapaItem.objects.create(
            etapaitem_etapa=etapa, etapaitem_planitem=item, etapaitem_pct_proyectado_mes=Decimal("25")
        )

        self.assertEqual(etapa.etapa_monto_pesos(), Decimal("2500.00"))


class MatrizPlanDeTrabajosEtapaFormValidationTests(TestCase):
    def setUp(self):
        empresa = Empresa.objects.create(empresa_nombre="Empresa Test")
        programa = Programa.objects.create(programa_nombre="Programa Test")
        obra = Obra.objects.create(
            obra_nombre="Obra Test", obra_empresa=empresa, obra_programa=programa, obra_expediente="EXP-2"
        )
        self.plan = PlanDeTrabajos.objects.create(trabajos_obra=obra, trabajos_fecha=date(2026, 1, 1))
        self.rubro = PlanDeTrabajosRubro.objects.create(
            rubro_plan=self.plan, rubro_nombre="Vivienda", rubro_presupuesto=Decimal("1000")
        )
        self.item = PlanDeTrabajosItem.objects.create(
            planitem_rubro=self.rubro, planitem_nombre="Item 1", planitem_incidencia_pct=Decimal("40")
        )

    def test_rechaza_si_la_suma_de_columnas_supera_la_incidencia_del_item(self):
        from carga.forms.plandetrabajosetapaforms import build_matriz_form

        form_class = build_matriz_form([self.item], total_columns=2, anterior_map={})
        form = form_class({f"item_{self.item.pk}_col_0": "30", f"item_{self.item.pk}_col_1": "20"})
        self.assertFalse(form.is_valid())

    def test_acepta_si_la_suma_de_columnas_no_supera_la_incidencia(self):
        from carga.forms.plandetrabajosetapaforms import build_matriz_form

        form_class = build_matriz_form([self.item], total_columns=2, anterior_map={})
        form = form_class({f"item_{self.item.pk}_col_0": "20", f"item_{self.item.pk}_col_1": "20"})
        self.assertTrue(form.is_valid())

    def test_rechaza_si_una_columna_supera_el_100_por_ciento_entre_items(self):
        from carga.forms.plandetrabajosetapaforms import build_matriz_form

        item2 = PlanDeTrabajosItem.objects.create(
            planitem_rubro=self.rubro, planitem_nombre="Item 2", planitem_incidencia_pct=Decimal("100")
        )
        form_class = build_matriz_form([self.item, item2], total_columns=1, anterior_map={})
        form = form_class({f"item_{self.item.pk}_col_0": "40", f"item_{item2.pk}_col_0": "70"})
        self.assertFalse(form.is_valid())


class PlanDeTrabajosEtapaMatrizViewTests(TestCase):
    def setUp(self):
        empresa = Empresa.objects.create(empresa_nombre="Empresa Test")
        programa = Programa.objects.create(programa_nombre="Programa Test")
        obra = Obra.objects.create(
            obra_nombre="Obra Test", obra_empresa=empresa, obra_programa=programa, obra_expediente="EXP-3"
        )
        self.plan = PlanDeTrabajos.objects.create(
            trabajos_obra=obra, trabajos_fecha=date(2026, 1, 1), trabajos_meses=2
        )
        self.rubro = PlanDeTrabajosRubro.objects.create(
            rubro_plan=self.plan, rubro_nombre="Vivienda", rubro_presupuesto=Decimal("1000")
        )
        self.item = PlanDeTrabajosItem.objects.create(
            planitem_rubro=self.rubro, planitem_nombre="Item 1", planitem_incidencia_pct=Decimal("100")
        )
        user = get_user_model().objects.create_superuser(username="tester", password="testpass123")
        self.client.force_login(user)
        self.url = reverse("carga:plandetrabajosetapa-matriz", kwargs={"pk": self.rubro.pk})

    def _post_data(self, valores):
        """`valores`: un valor de % Proyectado del Mes por columna, para el único item."""
        return {f"item_{self.item.pk}_col_{col}": str(valor) for col, valor in enumerate(valores)}

    def test_get_muestra_tantas_columnas_como_trabajos_meses(self):
        response = self.client.get(self.url)
        self.assertContains(response, f'name="item_{self.item.pk}_col_0"')
        self.assertContains(response, f'name="item_{self.item.pk}_col_1"')
        self.assertNotContains(response, f'name="item_{self.item.pk}_col_2"')

    def test_post_crea_una_etapa_por_columna_con_numeracion_y_fecha_correctas(self):
        response = self.client.post(self.url, self._post_data(["30", "20"]))

        self.assertRedirects(
            response, reverse("carga:estado-obra", kwargs={"pk": self.plan.trabajos_obra_id})
        )
        etapas = list(PlanDeTrabajosEtapa.objects.order_by("etapa_numero"))
        self.assertEqual([e.etapa_numero for e in etapas], [1, 2])
        self.assertEqual(etapas[0].etapa_fecha, date(2026, 1, 1))
        self.assertEqual(etapas[1].etapa_fecha, date(2026, 2, 1))

        items = PlanDeTrabajosEtapaItem.objects.filter(
            etapaitem_etapa__in=etapas
        ).order_by("etapaitem_etapa__etapa_numero")
        self.assertEqual([i.etapaitem_pct_proyectado_mes for i in items], [Decimal("30"), Decimal("20")])
        self.assertEqual([i.etapaitem_pct_proyectado_acumulado for i in items], [Decimal("30"), Decimal("50")])

    def test_reabrir_y_modificar_una_columna_anterior_recalcula_el_acumulado_de_las_siguientes(self):
        self.client.post(self.url, self._post_data(["30", "20"]))

        response = self.client.post(self.url, self._post_data(["10", "20"]))

        self.assertEqual(response.status_code, 302)
        items = PlanDeTrabajosEtapaItem.objects.filter(
            etapaitem_planitem=self.item
        ).order_by("etapaitem_etapa__etapa_numero")
        self.assertEqual([i.etapaitem_pct_proyectado_mes for i in items], [Decimal("10"), Decimal("20")])
        self.assertEqual([i.etapaitem_pct_proyectado_acumulado for i in items], [Decimal("10"), Decimal("30")])

    def test_post_rechaza_si_la_suma_total_supera_la_incidencia_del_item(self):
        self.item.planitem_incidencia_pct = Decimal("40")
        self.item.save()

        response = self.client.post(self.url, self._post_data(["30", "20"]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PlanDeTrabajosEtapa.objects.count(), 0)

    def test_completar_etapas_con_una_ya_guardada_no_duplica_el_acumulado_anterior(self):
        """Si ya existe 1 etapa guardada y se reabre la matriz para completar las
        restantes, la etapa existente no debe contarse dos veces (una via el
        acumulado anterior y otra como columna de la matriz)."""
        self.item.planitem_incidencia_pct = Decimal("40")
        self.item.save()
        self.plan.trabajos_meses = 1
        self.plan.save()
        self.client.post(self.url, self._post_data(["30"]))
        self.assertEqual(PlanDeTrabajosEtapa.objects.count(), 1)

        self.plan.trabajos_meses = 3
        self.plan.save()
        response = self.client.post(self.url, self._post_data(["30", "5", "5"]))

        self.assertRedirects(
            response, reverse("carga:estado-obra", kwargs={"pk": self.plan.trabajos_obra_id})
        )
        self.assertEqual(PlanDeTrabajosEtapa.objects.count(), 3)


class FojaDeMedicionNumeracionTests(TestCase):
    def setUp(self):
        empresa = Empresa.objects.create(empresa_nombre="Empresa Test")
        programa = Programa.objects.create(programa_nombre="Programa Test")
        self.obra = Obra.objects.create(
            obra_nombre="Obra Test",
            obra_empresa=empresa,
            obra_programa=programa,
            obra_expediente="EXP-1",
        )
        self.plan = PlanDeTrabajos.objects.create(
            trabajos_obra=self.obra, trabajos_fecha=date(2026, 1, 1)
        )
        self.rubro = PlanDeTrabajosRubro.objects.create(
            rubro_plan=self.plan,
            rubro_nombre="Vivienda",
            rubro_presupuesto=Decimal("1000"),
            rubro_foja_numero_inicial=5,
        )
        self.certificado_rubro_db = CertificadoRubro.objects.create(
            certificadorubro_nombre="Vivienda", certificadorubro_nombre_corto="V"
        )

    def _crear_certificado(self, **kwargs):
        defaults = {
            "certificado_obra": self.obra,
            "certificado_expediente": "EXP-CERT-1",
            "certificado_rubro_db": self.certificado_rubro_db,
        }
        defaults.update(kwargs)
        return Certificado.objects.create(**defaults)

    def test_primera_foja_real_toma_el_numero_inicial_del_rubro(self):
        foja = FojaDeMedicion.objects.create(foja_rubro=self.rubro, foja_periodo=date(2026, 1, 1))
        self.assertEqual(foja.foja_numero, 5)

    def test_foja_legacy_con_numero_manual_y_vinculo_a_certificado(self):
        certificado = self._crear_certificado()

        foja = FojaDeMedicion(foja_rubro=self.rubro, foja_periodo=date(2020, 1, 1), foja_legacy=True)
        foja.foja_numero = 2
        foja.save()

        certificado.certificado_foja = foja
        certificado.save(update_fields=["certificado_foja"])

        foja.refresh_from_db()
        certificado.refresh_from_db()
        self.assertEqual(foja.foja_numero, 2)
        self.assertTrue(foja.foja_legacy)
        self.assertEqual(certificado.certificado_foja_id, foja.pk)

    def test_foja_real_despues_de_legacy_continua_la_secuencia(self):
        foja_legacy = FojaDeMedicion(foja_rubro=self.rubro, foja_periodo=date(2020, 1, 1), foja_legacy=True)
        foja_legacy.foja_numero = 3
        foja_legacy.save()

        foja_legacy_2 = FojaDeMedicion(foja_rubro=self.rubro, foja_periodo=date(2020, 2, 1), foja_legacy=True)
        foja_legacy_2.foja_numero = 4
        foja_legacy_2.save()

        foja_real = FojaDeMedicion.objects.create(foja_rubro=self.rubro, foja_periodo=date(2026, 1, 1))
        self.assertEqual(foja_real.foja_numero, 5)

    def _form_data(self, foja_numero_manual):
        return {
            "foja_rubro": self.rubro.pk,
            "foja_legacy": True,
            "foja_numero_manual": foja_numero_manual,
            "foja_periodo": "2020-02-01",
            "foja_fecha": "2020-02-01",
        }

    def test_form_rechaza_numero_duplicado_en_modo_legacy(self):
        foja_existente = FojaDeMedicion(foja_rubro=self.rubro, foja_periodo=date(2020, 1, 1), foja_legacy=True)
        foja_existente.foja_numero = 2
        foja_existente.save()

        form = FojaDeMedicionForm(data=self._form_data(2))

        self.assertFalse(form.is_valid())
        self.assertIn("foja_numero_manual", form.errors)

    def test_form_rechaza_numero_fuera_de_rango_en_modo_legacy(self):
        form = FojaDeMedicionForm(data=self._form_data(self.rubro.rubro_foja_numero_inicial))

        self.assertFalse(form.is_valid())
        self.assertIn("foja_numero_manual", form.errors)
