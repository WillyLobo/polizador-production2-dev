import os
import io
import pymupdf
import pytesseract
from PIL import Image
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from secretariador.models import InstrumentosLegalesDecretos, InstrumentosLegalesMemorandum, InstrumentosLegalesResoluciones
import time

# Maps each instrument model to its field-name prefix. All three models follow the
# convention <prefix> (FileField), <prefix>_document, <prefix>_descripcion,
# <prefix>_fecha_aprobacion.
INSTRUMENT_PREFIXES = {
    InstrumentosLegalesResoluciones: "instrumentolegalresoluciones",
    InstrumentosLegalesMemorandum: "instrumentolegalmemorandum",
    InstrumentosLegalesDecretos: "instrumentolegaldecretos",
}

def extract_text_hybrid(file: str | bytes, lang: str = "spa", min_chars_per_page: int = 20, dpi: int = 300, psm: int = 6) -> str:
    """Extract text from a PDF (given a local path or raw file bytes), using
    each page's embedded text layer where present and falling back to local
    Tesseract OCR for scanned pages."""
    text_parts = []
    open_kwargs = {"filename": file} if isinstance(file, str) else {"stream": file, "filetype": "pdf"}
    with pymupdf.open(**open_kwargs) as doc:
        for page in doc:
            page_text = page.get_text().strip()
            if len(page_text) < min_chars_per_page:
                pixmap = page.get_pixmap(dpi=dpi)
                image = Image.open(io.BytesIO(pixmap.tobytes("png")))
                page_text = pytesseract.image_to_string(image, lang=lang, config=f"--psm {psm}").strip()
            text_parts.append(page_text)
    return "\n".join(text_parts)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for model, prefix in INSTRUMENT_PREFIXES.items():
            document_field = f"{prefix}_document"
            pendientes = model.objects.exclude(**{prefix: ""}).filter(
                Q(**{f"{document_field}__isnull": True}) | Q(**{document_field: ""})
            )

            self.stdout.write(f"{self.style.MIGRATE_HEADING(str(model._meta.verbose_name_plural))} ({pendientes.count()} pendientes)")
            for p in pendientes:
                self._procesar(p, prefix)

    def _procesar(self, p, prefix):
        start_time = time.perf_counter()
        file_field = getattr(p, prefix)
        local_path = os.path.join(settings.MEDIA_ROOT, file_field.name)
        self.stdout.write(f"{self.style.MIGRATE_LABEL('Procesando el archivo:')} {self.style.SQL_KEYWORD(local_path)}")

        if os.path.exists(local_path):
            source = local_path
        else:
            self.stdout.write(f"{self.style.WARNING('Archivo local no encontrado, se descarga desde la nube:')} {local_path}")
            with file_field.open("rb") as f:
                source = f.read()

        try:
            self.stdout.write(f"{self.style.MIGRATE_LABEL('Procesando OCR:')}")
            setattr(p, f"{prefix}_document", extract_text_hybrid(source))
            p.save()
        except Exception as e:
            self.stdout.write(f"Error al procesar el archivo {self.style.ERROR(local_path)}: {self.style.ERROR(e)}")
            return

        # Console output
        self.stdout.write(f"{self.style.SUCCESS('Archivo procesado con éxito.')}")
        self.stdout.write(f"    ID:{p.id}")
        self.stdout.write(f"    Instrumento: {p}")
        self.stdout.write(f"    Fecha de Aprobación: {getattr(p, f'{prefix}_fecha_aprobacion')}")
        self.stdout.write(f"    Descripción: {getattr(p, f'{prefix}_descripcion')}")
        self.stdout.write(f"    Texto Extraído: {self.style.HTTP_SUCCESS(getattr(p, f'{prefix}_document')[:100])}...(truncado)")

        elapsed_time = time.perf_counter() - start_time
        self.stdout.write(f"Tiempo de ejecución: {elapsed_time:.6f} segundos.")