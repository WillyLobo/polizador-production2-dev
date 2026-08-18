import tempfile
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from core import knowledge_base as kb

FIXTURE_SOURCE = (Path(__file__).parent / "fixtures" / "kb_sample_module.py").read_text(encoding="utf-8")

WIDGET_PAGE = "kb_sample_app/models/Widget"
CREAR_WIDGET_PAGE = "kb_sample_app/models/crear_widget"
WIDGET_CREADO_PAGE = "kb_sample_app/models/widget_creado"


class KbExtractTest(TestCase):
    """Ejercita core/knowledge_base.py + kb_extract contra un módulo fixture sintético
    (nunca contra la app carga real), para que el test sea hermético y no dependa de
    futuros cambios en carga. Ver knowledge_base/README.md para el pipeline completo."""

    def setUp(self):
        tmp_dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.app_dir = tmp_dir / "kb_sample_app"
        self.app_dir.mkdir()
        (self.app_dir / "models.py").write_text(FIXTURE_SOURCE, encoding="utf-8")
        self.kb_root = tmp_dir / "knowledge_base"
        self.enterContext(self.settings(BASE_DIR=tmp_dir, KNOWLEDGE_BASE_ROOT=self.kb_root))

    def _rewrite_fixture(self, source: str):
        (self.app_dir / "models.py").write_text(source, encoding="utf-8")

    def test_extracts_symbols_with_signature_lines_and_decorators(self):
        call_command("kb_extract", "kb_sample_app")

        manifest = kb.load_manifest()
        symbols = manifest["kb_sample_app"]["modules"]["models"]["symbols"]

        assert set(symbols) == {"Widget", "crear_widget", "widget_creado"}

        widget = symbols["Widget"]
        assert widget["kind"] == "class"
        assert widget["module"] == "kb_sample_app/models.py"
        assert widget["page_path"] == WIDGET_PAGE
        assert widget["bases"] == ["models.Model"]
        assert widget["docstring"] == "Un widget de prueba."
        assert [m["name"] for m in widget["methods"]] == ["etiqueta"]
        # lineno real de "class Widget(models.Model):" en el fixture
        assert widget["lines"][0] == FIXTURE_SOURCE.splitlines().index("class Widget(models.Model):") + 1

        fn = symbols["crear_widget"]
        assert fn["kind"] == "function"
        assert fn["signature"].startswith("def crear_widget(nombre)")

        receiver_fn = symbols["widget_creado"]
        assert receiver_fn["decorators"] == ["receiver(post_save, sender=Widget)"]

    def test_creates_stub_md_with_front_matter_and_placeholders(self):
        call_command("kb_extract", "kb_sample_app")

        md_file = kb.markdown_path(WIDGET_PAGE)
        assert md_file.exists()

        front, body = kb.parse_front_matter(md_file.read_text(encoding="utf-8"))
        assert front["symbol"] == "Widget"
        assert front["kind"] == "class"
        assert front["authored"] == "false"
        assert "signature_hash" in front
        assert "## Propósito" in body
        assert "_(pendiente de autoría)_" in body

    def test_rerun_does_not_clobber_authored_content(self):
        call_command("kb_extract", "kb_sample_app")

        md_file = kb.markdown_path(WIDGET_PAGE)
        front, _ = kb.parse_front_matter(md_file.read_text(encoding="utf-8"))
        front["authored"] = "true"
        hand_written = kb.render_front_matter(front) + "\n# Widget\n\nTexto escrito a mano.\n"
        md_file.write_text(hand_written, encoding="utf-8")

        call_command("kb_extract", "kb_sample_app")

        assert md_file.read_text(encoding="utf-8") == hand_written

        manifest = kb.load_manifest()
        widget = manifest["kb_sample_app"]["modules"]["models"]["symbols"]["Widget"]
        assert widget["authored"] is True
        assert widget["stale"] is False

    def test_check_reports_staleness_without_writing(self):
        call_command("kb_extract", "kb_sample_app")
        manifest_before = kb.manifest_path().read_text(encoding="utf-8")

        # Firma sin cambios en el docstring: no debería marcar stale a los demás símbolos.
        self._rewrite_fixture(FIXTURE_SOURCE.replace(
            '"""Un widget de prueba."""', '"""Un widget de prueba (actualizado)."""'
        ))

        with self.assertRaises(SystemExit) as ctx:
            call_command("kb_extract", "kb_sample_app", "--check")
        assert ctx.exception.code == 1

        # --check no escribe nada: ni el manifest ni los .md cambian.
        assert kb.manifest_path().read_text(encoding="utf-8") == manifest_before
        front, _ = kb.parse_front_matter(kb.markdown_path(WIDGET_PAGE).read_text(encoding="utf-8"))
        assert front["signature_hash"] == kb.load_manifest()["kb_sample_app"]["modules"]["models"]["symbols"]["Widget"]["signature_hash"]

        # Correrlo sin --check sí debe detectar y reportar el drift (sin pisar el .md autorado).
        call_command("kb_extract", "kb_sample_app")
        manifest = kb.load_manifest()
        widget = manifest["kb_sample_app"]["modules"]["models"]["symbols"]["Widget"]
        assert widget["stale"] is True

    def test_render_generates_html_from_markdown(self):
        call_command("kb_extract", "kb_sample_app", "--render")

        html_file = kb.html_path(WIDGET_PAGE)
        assert html_file.exists()
        html = html_file.read_text(encoding="utf-8")
        assert "<h1>Widget</h1>" in html
        assert "<h2>Propósito</h2>" in html

    def test_check_and_render_together_is_rejected(self):
        with self.assertRaises(Exception):
            call_command("kb_extract", "kb_sample_app", "--check", "--render")
