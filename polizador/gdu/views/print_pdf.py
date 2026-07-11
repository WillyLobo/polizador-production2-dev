import io
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _ficha(titulo, campos, estilos):
    elementos = [Paragraph(str(titulo), estilos["Title"]), Spacer(1, 12)]
    filas = [[str(k), str(v)] for k, v in campos.items() if k != "bearer"]
    if filas:
        tabla = Table([["Campo", "Valor"]] + filas, colWidths=[180, 300])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))
        elementos.append(tabla)
    return elementos


@login_required
@require_POST
def imprimir(request):
    """
    Equivalente a controllers/print.js::postPrint. El original delegaba en templates
    pdfmake por-documento (controllers/templates/*.js) que no existen en ningún lado
    del código disponible (ni en el repo ni en el dump de la base) — probablemente
    vivían solo en el servidor de producción y nunca se commitearon. Este reemplazo
    genera una ficha genérica (título + tabla clave/valor) a partir de los mismos
    datos, no una réplica visual de los documentos originales.

    `data` acepta un objeto (una ficha) o una lista de objetos (impresión múltiple,
    equivalente a la selección por rectángulo + impresión del visor original): cada
    elemento de la lista se imprime en su propia página.
    """
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"errors": "body inválido, se espera JSON"}, status=400)

    campos = body.get("data")
    if isinstance(campos, dict):
        lista_campos = [campos]
    elif isinstance(campos, list) and campos and all(isinstance(c, dict) for c in campos):
        lista_campos = campos
    else:
        return JsonResponse({"errors": "Data is not valid"}, status=400)
    titulo = body.get("template", "Ficha")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    estilos = getSampleStyleSheet()

    elementos = []
    for i, item_campos in enumerate(lista_campos):
        if i:
            elementos.append(PageBreak())
        elementos.extend(_ficha(titulo, item_campos, estilos))

    doc.build(elementos)
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type="application/pdf")
