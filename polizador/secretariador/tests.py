import io
import zipfile
from pathlib import Path

from django.conf import settings
from django.test import TestCase

from secretariador.docx_header import inject_header, tiene_encabezado_valido

BASE = Path(settings.BASE_DIR)
BODY_TEMPLATE = BASE / "secretariador/media/solicitud_template.docx"
HEADER_SOURCE = BASE / "secretariador/media/solicitud_exterior.docx"


def _read_part(docx_bytes, part):
    with zipfile.ZipFile(io.BytesIO(docx_bytes)) as zf:
        return zf.read(part)


def _build_header_docx_with_marker():
    """Copia solicitud_exterior.docx pero con un texto distinto en su header de primera página."""
    with open(HEADER_SOURCE, "rb") as f:
        original = f.read()
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(original)) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/header3.xml":
                assert b"Provincia del Chaco" in data
                data = data.replace(b"Provincia del Chaco", b"ENCABEZADO DE PRUEBA")
            zout.writestr(info, data)
    out.seek(0)
    return out


class InjectHeaderTests(TestCase):
    def test_header_is_replaced_and_body_untouched(self):
        original_body_document_xml = _read_part(BODY_TEMPLATE.read_bytes(), "word/document.xml")

        merged = inject_header(BODY_TEMPLATE, _build_header_docx_with_marker())
        merged_bytes = merged.read()

        merged_header = _read_part(merged_bytes, "word/header3.xml")
        self.assertIn(b"ENCABEZADO DE PRUEBA", merged_header)
        self.assertNotIn(b"Provincia del Chaco", merged_header)

        merged_document_xml = _read_part(merged_bytes, "word/document.xml")
        self.assertEqual(merged_document_xml, original_body_document_xml)
        self.assertIn(b"{{parrafo_uno}}", merged_document_xml)

    def test_tiene_encabezado_valido_true_for_real_template(self):
        with open(BODY_TEMPLATE, "rb") as f:
            self.assertTrue(tiene_encabezado_valido(f))

    def test_tiene_encabezado_valido_false_for_garbage(self):
        garbage = io.BytesIO(b"not a docx at all")
        self.assertFalse(tiene_encabezado_valido(garbage))
