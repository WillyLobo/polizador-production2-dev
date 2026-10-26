import io
import zipfile
from decimal import Decimal
from unittest import mock

from django.contrib.auth.models import Permission
from django.contrib.gis.geos import Point, Polygon
from django.db import connection
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from gdu.models import (
    Barrios,
    Catastrourbano,
    Expropiaciones,
    PlanoMensura,
    ViviendaDispersa,
    Viviendas,
    ViviendasParaEscriturar,
)

from personalizador.models import CustomUser


class DescargarProyectoQgisTest(TestCase):
    def setUp(self):
        self.url = reverse("gdu:descargar_proyecto_qgis")

    def test_anonimo_redirige_a_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_sin_permiso_de_capas_da_403(self):
        user = CustomUser.objects.create_user(username="sinpermiso", password="x")
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_con_permiso_devuelve_zip_con_qgz_y_forms_reconectados(self):
        username = "jperez"
        user = CustomUser.objects.create_user(username=username, password="x")
        user.user_permissions.add(
            Permission.objects.get(codename="ver_viviendas", content_type__app_label="gdu")
        )
        self.client.force_login(user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Disposition"], f'attachment; filename="gdu_qgis_{username}.zip"')

        paquete = zipfile.ZipFile(io.BytesIO(b"".join(response.streaming_content)))
        nombres = paquete.namelist()
        qgz_nombres = [n for n in nombres if n.endswith(".qgz")]
        self.assertEqual(qgz_nombres, [f"gdu.wfs.{username}.qgz"])
        self.assertTrue(any(n.startswith("forms/") for n in nombres))

        qgz_bytes = paquete.read(qgz_nombres[0])
        qgs_bytes = zipfile.ZipFile(io.BytesIO(qgz_bytes)).read("gdu.qgs")
        qgs_text = qgs_bytes.decode("utf-8")

        self.assertIn(f"username='{username}'", qgs_text)
        self.assertNotIn("password='", qgs_text)

        # Servidor de prueba: el proyecto debe venir podado a las capas piloto
        # (+ sus dependencias de relación) y sin quedar ninguna referencia al
        # host de producción (10.106.16.118), ni siquiera en las copias
        # cacheadas de <Option name="ReferencedLayerDataSource">.
        self.assertLess(qgs_text.count("<maplayer"), 20)
        self.assertNotIn("10.106.16.118", qgs_text)

        # Las capas de soporte (lookups de intervencion) también van a WFS --
        # nada debe quedar conectado directo a Postgres (evita repartir una
        # credencial de Postgres compartida solo para verlas).
        self.assertNotIn("dbname=", qgs_text)
        self.assertIn("typename='gdu:tipo_estado'", qgs_text)
        self.assertIn("typename='gdu:programa'", qgs_text)

    def _login_con_permiso(self, username):
        user = CustomUser.objects.create_user(username=username, password="x")
        user.user_permissions.add(
            Permission.objects.get(codename="ver_viviendas", content_type__app_label="gdu")
        )
        self.client.force_login(user)
        return user

    def test_authcfg_valido_se_usa_en_vez_del_username(self):
        username = "mlopez"
        self._login_con_permiso(username)

        response = self.client.get(self.url, {"authcfg": "a1b2c3d"})

        self.assertEqual(response.status_code, 200)
        paquete = zipfile.ZipFile(io.BytesIO(b"".join(response.streaming_content)))
        qgz_nombre = next(n for n in paquete.namelist() if n.endswith(".qgz"))
        qgs_text = zipfile.ZipFile(io.BytesIO(paquete.read(qgz_nombre))).read("gdu.qgs").decode("utf-8")

        self.assertIn("authcfg=a1b2c3d", qgs_text)
        self.assertNotIn(f"username='{username}'", qgs_text)
        self.assertNotIn("password='", qgs_text)

    def test_authcfg_invalido_da_400(self):
        self._login_con_permiso("nvalido")

        response = self.client.get(self.url, {"authcfg": "no-va!"})

        self.assertEqual(response.status_code, 400)

    def test_ldap_username_se_usa_en_vez_del_username_de_django(self):
        self._login_con_permiso("cuentalocal")

        response = self.client.get(self.url, {"ldap_username": "jperez.red"})

        self.assertEqual(response.status_code, 200)
        paquete = zipfile.ZipFile(io.BytesIO(b"".join(response.streaming_content)))
        qgz_nombre = next(n for n in paquete.namelist() if n.endswith(".qgz"))
        qgs_text = zipfile.ZipFile(io.BytesIO(paquete.read(qgz_nombre))).read("gdu.qgs").decode("utf-8")

        self.assertIn("username='jperez.red'", qgs_text)
        self.assertNotIn("username='cuentalocal'", qgs_text)

    def test_ldap_username_se_ignora_si_hay_authcfg(self):
        self._login_con_permiso("cuentalocal")

        response = self.client.get(self.url, {"ldap_username": "jperez.red", "authcfg": "a1b2c3d"})

        self.assertEqual(response.status_code, 200)
        paquete = zipfile.ZipFile(io.BytesIO(b"".join(response.streaming_content)))
        qgz_nombre = next(n for n in paquete.namelist() if n.endswith(".qgz"))
        qgs_text = zipfile.ZipFile(io.BytesIO(paquete.read(qgz_nombre))).read("gdu.qgs").decode("utf-8")

        self.assertIn("authcfg=a1b2c3d", qgs_text)
        self.assertNotIn("username='jperez.red'", qgs_text)

    def test_ldap_username_invalido_da_400(self):
        self._login_con_permiso("cuentalocal")

        response = self.client.get(self.url, {"ldap_username": "jper ez'"})

        self.assertEqual(response.status_code, 400)


def _cuadrado():
    poligono = Polygon(((-59.0, -27.45), (-58.999, -27.45), (-58.999, -27.449), (-59.0, -27.449), (-59.0, -27.45)))
    poligono.srid = 4326
    return poligono


class FichaTest(TestCase):
    """Las capas son managed=False (tablas/vistas de la base GDU heredada), así que no existen en la
    base de test: se crean acá a partir del modelo, dentro de la transacción de la clase."""

    MODELOS = [Barrios, Catastrourbano, Expropiaciones, PlanoMensura, ViviendaDispersa, Viviendas, ViviendasParaEscriturar]

    @classmethod
    def setUpTestData(cls):
        with connection.cursor() as cursor:
            faltantes = []
            for modelo in cls.MODELOS:
                esquema = modelo._meta.db_table.split(".")[0]  # db_table = '"esquema"."tabla"'
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {esquema}")
                cursor.execute("SELECT to_regclass(%s)", [modelo._meta.db_table])
                if cursor.fetchone()[0] is None:
                    faltantes.append(modelo)
        with connection.schema_editor() as editor:
            for modelo in faltantes:
                editor.create_model(modelo)

        punto = Point(-59.0, -27.45, srid=4326)
        cls.objetos = {
            "viviendas": Viviendas.objects.create(
                id=1, uf="UF-7", obra="25 Viviendas", localidad="Resistencia",
                nro_adjudicatario=12345, estado_dominial="Escriturada", expediente="E1-2020-1", geom=_cuadrado(),
            ),
            "barrios": Barrios.objects.create(id=2, barrio="Barrio Norte", localidad="Resistencia", programa="FONAVI", geom=None),
            "expropiaciones": Expropiaciones.objects.create(
                id=3, ley="Ley 1234", dpto="01", circ="II", secc="A", ch="1", qta="2", fracc="3", mz="4", parc="5",
                propietario_expropiado="Juan Pérez", geom=_cuadrado(),
            ),
            "viviendas-dispersas": ViviendaDispersa.objects.create(id=4, obra="Dispersa 1", localidad="Charata", geom=punto),
            "planos-mensura": PlanoMensura.objects.create(
                depto="01", nro=99, ano="20", en_gdu=True, sup_parcelas=Decimal("1500.50"), geom=_cuadrado(),
            ),
            "catastro-urbano": Catastrourbano.objects.create(id_nomencl="01-II-A", municipio="Resistencia", anio=1998, geom=_cuadrado()),
            "para-escriturar": ViviendasParaEscriturar.objects.create(id=7, uf="UF-9", localidad="Fontana", geom=_cuadrado()),
        }

    def setUp(self):
        # catastro.contratacion (al que apunta ObraContratacion) tampoco es de Django: las obras
        # vinculadas se resuelven aparte, ver test_obras_vinculadas_por_expediente
        patcher = mock.patch("gdu.views.ficha._obras_por_expediente", return_value={})
        patcher.start()
        self.addCleanup(patcher.stop)

    def _login(self, *codenames):
        user = CustomUser.objects.create_user(username="fichero", password="x")
        user.user_permissions.add(*Permission.objects.filter(codename__in=codenames, content_type__app_label="gdu"))
        self.client.force_login(user)
        return user

    def _url(self, capa, objeto_id):
        return reverse("gdu:ficha", kwargs={"capa": capa, "objeto_id": objeto_id})

    def test_anonimo_redirige_a_login(self):
        response = self.client.get(self._url("viviendas", 1))
        self.assertEqual(response.status_code, 302)

    def test_cada_capa_muestra_sus_campos(self):
        self._login(
            "ver_viviendas", "ver_barrios", "ver_expropiaciones", "ver_viviendas_dispersas",
            "ver_plano_mensura", "ver_catastro_urbano", "ver_escriturar",
        )
        esperado = {
            "viviendas": ["UF-7", "Nº adjudicatario", "12345", "Estado dominial", "Escriturada"],
            "barrios": ["Barrio Norte", "Programa", "FONAVI", "no tiene geometría"],
            "expropiaciones": ["Nomenclatura", "01-II-A-1-2-3-4-5", "Propietario expropiado", "Juan Pérez"],
            "viviendas-dispersas": ["Dispersa 1", "Charata"],
            "planos-mensura": ["Plano", "01-99-20", "En GDU", "Sí", "1500.50"],
            "catastro-urbano": ["Matrícula", "Municipio", "1998"],
            "para-escriturar": ["UF-9", "Fontana"],
        }
        for capa, textos in esperado.items():
            with self.subTest(capa=capa):
                response = self.client.get(self._url(capa, self.objetos[capa].pk))
                self.assertEqual(response.status_code, 200)
                for texto in textos:
                    self.assertContains(response, texto)
                self.assertNotContains(response, "<dt>id</dt>")
                geometria = response.context["config_mapa"]["geometria"]
                if capa == "barrios":
                    self.assertIsNone(geometria)
                else:
                    self.assertIn(geometria["type"], ("Polygon", "Point"))

    def test_obras_vinculadas_por_expediente(self):
        self._login("ver_viviendas")
        obras = {"E1-2020-1": [{"id": 5, "nombre": "Obra Cinco"}, {"id": 6, "nombre": None}]}
        with mock.patch("gdu.views.ficha._obras_por_expediente", return_value=obras), \
                mock.patch("gdu.views.ficha.normalizar_expediente", side_effect=lambda e: e):
            response = self.client.get(self._url("viviendas", 1))
        self.assertContains(response, "Obra Cinco, Obra 6")

    def test_capas_de_contexto_solo_las_permitidas(self):
        self._login("ver_viviendas", "ver_catastro_urbano")
        response = self.client.get(self._url("viviendas", 1))
        capas = [c["capa"] for c in response.context["config_mapa"]["capasContexto"]]
        self.assertEqual(capas, ["viviendas", "catastro-urbano"])

    def test_sin_permiso_de_la_capa_da_403(self):
        self._login("ver_barrios")
        response = self.client.get(self._url("viviendas", 1))
        self.assertEqual(response.status_code, 403)

    def test_capa_desconocida_da_404(self):
        self._login("ver_viviendas")
        response = self.client.get(self._url("parcelas", 1))
        self.assertEqual(response.status_code, 404)

    def test_objeto_inexistente_da_404(self):
        self._login("ver_viviendas")
        response = self.client.get(self._url("viviendas", 999))
        self.assertEqual(response.status_code, 404)

    def test_ya_no_existe_el_pdf_generico(self):
        with self.assertRaises(NoReverseMatch):
            reverse("gdu:imprimir")
