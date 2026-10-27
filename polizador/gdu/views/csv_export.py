import csv
from collections import defaultdict

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from gdu.models import Encuesta, PreguntaRelevamiento, RespuestaEncuesta


@permission_required("gdu.view_relevamiento", raise_exception=True)
@require_POST
def exportar_csv(request):
    """Equivalente a controllers/export.js::csv: una fila por encuesta, una columna por variable.
    En las preguntas de respuesta múltiple van los valores elegidos separados por ";" (el
    original ponía "[MULTIPLES RESPUESTAS]")."""
    relevamiento_id = request.POST.get("relevamiento")
    if not relevamiento_id or not relevamiento_id.isdigit():
        return JsonResponse({"errors": "relevamiento cannot be blank"}, status=400)

    columnas = list(
        PreguntaRelevamiento.objects.filter(relevamiento_id=relevamiento_id).order_by("id").values_list("variable", flat=True)
    )
    valores = defaultdict(lambda: defaultdict(list))
    for encuesta_id, variable, valor in RespuestaEncuesta.objects.filter(
        encuesta__relevamiento_id=relevamiento_id,
    ).order_by("id").values_list("encuesta_id", "pregunta_relevamiento__variable", "valor"):
        valores[encuesta_id][variable].append(valor)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="resultados-relevamiento.csv"'
    writer = csv.writer(response)
    writer.writerow(["vivienda", "tipo", "fechahora"] + columnas)
    encuestas = Encuesta.objects.filter(relevamiento_id=relevamiento_id).select_related("vivienda").order_by("enviada_en")
    for encuesta in encuestas:
        respuestas = valores[encuesta.pk]
        writer.writerow(
            [encuesta.vivienda.numero, encuesta.tipo, encuesta.capturada_en or encuesta.enviada_en]
            + [";".join(respuestas.get(c, [])) for c in columnas]
        )
    return response
