import base64
from datetime import date
from io import StringIO

from django.contrib.auth import authenticate, get_user_model
from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from carga.models import Departamento, Localidad, Municipio
from gdu.models import (
    Actuacion, Adjudicatario3450, Contratacion, DestinoParcela, Encuesta, EventoVisor, Intervencion,
    IntervencionEjecutor, Ejecutor, Parcela, PlanoMensura, PlanoMensuraIntervencion, PreAdjudicatarioDispersa,
    PreguntaRelevamiento, Programa, Relevamiento, TipoContratacion, TipoEjecutor, TipoIntervencion, Uf,
    ViviendaPunto, ViviendaRelevamiento, Barrio,
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


class ReglasTest(TestCase):
    def test_traduce_y_evalua_reglas_js_heredadas(self):
        from gdu.reglas import evaluar, traducir_js

        regla = traducir_js(
            "||(e) =>{ return e.relacion != 3 && !(e.vivienda && e.vivienda.perfil=='SOLIDARIDAD') "
            "&& (e.pagando_cuotas==1 || e.pagando_cuotas==4)}||"
        )
        self.assertTrue(evaluar(regla, {"relacion": 1, "vivienda": {"perfil": "X"}, "pagando_cuotas": 4}))
        self.assertFalse(evaluar(regla, {"relacion": 1, "vivienda": {"perfil": "SOLIDARIDAD"}, "pagando_cuotas": 4}))
        self.assertFalse(evaluar(regla, {"relacion": 3, "pagando_cuotas": 1}))

    def test_helper_v_es_opcion_marcada_en_respuesta_multiple(self):
        from gdu.reglas import evaluar, traducir_js

        regla = traducir_js("||(e) => v(e,'modificaciones_tipos',1)||")
        self.assertEqual(regla, {"in": [1, {"var": "modificaciones_tipos"}]})
        self.assertTrue(evaluar(regla, {"modificaciones_tipos": [1, 3]}))
        self.assertFalse(evaluar(regla, {"modificaciones_tipos": [2]}))
        self.assertFalse(evaluar(regla, {}))

    def test_regla_vacia_y_regla_no_soportada(self):
        from gdu.reglas import ReglaInvalida, traducir_js

        self.assertIsNone(traducir_js("||||"))
        with self.assertRaises(ReglaInvalida):
            traducir_js("(e) =>{ return e.lista.map(x => x) }")


class ImportadorLegacyTest(TestCase):
    """Carga el esquema heredado (gdu/etl/fixtures/legacy_schema.sql) en la base de test,
    dentro de la transacción del test, y corre el ETL leyendo de esa misma conexión."""

    DATOS_LEGACY = """
        INSERT INTO public.localidad (id, codpcia, coddpto, codloc, provincia, departamento, localidad, geom) VALUES
            (1, '22', '007', '010', 'Chaco', 'Almirante Brown', 'Concepción del Bermejo', 'SRID=22175;POINT(5500000 7000000)'),
            (2, '22', '999', '999', 'Chaco', 'X', 'Sin equivalente', 'SRID=22175;POINT(5500000 7000000)');
        INSERT INTO public.programa (id, nombre, origen) VALUES (1, 'Programa', 'NACIONAL');
        INSERT INTO public.actuacion (id, id_programa, ano, nombre, instrumento) VALUES (1, 1, 2020, 'Actuación', 'Res 1');
        INSERT INTO public.tipo_contratacion (id, nombre) VALUES (1, 'Licitación');
        INSERT INTO public.contratacion (id, id_actuacion, tipo, ano, expediente) VALUES (1, 1, 1, 2020, 'E10-1');
        INSERT INTO public.tipo_intervencion (id, nombre) VALUES (1, 'Viviendas');
        INSERT INTO public.tipo_estado (id, nombre) VALUES (2, 'Terminadas');
        INSERT INTO public.intervencion (id, id_localidad, id_contratacion, nombre, tipo, estado, grupo, drf_grupo) VALUES
            (1, 1, 1, 'Intervención', 1, 2, NULL, 8),
            (2, 2, 1, 'Sin localidad', 1, NULL, NULL, NULL);
        INSERT INTO public.barrio (id, id_intervencion, nombre, geom) VALUES
            (1, 1, 'Moño', 'SRID=22175;MULTIPOLYGON(((0 0, 10 10, 10 0, 0 10, 0 0)))'),
            (2, 2, 'Huérfano', 'SRID=22175;MULTIPOLYGON(((0 0, 0 10, 10 10, 10 0, 0 0)))');
        INSERT INTO public.destino_parcela (id, nombre) VALUES (1, 'Vivienda');
        INSERT INTO public.parcela (id, id_intervencion, dpto, circ, secc, ch, qta, fracc, mz, parc, destino, geom) VALUES
            (1, 1, '12', '22', '0B', '0028', '0000', '0000', '0006', '00009', 1,
             'SRID=22175;POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))');
        INSERT INTO public.tipo_uf (id, nombre) VALUES (1, 'Vivienda Unifamiliar');
        INSERT INTO public.adjudicatario3450 ("AdjuGISNroAdju", "AdjuGISEscritura", "AdjuGISmatricula") VALUES (500, 'SI', ' 123 ');
        INSERT INTO public.tmp_regularizacion (nro_adjudicatario, estado) VALUES (500, 'SIN REGULARIZACION');
        INSERT INTO public.uf (id, id_parcela, uf, tipo, nro_adjudicatario, tipo_id_adjudicatario, geom) VALUES
            (1, 1, '1', 1, 30111222, 'DNI', 'SRID=22175;POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))'),
            (2, 1, '2', 1, 500, NULL, 'SRID=22175;POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))'),
            (3, 1, '3', 1, 777, NULL, 'SRID=22175;POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))');
        INSERT INTO public.tipo_ejecutor (id, nombre) VALUES (1, 'Empresa');
        INSERT INTO public.ejecutor (id, tipo, cuit, nombre) VALUES (1, 1, '11111111111', 'Constructora');
        INSERT INTO public.intervencion_ejecutor (id, id_intervencion, id_ejecutor) VALUES (1, 1, 1), (2, 1, 1);
        INSERT INTO our.tipo_pregunta (id, nombre, tipo) VALUES (9, 'Múltiple', 'integer[]');
        INSERT INTO our.relevamiento (id, nombre, objetivo) VALUES (1, 'Relevamiento', 10);
        INSERT INTO our.seccion (id, relevamiento, nombre, orden) VALUES (1, 1, 'Sección', 1);
        INSERT INTO our.pregunta (id, tipo, texto) VALUES (1, 9, '¿Qué modificaciones?');
        INSERT INTO our.pregunta_relevamiento (id, relevamiento, seccion, pregunta, variable, visible) VALUES
            (1, 1, 1, 1, 'modificaciones', '||(e) => v(e,''modificaciones'',1)||');
        INSERT INTO our.vivienda (id, relevamiento, vivienda, geom, properties) VALUES
            (1, 1, 2, 'SRID=3857;MULTIPOLYGON(((0 0, 0 10, 10 10, 10 0, 0 0)))', '{"grupo": "8", "relevado": false}');
        INSERT INTO our.encuesta (id, relevamiento, vivienda, "user", tstamp, tipo) VALUES (1, 1, 2, 'nadie', '2024-05-01 10:00', 1);
        INSERT INTO our.respuesta_encuesta (id, encuesta, pregunta, valor) VALUES (1, 1, 1, '1');
        INSERT INTO visualizador.rolegroup (id, nombre, descripcion) VALUES (1, 'Capas', '-');
        INSERT INTO visualizador.role (id, nombre, descripcion, "group") VALUES (1, 'barrios-ver', '-', 1), (2, 'admin-user', '-', 1);
        INSERT INTO visualizador."user" (id, nombre, username, password, activo) VALUES (1, 'Ana', 'ana.gdu', 'x', true);
        INSERT INTO visualizador.rolemapping ("user", role) VALUES (1, 1), (1, 2);
        INSERT INTO audit.audit_logs (id, tstamp, user_id, username, action) VALUES (1, '2024-05-01 10:00', 1, 'ana.gdu', 'login');
    """

    @classmethod
    def setUpTestData(cls):
        from pathlib import Path

        from django.db import connection

        departamento = Departamento.objects.create(id=22007, departamento_nombre="Almirante Brown")
        municipio = Municipio.objects.create(id=1, municipio_nombre="Bermejo", municipio_departamento=departamento)
        Localidad.objects.create(
            id=22007010, localidad_nombre="Concepción del Bermejo", localidad_departamento=departamento,
            localidad_municipio=municipio,
        )
        esquema = (Path(__file__).parent / "etl" / "fixtures" / "legacy_schema.sql").read_text()
        with connection.cursor() as cur:
            cur.execute(esquema)
            cur.execute(cls.DATOS_LEGACY)

    def correr_etl(self, **kwargs):
        from django.db import connection

        from gdu.etl.importador import Importador

        connection.ensure_connection()
        return Importador(conexion=connection.connection, log=lambda *a: None).ejecutar(**kwargs)

    def incidencias(self, reporte, tabla):
        return {(tipo, motivo) for t, _, tipo, motivo, _ in reporte.filas if t == tabla}

    def test_carga_y_conciliacion(self):
        reporte = self.correr_etl()

        intervencion = Intervencion.objects.get()
        self.assertEqual((intervencion.localidad_id, intervencion.estado, intervencion.grupo), (22007010, "terminada", "8"))
        self.assertEqual(Programa.objects.get().origen, Programa.Origen.NACIONAL)
        self.assertIn(("descarte", "localidad sin equivalente en carga"), self.incidencias(reporte, "gdu_intervencion"))
        self.assertIn(("descarte", "intervencion no cargado"), self.incidencias(reporte, "gdu_barrio"))
        self.assertIn(("advertencia", "geometría inválida (ST_IsValid)"), self.incidencias(reporte, "gdu_barrio"))
        self.assertIn(("advertencia", "CUIT inválido"), self.incidencias(reporte, "gdu_ejecutor"))
        self.assertEqual(IntervencionEjecutor.objects.count(), 1)

        # misma nomenclatura que el trigger heredado (sin el relleno de los char(n))
        self.assertEqual(Parcela.objects.get().nomenclatura, "12220B0028000000000006" "00009")

        ufs = {u.uf: (u.dni, u.adjudicatario_id, u.nro_adjudicatario_legacy) for u in Uf.objects.all()}
        self.assertEqual(ufs, {"1": (30111222, None, None), "2": (None, 500, None), "3": (None, None, 777)})
        adjudicatario = Adjudicatario3450.objects.get()
        self.assertEqual(
            (adjudicatario.escritura, adjudicatario.matricula, adjudicatario.estado_regularizacion),
            (True, "123", "SIN REGULARIZACION"),
        )

        vivienda = ViviendaRelevamiento.objects.get()
        self.assertEqual((vivienda.uf_id, vivienda.datos, vivienda.geom.srid), (2, {"grupo": "8"}, SRID_GDU))
        encuesta = Encuesta.objects.get()
        self.assertEqual((encuesta.usuario_id, encuesta.usuario_legacy), (None, "nadie"))
        self.assertEqual(
            PreguntaRelevamiento.objects.get().regla_visible, {"in": [1, {"var": "modificaciones"}]},
        )

        usuario = get_user_model().objects.get(username="ana.gdu")
        self.assertFalse(usuario.has_usable_password())
        # los usuarios del visor también quedan como lectores del proyecto QGIS
        self.assertEqual(
            sorted(usuario.groups.values_list("name", flat=True)), ["GDU: Lectores QGIS", "GDU: barrios-ver"],
        )
        self.assertTrue(usuario.has_perm("gdu.ver_barrios"))
        self.assertEqual(EventoVisor.objects.get().usuario, usuario)

        # secuencias reseteadas: el próximo alta no choca con las PKs heredadas
        nueva = Uf.objects.create(parcela_id=1, uf="4", geom=CUADRADO)
        self.assertEqual(nueva.pk, 4)

    def test_editores_qgis_salen_del_mapeo_de_grants(self):
        from unittest import mock

        from gdu.etl.importador import Importador

        leer = Importador._leer_csv
        mapeo = {"ANA.GDU": "editor", "fantasma": "editor"}
        with mock.patch.object(
            Importador, "_leer_csv",
            side_effect=lambda nombre, clave, valor: mapeo if nombre == "usuarios_qgis.csv" else leer(nombre, clave, valor),
        ):
            reporte = self.correr_etl()
        usuario = get_user_model().objects.get(username="ana.gdu")
        self.assertTrue(usuario.groups.filter(name="GDU: Editores QGIS").exists())
        self.assertTrue(usuario.has_perm("gdu.add_barrio"))
        # sin cuenta en polizador: no se crea, queda en el reporte
        self.assertFalse(get_user_model().objects.filter(username="fantasma").exists())
        self.assertIn(
            ("descarte", "usuario de QGIS sin cuenta en polizador (darlo de alta y correr configurar_grupos_qgis)"),
            self.incidencias(reporte, "auth_user_groups"),
        )

    def test_es_repetible(self):
        primera = self.correr_etl()
        segunda = self.correr_etl()
        conteos = lambda r: {t.destino: (t.leidas, t.cargadas) for t in r.tablas.values()}
        self.assertEqual(conteos(primera), conteos(segunda))
        self.assertEqual(Uf.objects.count(), 3)
        self.assertEqual(get_user_model().objects.filter(username="ana.gdu").count(), 1)

    def test_dry_run_no_deja_cambios(self):
        reporte = self.correr_etl(dry_run=True)
        self.assertEqual(reporte.tablas["gdu_uf"].cargadas, 3)
        self.assertFalse(Uf.objects.exists())


class OapifTest(TestCase):
    """Capas del piloto OAPIF (gdu/oapif.py), como las usa QGIS: Basic Auth, OPTIONS para
    saber qué puede editar, POST con Location, PATCH, DELETE y geometrías en CRS84."""

    BASE = "/gdu/oapif"
    CRS84 = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"

    @classmethod
    def setUpTestData(cls):
        import base64

        from django.contrib.auth.models import Permission

        ModelosGduTest.setUpTestData.__func__(cls)
        User = get_user_model()
        cls.editor = User.objects.create_user("editor", password="clave-editor")
        cls.editor.user_permissions.add(*Permission.objects.filter(
            content_type__app_label="gdu",
            codename__in=["view_barrio", "add_barrio", "change_barrio", "delete_barrio", "view_intervencion"],
        ))
        cls.lector = User.objects.create_user("lector", password="clave-lector")
        cls.lector.user_permissions.add(Permission.objects.get(content_type__app_label="gdu", codename="view_barrio"))
        cls.auth = {
            usuario: "Basic " + base64.b64encode(f"{usuario}:clave-{usuario}".encode()).decode()
            for usuario in ("editor", "lector")
        }

    def pedir(self, metodo, ruta, usuario=None, datos=None, **headers):
        import json

        if usuario:
            headers["HTTP_AUTHORIZATION"] = self.auth[usuario]
        if datos is not None:
            headers.update(data=json.dumps(datos), content_type="application/geo+json")
        return getattr(self.client, metodo)(f"{self.BASE}{ruta}", HTTP_ACCEPT="application/geo+json", **headers)

    def feature_barrio(self, nombre="Barrio nuevo", **propiedades):
        # un cuadrado de ~100 m en Resistencia, en lon/lat (≈ X 5600850, Y 6959288 en EPSG:22175)
        lon, lat, d = -58.9794, -27.4930, 0.001
        return {
            "type": "Feature",
            "properties": {"nombre": nombre, "intervencion": self.intervencion.pk, **propiedades},
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[lon, lat], [lon, lat + d], [lon + d, lat + d], [lon + d, lat], [lon, lat]]]],
            },
        }

    def test_cada_usuario_ve_solo_sus_colecciones_en_crs84(self):
        respuesta = self.pedir("get", "/collections", "lector")
        self.assertEqual(respuesta.status_code, 200)
        colecciones = {c["id"]: c for c in respuesta.json()["collections"]}
        self.assertEqual(set(colecciones), {"barrios"})
        # 22175 no se ofrece: su orden de ejes EPSG es norte, este y django-oapif no lo invierte
        self.assertEqual(colecciones["barrios"]["storageCrs"], self.CRS84)
        self.assertEqual(colecciones["barrios"]["crs"], [self.CRS84])
        epsg = f"http://www.opengis.net/def/crs/EPSG/0/{SRID_GDU}"
        self.assertEqual(self.pedir("get", f"/collections/barrios/items?crs={epsg}", "lector").status_code, 400)
        editor = {c["id"] for c in self.pedir("get", "/collections", "editor").json()["collections"]}
        self.assertEqual(editor, {"barrios", "intervenciones"})

    def test_allow_segun_permisos(self):
        allow = lambda usuario: set(self.pedir("options", "/collections/barrios/items", usuario)["Allow"].split(", "))
        self.assertIn("POST", allow("editor"))
        self.assertNotIn("POST", allow("lector"))
        allow_intervencion = self.pedir("options", "/collections/intervenciones/items", "editor")["Allow"]
        self.assertNotIn("POST", allow_intervencion)

    def test_qgis_puede_cachear_metadatos_pero_no_datos(self):
        # QGIS pide estos metadatos en serie para cada capa al abrir el proyecto (gdu/middleware.py)
        for ruta in ("/", "/openapi.json", "/conformance", "/collections/barrios",
                     "/collections/barrios/queryables", "/collections/barrios/schema"):
            with self.subTest(ruta=ruta):
                respuesta = self.pedir("get", ruta, "lector")
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn("private", respuesta["Cache-Control"])
                self.assertIn("max-age=", respuesta["Cache-Control"])
        # los datos y la lista de colecciones (depende de los permisos) no
        for ruta in ("/collections", "/collections/barrios/items"):
            with self.subTest(ruta=ruta):
                self.assertFalse(self.pedir("get", ruta, "lector").has_header("Cache-Control"))
        # una respuesta de error tampoco
        self.assertFalse(self.pedir("get", "/collections/intervenciones", "lector").has_header("Cache-Control"))

    def test_sin_permiso_no_ve_la_capa(self):
        self.assertIn(self.pedir("get", "/collections/barrios/items").status_code, (401, 403))

    def test_alta_edicion_y_borrado(self):
        alta = self.pedir("post", "/collections/barrios/items", "editor", self.feature_barrio())
        self.assertEqual(alta.status_code, 201, alta.content)
        self.assertIn("/collections/barrios/items/", alta["Location"])
        barrio = Barrio.objects.get(nombre="Barrio nuevo")
        self.assertEqual(barrio.updated_by, self.editor)
        # guardada en 22175 con los ejes en su lugar (X ≈ 5,6 millones, Y ≈ 6,96 millones)
        xmin, ymin, _, _ = barrio.geom.extent
        self.assertAlmostEqual(xmin, 5600850, delta=200)
        self.assertAlmostEqual(ymin, 6959288, delta=200)
        self.assertEqual(barrio.history.get().history_user, self.editor)

        cambio = self.pedir(
            "patch", f"/collections/barrios/items/{barrio.pk}", "editor", {"type": "Feature", "properties": {"nombre": "Renombrado"}},
        )
        self.assertEqual(cambio.status_code, 200, cambio.content)
        self.assertEqual(Barrio.objects.get(pk=barrio.pk).nombre, "Renombrado")

        self.assertEqual(self.pedir("delete", f"/collections/barrios/items/{barrio.pk}", "lector").status_code, 403)
        self.assertEqual(self.pedir("delete", f"/collections/barrios/items/{barrio.pk}", "editor").status_code, 200)
        self.assertFalse(Barrio.objects.filter(pk=barrio.pk).exists())

    def test_validacion_del_modelo_devuelve_422(self):
        feature = self.feature_barrio(nombre="x" * 300)  # max_length=255
        respuesta = self.pedir("post", "/collections/barrios/items", "editor", feature)
        self.assertEqual(respuesta.status_code, 422, respuesta.content)
        # mensaje legible para QGIS, sin repetir el valor enviado
        self.assertEqual(respuesta.json(), {"detail": "nombre: admite como máximo 255 caracteres"})

    def test_borrar_algo_referenciado_devuelve_409(self):
        from django.contrib.auth.models import Permission

        self.editor.user_permissions.add(*Permission.objects.filter(
            content_type__app_label="gdu", codename__in=["view_planomensura", "delete_planomensura"],
        ))
        plano = PlanoMensura.objects.create(depto="09", nro=78, ano="11")
        PlanoMensuraIntervencion.objects.create(plano=plano, intervencion=self.intervencion, tipo="perimetral")
        # el borrado en cascada de PlanoMensuraIntervencion no protege; uno PROTECT sí
        PreAdjudicatarioDispersa.objects.create(apellido="A", nombre="B", plano_mensura=plano, geom=Point(5, 5, srid=SRID_GDU))
        respuesta = self.pedir("delete", f"/collections/planos_mensura/items/{plano.pk}", "editor")
        self.assertEqual(respuesta.status_code, 409, respuesta.content)
        self.assertIn("No se puede borrar", respuesta.json()["detail"])

    def test_options_unknown_id_para_colecciones_vacias(self):
        # QGIS pregunta así los permisos de edición cuando la capa no tiene features
        allow = lambda usuario: set(self.pedir("options", "/collections/barrios/items/unknown_id", usuario)["Allow"].split(", "))
        self.assertTrue({"PUT", "PATCH", "DELETE"} <= allow("editor"))
        self.assertEqual(allow("lector"), {"OPTIONS", "GET"})
        self.assertEqual(self.pedir("get", "/collections/barrios/items/no-numerico", "editor").status_code, 404)

    def test_alta_como_la_manda_qgis(self):
        # QGIS manda todos los campos de la capa: id y los de solo lectura en null
        feature = self.feature_barrio(id=None, updated_at=None, updated_by=None)
        alta = self.pedir("post", "/collections/barrios/items", "editor", feature)
        self.assertEqual(alta.status_code, 201, alta.content)
        schema = self.client.get(f"{self.BASE}/collections/barrios/schema", HTTP_AUTHORIZATION=self.auth["editor"],
                                 HTTP_ACCEPT="application/schema+json").json()
        self.assertTrue(schema["properties"]["id"].get("readOnly"))
        self.assertFalse({"id", "updated_at", "updated_by"} & set(schema.get("required", [])))

    def test_texto_vacio_en_null_no_da_500(self):
        from django.contrib.auth.models import Permission

        self.editor.user_permissions.add(*Permission.objects.filter(
            content_type__app_label="gdu", codename__in=["view_planomensura", "add_planomensura"],
        ))
        feature = {
            "type": "Feature", "geometry": None,
            "properties": {"depto": "99", "nro": 1, "ano": "26", "pm_antecedente": None, "en_gdu": None},
        }
        alta = self.pedir("post", "/collections/planos_mensura/items", "editor", feature)
        self.assertEqual(alta.status_code, 201, alta.content)
        self.assertEqual(PlanoMensura.objects.get(depto="99").pm_antecedente, "")

    def test_lector_recibe_403_aunque_el_cuerpo_sea_invalido(self):
        respuesta = self.pedir("post", "/collections/barrios/items", "lector", self.feature_barrio(nombre="x" * 300))
        self.assertEqual(respuesta.status_code, 403)

    def test_mensaje_de_unicidad_sin_prefijo_interno_y_sin_escapar(self):
        from django.contrib.auth.models import Permission

        self.editor.user_permissions.add(*Permission.objects.filter(
            content_type__app_label="gdu", codename__in=["view_planomensuraintervencion", "add_planomensuraintervencion"],
        ))
        plano = PlanoMensura.objects.create(depto="09", nro=78, ano="11")
        PlanoMensuraIntervencion.objects.create(plano=plano, intervencion=self.intervencion, tipo="perimetral")
        feature = {
            "type": "Feature", "geometry": None,
            "properties": {"plano": plano.pk, "intervencion": self.intervencion.pk, "tipo": "perimetral"},
        }
        respuesta = self.pedir("post", "/collections/planos_mensura_intervencion/items", "editor", feature)
        self.assertEqual(respuesta.status_code, 422)
        cuerpo = respuesta.content.decode()
        self.assertIn("Plano de intervención", cuerpo)  # sin \u00f3
        self.assertNotIn("__all__", cuerpo)


class OapifColeccionesTest(OapifTest):
    """Fase 4: todas las capas del proyecto QGIS publicadas, con los grupos de permisos que
    arma configurar_grupos_qgis."""

    # un punto de Resistencia (el mismo de feature_barrio), en EPSG:22175
    RESISTENCIA = Polygon(((5600800, 6959250), (5600800, 6959300), (5600850, 6959300), (5600850, 6959250),
                           (5600800, 6959250)), srid=SRID_GDU)

    @classmethod
    def setUpTestData(cls):
        from django.core.management import call_command

        super().setUpTestData()
        User = get_user_model()
        cls.editor_qgis = User.objects.create_user("editor_qgis", password="clave-editor_qgis")
        cls.lector_qgis = User.objects.create_user("lector_qgis", password="clave-lector_qgis")
        call_command("configurar_grupos_qgis", editores=["editor_qgis"], lectores=["lector_qgis"], stdout=StringIO())
        cls.auth.update({
            usuario: "Basic " + base64.b64encode(f"{usuario}:clave-{usuario}".encode()).decode()
            for usuario in ("editor_qgis", "lector_qgis")
        })

    def ids(self, ruta, usuario):
        respuesta = self.pedir("get", ruta, usuario)
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        return {int(f["id"]) for f in respuesta.json()["features"]}

    def test_los_grupos_ven_todas_las_colecciones(self):
        from gdu.oapif import api

        for usuario in ("editor_qgis", "lector_qgis"):
            visibles = {c["id"] for c in self.pedir("get", "/collections", usuario).json()["collections"]}
            self.assertEqual(visibles, set(api.collections), usuario)

    def test_el_lector_no_edita_y_las_de_referencia_no_se_editan(self):
        allow = lambda coleccion, usuario: set(
            self.pedir("options", f"/collections/{coleccion}/items", usuario)["Allow"].split(", ")
        )
        self.assertIn("POST", allow("tierras", "editor_qgis"))
        self.assertNotIn("POST", allow("tierras", "lector_qgis"))
        for coleccion in ("catastro_urbano", "localidades", "adjudicatarios_3450", "viviendas_para_escriturar"):
            self.assertNotIn("POST", allow(coleccion, "editor_qgis"), coleccion)

    def test_configurar_grupos_es_repetible(self):
        from django.contrib.auth.models import Group
        from django.core.management import call_command

        antes = Group.objects.get(name="GDU: Editores QGIS").permissions.count()
        call_command("configurar_grupos_qgis", stdout=StringIO())
        self.assertEqual(Group.objects.get(name="GDU: Editores QGIS").permissions.count(), antes)
        self.assertTrue(self.editor_qgis.groups.filter(name="GDU: Editores QGIS").exists())

    def test_zonas_de_parcelas(self):
        from gdu.oapif import ZONAS_PARCELAS, api

        self.assertEqual(len(ZONAS_PARCELAS), 29)
        for zona in ZONAS_PARCELAS:
            self.assertTrue(api.collections[zona["id"]].zona.valid, zona["id"])
        parcela = Parcela.objects.create(
            intervencion=self.intervencion, destino=self.destino, geom=self.RESISTENCIA, **NOMENCLATURA,
        )
        con_la_parcela = {
            zona["id"] for zona in ZONAS_PARCELAS
            if parcela.pk in self.ids(f"/collections/{zona['id']}/items", "lector_qgis")
        }
        self.assertTrue(con_la_parcela)
        self.assertTrue(all(z.startswith("parcelas_resistencia_") for z in con_la_parcela), con_la_parcela)
        self.assertIn(parcela.pk, self.ids("/collections/parcelas/items", "lector_qgis"))
        # se edita desde la capa de su zona
        zona = sorted(con_la_parcela)[0]
        cambio = self.pedir("patch", f"/collections/{zona}/items/{parcela.pk}", "editor_qgis",
                            {"type": "Feature", "properties": {"estado_dominial": "ipduv"}})
        self.assertEqual(cambio.status_code, 200, cambio.content)
        self.assertEqual(self.pedir("get", f"/collections/parcelas_dpto_01/items/{parcela.pk}", "editor_qgis").status_code, 404)

    def test_permisos_por_campo_de_las_uf(self):
        from django.contrib.auth.models import Permission

        solo_lectura = lambda usuario: {
            campo for campo, p in self.client.get(
                f"{self.BASE}/collections/ufs/schema", HTTP_AUTHORIZATION=self.auth[usuario],
                HTTP_ACCEPT="application/schema+json",
            ).json()["properties"].items() if p.get("readOnly")
        }
        self.assertFalse({"estado_dominial", "dni", "adjudicatario"} & solo_lectura("editor_qgis"))
        self.editor.user_permissions.add(*Permission.objects.filter(content_type__app_label="gdu", codename__in=["view_uf", "change_uf"]))
        self.assertTrue({"estado_dominial", "dni", "adjudicatario"} <= solo_lectura("editor"))

    def test_viviendas_filtradas(self):
        parcela = Parcela.objects.create(intervencion=self.intervencion, destino=self.destino, geom=CUADRADO, **NOMENCLATURA)
        Adjudicatario3450.objects.create(nro_adjudicatario=1, escritura=False)
        Adjudicatario3450.objects.create(nro_adjudicatario=2, escritura=True)
        sin_escritura = Uf.objects.create(parcela=parcela, uf="1", geom=CUADRADO, adjudicatario_id=1)
        Uf.objects.create(parcela=parcela, uf="2", geom=CUADRADO, adjudicatario_id=2)
        sin_adjudicatario = Uf.objects.create(parcela=parcela, uf="3", geom=CUADRADO)
        self.assertEqual(self.ids("/collections/viviendas_para_escriturar/items", "lector_qgis"), {sin_escritura.pk})
        # la intervención del fixture no tiene plan
        self.assertEqual(len(self.ids("/collections/viviendas_sin_plan_grupo/items", "lector_qgis")), 3)
        Intervencion.objects.filter(pk=self.intervencion.pk).update(plan=12, grupo="8A")
        self.assertEqual(
            self.ids("/collections/viviendas_con_plan_grupo_sin_adjudicatario/items", "lector_qgis"),
            {sin_adjudicatario.pk},
        )

    def test_schema_trae_las_etiquetas_de_las_choices(self):
        schema = self.client.get(f"{self.BASE}/collections/tierras/schema", HTTP_AUTHORIZATION=self.auth["lector_qgis"],
                                 HTTP_ACCEPT="application/schema+json").json()
        self.assertEqual(schema["properties"]["superficie"]["x-gdu-etiquetas"]["500+"], "Más de 500 m²")

    def test_el_proyecto_qgis_usa_colecciones_existentes(self):
        import re
        import zipfile
        from pathlib import Path

        from gdu.oapif import api

        qgz = Path(__file__).resolve().parents[2] / "qgis-gdu" / "oapif" / "gdu-oapif.qgz"
        if not qgz.exists():
            self.skipTest("todavía no se generó qgis-gdu/oapif/gdu-oapif.qgz")
        with zipfile.ZipFile(qgz) as archivo:
            qgs = archivo.read(next(n for n in archivo.namelist() if n.endswith(".qgs"))).decode()
        usadas = set(re.findall(r"typename='([^']+)'", qgs))
        self.assertTrue(usadas)
        self.assertEqual(usadas - set(api.collections), set())
        # y al revés: una colección nueva en el servidor pide regenerar el proyecto
        # (qgis-gdu/oapif/armar_proyecto.py, ver su README)
        self.assertEqual(set(api.collections) - usadas, set(), "regenerar qgis-gdu/oapif/gdu-oapif.qgz")

    def test_nomenclatura_incompleta_se_sirve_como_null(self):
        # daba 500: el schema la declaraba texto no nulo (viviendas_punto, pre_adjudicatarios_dispersa)
        vivienda = ViviendaPunto.objects.create(
            intervencion=self.intervencion, estado_dominial="ipduv", geom=Point(5, 5, srid=SRID_GDU),
            **{**NOMENCLATURA, "parc": None},
        )
        respuesta = self.pedir("get", "/collections/viviendas_punto/items", "lector_qgis")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        feature = next(f for f in respuesta.json()["features"] if int(f["id"]) == vivienda.pk)
        self.assertIsNone(feature["properties"]["nomenclatura"])

    def test_basic_auth_se_verifica_una_vez(self):
        from unittest import mock

        from django.core.cache import cache

        cache.clear()
        with mock.patch("gdu.oapif.authenticate", wraps=authenticate) as verificar:
            for _ in range(3):
                self.assertEqual(self.pedir("get", "/collections/barrios/items", "lector_qgis").status_code, 200)
            self.assertEqual(verificar.call_count, 1)
            # otra clave para el mismo usuario no usa lo recordado
            otra = "Basic " + base64.b64encode(b"lector_qgis:otra-clave").decode()
            respuesta = self.client.get(f"{self.BASE}/collections/barrios/items", HTTP_AUTHORIZATION=otra,
                                        HTTP_ACCEPT="application/geo+json")
            self.assertIn(respuesta.status_code, (401, 403))
            self.assertEqual(verificar.call_count, 2)
        # dado de baja: no entra aunque el par esté recordado
        get_user_model().objects.filter(pk=self.lector_qgis.pk).update(is_active=False)
        self.assertIn(self.pedir("get", "/collections/barrios/items", "lector_qgis").status_code, (401, 403))

    def test_mensaje_de_unicidad_con_tildes(self):
        ejecutor = Ejecutor.objects.create(
            tipo=TipoEjecutor.objects.create(nombre="Empresa"), cuit="20123456786", nombre="Constructora",
        )
        IntervencionEjecutor.objects.create(intervencion=self.intervencion, ejecutor=ejecutor)
        feature = {"type": "Feature", "geometry": None,
                   "properties": {"intervencion": self.intervencion.pk, "ejecutor": ejecutor.pk}}
        respuesta = self.pedir("post", "/collections/intervenciones_ejecutores/items", "editor_qgis", feature)
        self.assertEqual(respuesta.status_code, 422)
        self.assertIn("Intervención y Ejecutor", respuesta.json()["detail"])

    def test_uf_trae_la_nomenclatura_de_su_parcela(self):
        parcela = Parcela.objects.create(intervencion=self.intervencion, destino=self.destino, geom=CUADRADO, **NOMENCLATURA)
        uf = Uf.objects.create(parcela=parcela, uf="011", geom=CUADRADO)
        parcela.refresh_from_db()
        for coleccion in ("ufs", "viviendas_sin_plan_grupo"):
            respuesta = self.pedir("get", f"/collections/{coleccion}/items/{uf.pk}", "editor_qgis")
            self.assertEqual(respuesta.status_code, 200, respuesta.content)
            self.assertEqual(respuesta.json()["properties"]["parcela_nomenclatura"], parcela.nomenclatura)
        schema = self.client.get(f"{self.BASE}/collections/ufs/schema", HTTP_AUTHORIZATION=self.auth["editor_qgis"],
                                 HTTP_ACCEPT="application/schema+json").json()
        self.assertTrue(schema["properties"]["parcela_nomenclatura"]["readOnly"])
        # QGIS la manda de vuelta al modificar
        cambio = self.pedir("put", f"/collections/ufs/items/{uf.pk}", "editor_qgis", {
            "type": "Feature",
            "properties": {"parcela": parcela.pk, "uf": "012", "parcela_nomenclatura": "otra cosa"},
            "geometry": {"type": "Polygon", "coordinates": [[[-58.98, -27.49], [-58.98, -27.4899], [-58.9799, -27.4899], [-58.98, -27.49]]]},
        })
        self.assertEqual(cambio.status_code, 200, cambio.content)
        self.assertEqual(cambio.json()["properties"]["parcela_nomenclatura"], parcela.nomenclatura)
        self.assertEqual(Uf.objects.get(pk=uf.pk).uf, "012")


class VisorYFichaTest(TestCase):
    """Visor, ficha imprimible y ediciones del visor sobre los modelos de gdu (fase 5: antes
    leían las vistas SQL visualizador.* del piloto)."""

    # ~50 m en Resistencia, en EPSG:22175
    GEOM = Polygon(((5600800, 6959250), (5600800, 6959300), (5600850, 6959300), (5600850, 6959250),
                    (5600800, 6959250)), srid=SRID_GDU)

    @classmethod
    def setUpTestData(cls):
        from gdu.models import (
            AdjudicacionBeneficiario, Catastrourbano, EstadoGestionExpropiacion, Expropiacion, ObjetoExpropiacion,
            ParcelaExpropiada, ResolucionCostos,
        )

        ModelosGduTest.setUpTestData.__func__(cls)
        Intervencion.objects.filter(pk=cls.intervencion.pk).update(
            plan=12, grupo="8A",
            adjudicacion=AdjudicacionBeneficiario.objects.create(nro="45", ano=2010, tipo="definitiva"),
        )
        cls.plano = PlanoMensura.objects.create(depto="20", nro=107, ano="86", en_gdu=True, geom=cls.GEOM)
        PlanoMensuraIntervencion.objects.create(plano=cls.plano, intervencion=cls.intervencion, tipo="subdivision")
        cls.parcela = Parcela.objects.create(intervencion=cls.intervencion, destino=cls.destino, geom=cls.GEOM, **NOMENCLATURA)
        cls.uf = Uf.objects.create(parcela=cls.parcela, uf="1", poligono="00-01", geom=cls.GEOM, adjudicatario_id=12345,
                                   estado_dominial="adjudicatario", res_costos=ResolucionCostos.objects.create(
                                       nro_largo=100, nro_corto=1, ano=2010, tipo="provisoria"))
        Adjudicatario3450.objects.create(nro_adjudicatario=12345, escritura=False)
        cls.barrio = Barrio.objects.create(intervencion=cls.intervencion, nombre="Barrio Norte", geom=MultiPolygon(cls.GEOM))
        cls.dispersa = ViviendaPunto.objects.create(
            intervencion=cls.intervencion, estado_dominial="ipduv", geom=Point(5600825, 6959275, srid=SRID_GDU),
        )
        expropiacion = Expropiacion.objects.create(
            nro_ley=1234, letra_ley="A", ano_ley=1999, localidad_id=1, asentamiento=False, gestion="ipduv",
        )
        cls.expropiada = ParcelaExpropiada.objects.create(
            expropiacion=expropiacion, objeto=ObjetoExpropiacion.objects.create(nombre="Vivienda"),
            estado_gestion=EstadoGestionExpropiacion.objects.create(nombre="Iniciada"),
            propietario_expropiado="Juan Pérez", geom=cls.GEOM, **NOMENCLATURA,
        )
        cls.catastro = Catastrourbano.objects.create(id_nomencl="01-II-A", municipio="RESISTENCIA", anio=1998, geom=cls.GEOM)
        cls.objetos = {
            "viviendas": cls.uf, "barrios": cls.barrio, "expropiaciones": cls.expropiada,
            "viviendas-dispersas": cls.dispersa, "planos-mensura": cls.plano, "catastro-urbano": cls.catastro,
            "para-escriturar": cls.uf,
        }

    def setUp(self):
        from unittest import mock

        # la ficha consulta la API del Sistema 3450 en vivo
        patcher = mock.patch("gdu.views.ficha.api3450.consultar", return_value={"SDTDatosAdjuGIS": {}})
        patcher.start()
        self.addCleanup(patcher.stop)

    def login(self, *codenames, username="visor"):
        from django.contrib.auth.models import Permission

        usuario = get_user_model().objects.create_user(username, password="x")
        usuario.user_permissions.add(*Permission.objects.filter(content_type__app_label="gdu", codename__in=codenames))
        self.client.force_login(usuario)
        return usuario

    def todas(self):
        from gdu.capas import CAPAS

        return self.login(*(c.permiso.split(".")[1] for c in CAPAS.values()))

    def bbox(self):
        # bbox de Resistencia en EPSG:3857, como lo manda OpenLayers
        return "-6566000,-3186000,-6565000,-3184000"

    def test_cada_capa_dibuja_y_detalla_sus_elementos(self):
        self.todas()
        for capa, obj in self.objetos.items():
            with self.subTest(capa=capa):
                url = reverse_lazy_capa(capa)
                geojson = self.client.get(url, {"bbox": "-6600000,-3200000,-6500000,-3100000"})
                self.assertEqual(geojson.status_code, 200)
                self.assertIn(obj.pk, [f["id"] for f in geojson.json()["features"]])
                detalle = self.client.get(f"/gdu/mapa/{capa}/detalle.json", {"ids": str(obj.pk)})
                self.assertEqual(detalle.status_code, 200, detalle.content)
                self.assertIn(str(obj.pk), detalle.json())

    def test_detalle_de_vivienda_como_la_vista_heredada(self):
        self.todas()
        datos = self.client.get("/gdu/mapa/viviendas/detalle.json", {"ids": str(self.uf.pk)}).json()[str(self.uf.pk)]
        self.assertEqual(datos["uf"], "00-01")  # la vista heredada mostraba el polígono
        self.assertEqual(datos["obra"], "40 viviendas")
        self.assertEqual(datos["localidad"], "Resistencia")
        self.assertEqual(datos["adjudicacion"], "45/2010 - definitiva")
        self.assertEqual(datos["planos"], "20-107-86/subdivision")
        self.assertEqual(datos["nro_adjudicatario"], 12345)

    def test_busqueda_avanzada(self):
        self.todas()
        url = reverse_lazy_capa("viviendas")
        con = self.client.get(url, {"bbox": "-6600000,-3200000,-6500000,-3100000", "programa": "Programa", "grupo": "8A"})
        self.assertEqual(len(con.json()["features"]), 1)
        sin = self.client.get(url, {"bbox": "-6600000,-3200000,-6500000,-3100000", "programa": "Otro"})
        self.assertEqual(sin.json()["features"], [])
        ley = self.client.get(reverse_lazy_capa("expropiaciones"), {"bbox": "-6600000,-3200000,-6500000,-3100000", "ley": "1234A/1999"})
        self.assertEqual(len(ley.json()["features"]), 1)
        opciones = self.client.get("/gdu/mapa/opciones-busqueda.json").json()
        self.assertEqual(opciones["grupos"], ["8A"])
        self.assertEqual(opciones["leyes"], ["1234A/1999"])
        self.assertEqual(opciones["estados_gestion"], ["ipduv", "externa"])

    def test_buscar_localidad_usa_las_de_carga(self):
        Localidad.objects.filter(pk=1).update(localidad_centroide_lat=-27.45, localidad_centroide_lon=-58.98)
        self.todas()
        resultados = self.client.get("/gdu/mapa/buscar-localidad.json", {"q": "resis"}).json()["results"]
        self.assertEqual(resultados[0]["text"], "Resistencia, San Fernando")
        self.assertEqual(resultados[0]["lat"], -27.45)

    def test_ficha_de_cada_capa(self):
        self.todas()
        esperado = {
            "viviendas": ["00-01", "Nº adjudicatario", "12345", "Adjudicatario"],
            "barrios": ["Barrio Norte", "Programa"],
            "expropiaciones": ["1234A/1999", "Juan Pérez", "Iniciada"],
            "viviendas-dispersas": ["40 viviendas", "Resistencia"],
            "planos-mensura": ["20-107-86", "En GDU", "Sí"],
            "catastro-urbano": ["Matrícula", "RESISTENCIA", "1998"],
            "para-escriturar": ["00-01"],
        }
        for capa, textos in esperado.items():
            with self.subTest(capa=capa):
                respuesta = self.client.get(f"/gdu/ficha/{capa}/{self.objetos[capa].pk}/")
                self.assertEqual(respuesta.status_code, 200)
                for texto in textos:
                    self.assertContains(respuesta, texto)
                self.assertIn(respuesta.context["config_mapa"]["geometria"]["type"], ("Polygon", "MultiPolygon", "Point"))

    def test_ficha_registra_el_evento_y_respeta_permisos(self):
        usuario = self.login("ver_viviendas", "ver_catastro_urbano")
        respuesta = self.client.get(f"/gdu/ficha/viviendas/{self.uf.pk}/")
        capas = [c["capa"] for c in respuesta.context["config_mapa"]["capasContexto"]]
        self.assertEqual(capas, ["viviendas", "catastro-urbano"])
        evento = EventoVisor.objects.get(accion="printFeature")
        self.assertEqual((evento.usuario, evento.metadata), (usuario, {"layer": "viviendas", "id": self.uf.pk}))
        self.assertEqual(self.client.get(f"/gdu/ficha/barrios/{self.barrio.pk}/").status_code, 403)
        self.assertEqual(self.client.get(f"/gdu/ficha/parcelas/{self.parcela.pk}/").status_code, 404)
        self.assertEqual(self.client.get("/gdu/ficha/viviendas/999999/").status_code, 404)

    def test_editar_nro_adjudicatario_queda_en_el_historial(self):
        usuario = self.login("editar_nro_adjudicatario")
        respuesta = self.client.post(f"/gdu/uf/{self.uf.pk}/nro-adjudicatario/", {"nro_adjudicatario": "777"})
        self.assertEqual(respuesta.json(), {"id": self.uf.pk, "nro_adjudicatario": 777})
        uf = Uf.objects.get(pk=self.uf.pk)
        self.assertEqual((uf.adjudicatario_id, uf.updated_by), (777, usuario))
        self.assertEqual(uf.history.first().history_user, usuario)
        self.assertEqual(self.client.post(f"/gdu/uf/{self.uf.pk}/nro-adjudicatario/", {"nro_adjudicatario": "x"}).status_code, 400)
        self.assertEqual(self.client.post("/gdu/uf/999999/nro-adjudicatario/", {"nro_adjudicatario": "1"}).status_code, 404)

    def test_descarga_del_proyecto_qgis_con_la_url_del_servidor(self):
        import io
        import tempfile
        import zipfile
        from pathlib import Path

        from django.test import override_settings

        qgs = "<qgis><datasource>url='http://192.168.0.51:8000/gdu/oapif/' typename='barrios' authcfg='gduoapf'</datasource></qgis>"
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "gdu-oapif.qgz"
            with zipfile.ZipFile(archivo, "w") as z:
                z.writestr("gdu-oapif.qgs", qgs)
                z.writestr("gdu-oapif.qgd", b"\x00")
            with override_settings(GDU_QGIS_PROYECTO=archivo, ALLOWED_HOSTS=["testserver", "polizador.ipduv.gob.ar"]):
                self.login(username="sin-capas")
                self.assertEqual(self.client.get("/gdu/mapa/qgis/descargar/").status_code, 403)
                self.login("view_barrio")
                respuesta = self.client.get("/gdu/mapa/qgis/descargar/", HTTP_HOST="polizador.ipduv.gob.ar")
                self.assertEqual(respuesta.status_code, 200)
                contenido = b"".join(respuesta.streaming_content)
        with zipfile.ZipFile(io.BytesIO(contenido)) as z:
            self.assertEqual(
                z.read("gdu-oapif.qgs").decode(),
                qgs.replace("http://192.168.0.51:8000/gdu/oapif/", "http://polizador.ipduv.gob.ar/gdu/oapif/"),
            )
            self.assertEqual(z.read("gdu-oapif.qgd"), b"\x00")
        self.assertTrue(EventoVisor.objects.filter(accion="descargaProyectoQgis").exists())

    def test_el_proyecto_versionado_se_puede_reescribir(self):
        import io
        import re
        import zipfile

        from django.conf import settings

        from gdu.views.qgis_project import proyecto_con_url

        if not settings.GDU_QGIS_PROYECTO.exists():
            self.skipTest("no está el .qgz versionado")
        nuevo = proyecto_con_url(settings.GDU_QGIS_PROYECTO.read_bytes(), "https://otro/gdu/oapif/")
        with zipfile.ZipFile(io.BytesIO(nuevo)) as z:
            qgs = z.read(next(n for n in z.namelist() if n.endswith(".qgs"))).decode()
        urls = set(re.findall(r"url='([^']*)'", qgs))
        self.assertEqual(urls - {"https://otro/gdu/oapif/"}, {u for u in urls if "/gdu/oapif/" not in u})

    def test_listados_de_la_api(self):
        usuario = get_user_model().objects.create_superuser("admin-gdu", password="x")
        self.client.force_login(usuario)
        for slug in (
            "gdu-actuaciones", "gdu-contrataciones", "gdu-intervenciones", "gdu-programas",
            "gdu-barrios", "gdu-parcelas", "gdu-ufs", "gdu-localidades", "gdu-expropiaciones", "gdu-planos-mensura",
            "gdu-adjudicaciones-beneficiario", "gdu-resoluciones-costos", "gdu-tipos-contratacion",
            "gdu-tipos-intervencion", "gdu-destinos-parcela", "gdu-estados-gestion-expropiacion", "gdu-adjudicatarios-3450",
        ):
            with self.subTest(slug=slug):
                respuesta = self.client.get(f"/v1/api/datatables/{slug}/")
                self.assertEqual(respuesta.status_code, 200, respuesta.content[:300])
                self.assertGreaterEqual(respuesta.json()["recordsTotal"], 1, slug)
        busqueda = self.client.get("/v1/api/datatables/gdu-adjudicatarios-3450/", {"search": "12345"}).json()
        self.assertEqual([f["nro_adjudicatario"] for f in busqueda["data"]], [12345])
        for nombre in ("lista_actuaciones", "lista_ufs", "lista_localidades", "lista_adjudicatarios_3450"):
            self.assertEqual(self.client.get(reverse(f"gdu:{nombre}")).status_code, 200, nombre)

    def test_adjudicatario_cero_no_es_vacio(self):
        # en el Sistema 3450 el 0 es "crédito desadjudicado"
        Uf.objects.filter(pk=self.uf.pk).update(adjudicatario_id=0)
        self.todas()
        datos = self.client.get("/gdu/mapa/viviendas/detalle.json", {"ids": str(self.uf.pk)}).json()[str(self.uf.pk)]
        self.assertEqual(datos["nro_adjudicatario"], 0)


def reverse_lazy_capa(capa):
    return reverse(f"gdu:geojson_{capa.replace('-', '_')}")


class EncuestaWebTest(TestCase):
    """Formulario web de encuestas: las reglas JsonLogic deciden en el servidor qué se exige y
    qué se guarda (las preguntas ocultas no se guardan)."""

    @classmethod
    def setUpTestData(cls):
        from gdu.models import Pregunta, Respuesta, Seccion, TipoPregunta

        cls.relevamiento = Relevamiento.objects.create(nombre="Fontana", fecha="2024-01-01", objetivo=10)
        seccion = Seccion.objects.create(relevamiento=cls.relevamiento, nombre="Hogar", orden=1)
        numerico = TipoPregunta.objects.create(id=1, nombre="Multiple Choice Numérico", tipo="integer")
        texto = TipoPregunta.objects.create(id=7, nombre="Texto Simple", tipo="string")
        multiple = TipoPregunta.objects.create(id=9, nombre="Múltiple Choice Numérico - Respuesta Múltiple", tipo="integer[]")
        relacion = Pregunta.objects.create(tipo=numerico, texto="Relación con el adjudicatario")
        cls.opciones = {
            n: Respuesta.objects.create(pregunta=relacion, texto=t, nro_opcion=n, valor=str(n))
            for n, t in ((1, "Es el adjudicatario"), (2, "Es familiar"), (3, "Otro"))
        }
        servicios = Pregunta.objects.create(tipo=multiple, texto="Servicios")
        for n, t in ((1, "Agua"), (2, "Luz")):
            Respuesta.objects.create(pregunta=servicios, texto=t, nro_opcion=n, valor=str(n))
        PreguntaRelevamiento.objects.create(
            relevamiento=cls.relevamiento, seccion=seccion, pregunta=relacion, variable="relacion", requerida=True,
        )
        PreguntaRelevamiento.objects.create(
            relevamiento=cls.relevamiento, seccion=seccion, variable="relacion_otro", requerida=True,
            pregunta=Pregunta.objects.create(tipo=texto, texto="¿Cuál?"),
            regla_visible={"==": [{"var": "relacion"}, 3]},
            regla_valido={"!=": [{"var": "relacion_otro"}, "ninguna"]},
        )
        PreguntaRelevamiento.objects.create(
            relevamiento=cls.relevamiento, seccion=seccion, pregunta=servicios, variable="servicios",
        )
        cls.vivienda = ViviendaRelevamiento.objects.create(
            relevamiento=cls.relevamiento, numero=7, geom=MultiPolygon(CUADRADO), datos={"barrio": "Centro"},
        )
        cls.usuario = get_user_model().objects.create_superuser("encuestador", password="x")

    def setUp(self):
        self.client.force_login(self.usuario)
        self.url = f"/gdu/relevamientos/{self.relevamiento.pk}/viviendas/7/encuesta/"

    def test_pregunta_oculta_no_se_exige_ni_se_guarda(self):
        respuesta = self.client.post(self.url, {"relacion": "1", "relacion_otro": "no va", "servicios": ["1", "2"]})
        self.assertEqual(respuesta.status_code, 302, respuesta.context and respuesta.context["form"].errors)
        encuesta = Encuesta.objects.get()
        self.assertEqual((encuesta.vivienda, encuesta.usuario, encuesta.tipo), (self.vivienda, self.usuario, Encuesta.Tipo.WEB))
        guardadas = {(r.pregunta_relevamiento.variable, r.valor) for r in encuesta.respuestas.all()}
        self.assertEqual(guardadas, {("relacion", "1"), ("servicios", "1"), ("servicios", "2")})
        # el valor es el de la opción (lo que comparan las reglas), con la FK a la opción elegida
        self.assertEqual(encuesta.respuestas.get(pregunta_relevamiento__variable="relacion").respuesta, self.opciones[1])
        self.assertEqual(encuesta.respuestas.filter(respuesta__isnull=True).count(), 0)
        self.assertTrue(ViviendaRelevamiento.objects.con_relevado().get(pk=self.vivienda.pk).relevado)

    def test_pregunta_visible_obligatoria_y_regla_de_validez(self):
        sin_respuesta = self.client.post(self.url, {"relacion": "3"})
        self.assertEqual(sin_respuesta.context["form"].errors, {"relacion_otro": ["Este campo es obligatorio."]})
        invalida = self.client.post(self.url, {"relacion": "3", "relacion_otro": "ninguna"})
        self.assertIn("no es válido", invalida.context["form"].errors["relacion_otro"][0])
        self.assertEqual(self.client.post(self.url, {"relacion": "3", "relacion_otro": "vecino"}).status_code, 302)
        self.assertEqual(
            Encuesta.objects.get().respuestas.get(pregunta_relevamiento__variable="relacion_otro").valor, "vecino",
        )

    def test_el_navegador_recibe_la_regla_en_json(self):
        respuesta = self.client.get(self.url)
        self.assertContains(respuesta, 'data-visible-rule="{&quot;==&quot;: [{&quot;var&quot;: &quot;relacion&quot;}, 3]}"')
        self.assertContains(respuesta, "Centro")

    def test_listado_de_viviendas_y_csv(self):
        self.client.post(self.url, {"relacion": "2", "servicios": ["1", "2"]})
        listado = self.client.get(f"/gdu/relevamientos/{self.relevamiento.pk}/viviendas/")
        self.assertEqual([v.relevado for v in listado.context["viviendas"]], [True])
        relevamientos = self.client.get("/gdu/relevamientos/").context["relevamientos"]
        self.assertEqual((relevamientos[0].total_viviendas, relevamientos[0].total_relevadas), (1, 1))
        csv = self.client.post("/gdu/csv/", {"relevamiento": self.relevamiento.pk}).content.decode().splitlines()
        self.assertEqual(csv[0], "vivienda,tipo,fechahora,relacion,relacion_otro,servicios")
        self.assertTrue(csv[1].startswith("7,5,"))
        self.assertTrue(csv[1].endswith(",2,,1;2"))


class Importar3450Test(TestCase):
    def test_alta_y_actualizacion_conservan_el_estado_de_regularizacion(self):
        from gdu.management.commands.importar_3450 import Command

        Adjudicatario3450.objects.create(nro_adjudicatario=1, apellido_nombre="Viejo", estado_regularizacion="En trámite")
        registros = [
            {"AdjuGISNroAdju": 1, "AdjuGISapeynom": "BRITES MERCEDES ", "AdjuGISEscritura": "NO",
             "AdjuGISResFecha": "0000-00-00T00:00:00", "AdjuGISdni": 30111222},
            {"AdjuGISNroAdju": 81357, "AdjuGISapeynom": "NUEVO", "AdjuGISEscritura": "SI", "AdjuGISResFecha": "2015-08-13T00:00:00"},
        ]
        self.assertEqual(Command()._upsert(registros), (2, 0))
        uno = Adjudicatario3450.objects.get(pk=1)
        self.assertEqual(
            (uno.apellido_nombre, uno.escritura, uno.dni, uno.res_fecha, uno.estado_regularizacion),
            ("BRITES MERCEDES", False, 30111222, None, "En trámite"),
        )
        nuevo = Adjudicatario3450.objects.get(pk=81357)
        self.assertEqual((nuevo.escritura, nuevo.res_fecha), (True, date(2015, 8, 13)))

    def test_numero_repetido_en_la_misma_pagina_gana_el_ultimo(self):
        from gdu.management.commands.importar_3450 import Command

        registros = [
            {"AdjuGISNroAdju": 7, "AdjuGISapeynom": "PRIMERO"},
            {"AdjuGISNroAdju": 7, "AdjuGISapeynom": "SEGUNDO"},
        ]
        self.assertEqual(Command()._upsert(registros), (1, 0))
        self.assertEqual(Adjudicatario3450.objects.get(pk=7).apellido_nombre, "SEGUNDO")

    def test_registro_invalido_se_descarta_y_el_resto_se_guarda(self):
        from gdu.management.commands.importar_3450 import Command

        registros = [
            {"AdjuGISNroAdju": 1, "AdjuGISResFecha": "13/08/2015"},
            {"AdjuGISNroAdju": 2, "AdjuGISdni": "no es un número"},
            {"AdjuGISapeynom": "SIN NÚMERO"},
            {"AdjuGISNroAdju": 3, "AdjuGISapeynom": "BUENO"},
        ]
        with self.assertLogs("gdu.management.commands.importar_3450", "WARNING") as logs:
            self.assertEqual(Command()._upsert(registros), (1, 3))
        self.assertEqual(len(logs.records), 3)
        self.assertEqual(list(Adjudicatario3450.objects.values_list("pk", flat=True)), [3])
