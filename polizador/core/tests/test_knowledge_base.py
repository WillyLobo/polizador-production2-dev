import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase

from core import knowledge_base as kb

UserModel = get_user_model()

FIXTURE_SOURCE = '''
from django.db import models


class Widget(models.Model):
    """Un widget de prueba."""

    nombre = models.CharField(max_length=100)


def crear_widget(nombre):
    """Crea un Widget."""
    return Widget.objects.create(nombre=nombre)
'''


class KnowledgeBaseViewsTest(TestCase):
    """Mismo patrón que test_dashboard.py (anónimo/usuario común/superuser), más los
    casos propios de esta vista: resolución de page_path, 404 para desconocidos/
    traversal, y el rewriting de los links "Ver también" (ver core/views.py)."""

    def setUp(self):
        tmp_dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        app_dir = tmp_dir / "kb_sample_app"
        app_dir.mkdir()
        (app_dir / "models.py").write_text(FIXTURE_SOURCE, encoding="utf-8")
        self.enterContext(self.settings(BASE_DIR=tmp_dir, KNOWLEDGE_BASE_ROOT=tmp_dir / "knowledge_base"))

        call_command("kb_extract", "kb_sample_app", "--render")

        # Widget queda con un link "Ver también" hacia crear_widget, para probar el rewrite.
        front, _ = kb.parse_front_matter(kb.markdown_path("kb_sample_app/models/Widget").read_text(encoding="utf-8"))
        front["authored"] = "true"
        content = (
            kb.render_front_matter(front)
            + "\n# Widget\n\n## Ver también\n\n"
            + "- [crear_widget](crear_widget.md)\n"
        )
        kb.markdown_path("kb_sample_app/models/Widget").write_text(content, encoding="utf-8")
        kb.render_html_for("kb_sample_app/models/Widget")

        self.client = Client()
        self.user = UserModel.objects.create_user(username="plain_user", password="pass1234!")
        self.superuser = UserModel.objects.create_superuser(username="admin_user", password="pass1234!")

    def test_anonymous_redirected_to_login(self):
        assert self.client.get("/administracion/conocimiento/").status_code == 302
        assert self.client.get("/administracion/conocimiento/kb_sample_app/models/Widget/").status_code == 302

    def test_regular_user_forbidden(self):
        self.client.login(username="plain_user", password="pass1234!")
        assert self.client.get("/administracion/conocimiento/").status_code == 403
        assert self.client.get("/administracion/conocimiento/kb_sample_app/models/Widget/").status_code == 403

    def test_superuser_sees_index_with_tree(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/conocimiento/")
        assert resp.status_code == 200
        assert "kb_sample_app" in resp.content.decode()

    def test_superuser_sees_known_page_with_rewritten_link(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/conocimiento/kb_sample_app/models/Widget/")
        assert resp.status_code == 200
        body = resp.content.decode()
        assert "Widget" in body
        # El .md original decía "crear_widget.md"; la vista debe reescribirlo a la URL real.
        assert 'href="/administracion/conocimiento/kb_sample_app/models/crear_widget/"' in body
        assert 'href="crear_widget.md"' not in body

    def test_unknown_page_path_is_404(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/conocimiento/kb_sample_app/models/NoExiste/")
        assert resp.status_code == 404

    def test_path_traversal_attempt_is_404_not_leaked(self):
        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/administracion/conocimiento/../../../../etc/passwd/")
        assert resp.status_code == 404
        assert b"root:" not in resp.content

    def test_navbar_link_only_for_superuser(self):
        resp = self.client.get("/")
        assert 'href="/administracion/conocimiento/"' not in resp.content.decode()

        self.client.login(username="plain_user", password="pass1234!")
        resp = self.client.get("/")
        assert 'href="/administracion/conocimiento/"' not in resp.content.decode()

        self.client.login(username="admin_user", password="pass1234!")
        resp = self.client.get("/")
        assert 'href="/administracion/conocimiento/"' in resp.content.decode()
