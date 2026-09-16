import io
import zipfile

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

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
