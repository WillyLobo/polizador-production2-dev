from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from django.db import IntegrityError
from django.test import TestCase

from carga.models import Departamento, Localidad, Municipio
from gdu.models import (
    Actuacion, Adjudicatario3450, Contratacion, DestinoParcela, Encuesta, Intervencion, IntervencionEjecutor,
    Ejecutor, Parcela, Programa, Relevamiento, TipoContratacion, TipoEjecutor, TipoIntervencion, Uf,
    ViviendaPunto, ViviendaRelevamiento,
)
from gdu.models.base import SRID_GDU

CUADRADO = Polygon(((0, 0), (0, 10), (10, 10), (10, 0), (0, 0)), srid=SRID_GDU)

NOMENCLATURA = {
    "dpto": "01", "circ": "002", "secc": "03", "ch": "0004", "qta": "0005", "fracc": "0006", "mz": "0007",
    "parc": "00008",
}


class ModelosGduTest(TestCase):
    """Los modelos de gdu son managed=True: la base de test se arma con migrate, sin
    crear tablas a mano como hacía el piloto."""

    @classmethod
    def setUpTestData(cls):
        departamento = Departamento.objects.create(id=1, departamento_nombre="San Fernando")
        municipio = Municipio.objects.create(id=1, municipio_nombre="Resistencia", municipio_departamento=departamento)
        localidad = Localidad.objects.create(
            id=1, localidad_nombre="Resistencia", localidad_departamento=departamento, localidad_municipio=municipio,
        )
        programa = Programa.objects.create(nombre="Programa", origen=Programa.Origen.PROVINCIAL)
        actuacion = Actuacion.objects.create(programa=programa, ano=2024, nombre="Actuación", instrumento="Res. 1")
        contratacion = Contratacion.objects.create(
            actuacion=actuacion, tipo=TipoContratacion.objects.create(nombre="Licitación Pública"), ano=2024,
            expediente="E10-2024-1-A",
        )
        cls.intervencion = Intervencion.objects.create(
            contratacion=contratacion, localidad=localidad, nombre="40 viviendas",
            tipo=TipoIntervencion.objects.create(nombre="Construcción de viviendas"),
        )
        cls.destino = DestinoParcela.objects.create(nombre="Vivienda")

    def crear_parcela(self, **kwargs):
        return Parcela.objects.create(
            intervencion=self.intervencion, destino=self.destino, geom=CUADRADO, **{**NOMENCLATURA, **kwargs},
        )

    def test_nomenclatura_se_genera_en_la_base(self):
        parcela = self.crear_parcela()
        parcela.refresh_from_db()
        self.assertEqual(parcela.nomenclatura, "01002030004000500060007" "00008")

    def test_nomenclatura_opcional_es_null_si_falta_una_parte(self):
        vivienda = ViviendaPunto.objects.create(
            intervencion=self.intervencion, estado_dominial="ipduv", geom=Point(5, 5, srid=SRID_GDU),
            **{**NOMENCLATURA, "parc": None},
        )
        vivienda.refresh_from_db()
        self.assertIsNone(vivienda.nomenclatura)

    def test_es_ph_se_calcula_por_cantidad_de_ufs(self):
        simple = self.crear_parcela()
        ph = self.crear_parcela(parc="00009")
        Uf.objects.create(parcela=simple, uf="1", geom=CUADRADO)
        Uf.objects.create(parcela=ph, uf="1", geom=CUADRADO)
        Uf.objects.create(parcela=ph, uf="2", geom=CUADRADO)
        es_ph = dict(Parcela.objects.con_es_ph().values_list("pk", "es_ph"))
        self.assertEqual(es_ph, {simple.pk: False, ph.pk: True})

    def test_uf_admite_adjudicatario_no_importado_todavia(self):
        # db_constraint=False: el Sistema 3450 puede ir atrasado respecto de la carga
        uf = Uf.objects.create(parcela=self.crear_parcela(), uf="1", geom=CUADRADO, adjudicatario_id=99999)
        self.assertFalse(Adjudicatario3450.objects.filter(pk=99999).exists())
        self.assertEqual(Uf.objects.get(pk=uf.pk).adjudicatario_id, 99999)

    def test_relevado_se_deriva_de_las_encuestas(self):
        relevamiento = Relevamiento.objects.create(nombre="Fontana", fecha="2024-01-01", objetivo=10)
        geom = MultiPolygon(CUADRADO)
        encuestada = ViviendaRelevamiento.objects.create(relevamiento=relevamiento, numero=1, geom=geom)
        pendiente = ViviendaRelevamiento.objects.create(relevamiento=relevamiento, numero=2, geom=geom)
        Encuesta.objects.create(relevamiento=relevamiento, vivienda=encuestada)
        relevado = dict(ViviendaRelevamiento.objects.con_relevado().values_list("pk", "relevado"))
        self.assertEqual(relevado, {encuestada.pk: True, pendiente.pk: False})

    def test_nn_no_admite_pares_duplicados(self):
        ejecutor = Ejecutor.objects.create(
            tipo=TipoEjecutor.objects.create(nombre="Empresa"), cuit="20123456786", nombre="Constructora",
        )
        IntervencionEjecutor.objects.create(intervencion=self.intervencion, ejecutor=ejecutor)
        with self.assertRaises(IntegrityError):
            IntervencionEjecutor.objects.create(intervencion=self.intervencion, ejecutor=ejecutor)

    def test_cambios_quedan_en_el_historial(self):
        parcela = self.crear_parcela()
        parcela.estado_dominial = "ipduv"
        parcela.save()
        self.assertEqual(parcela.history.count(), 2)
