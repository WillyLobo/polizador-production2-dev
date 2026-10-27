from django.contrib.auth import get_user_model
from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from django.db import IntegrityError
from django.test import TestCase

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
        self.assertEqual(list(usuario.groups.values_list("name", flat=True)), ["GDU: barrios-ver"])
        self.assertTrue(usuario.has_perm("gdu.ver_barrios"))
        self.assertEqual(EventoVisor.objects.get().usuario, usuario)

        # secuencias reseteadas: el próximo alta no choca con las PKs heredadas
        nueva = Uf.objects.create(parcela_id=1, uf="4", geom=CUADRADO)
        self.assertEqual(nueva.pk, 4)

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
