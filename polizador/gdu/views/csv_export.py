import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from gdu.models import Encuesta, PreguntaRelevamiento, ResultadosEncuesta

TIPO_MULTIPLE_CHOICE_MULTIPLE = 9


@login_required
@require_POST
def exportar_csv(request):
    """Equivalente a controllers/export.js::csv."""
    relevamiento_id = request.POST.get("relevamiento")
    if not relevamiento_id:
        return JsonResponse({"errors": "relevamiento cannot be blank"}, status=400)

    columnas = list(
        PreguntaRelevamiento.objects
        .filter(relevamiento_id=relevamiento_id)
        .order_by("id")
        .values_list("variable", flat=True)
    )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="resultados-relevamiento.csv"'
    writer = csv.writer(response)
    writer.writerow(["vivienda", "tipo", "fechahora"] + columnas)

    encuestas = Encuesta.objects.filter(relevamiento_id=relevamiento_id).order_by("tstamp")
    for encuesta in encuestas:
        respuestas_por_variable = {}
        for r in ResultadosEncuesta.objects.filter(encuesta=encuesta.id):
            if r.tipo_pregunta == TIPO_MULTIPLE_CHOICE_MULTIPLE:
                respuestas_por_variable[r.variable] = "[MULTIPLES RESPUESTAS]"
            else:
                respuestas_por_variable[r.variable] = r.respuesta

        writer.writerow(
            [encuesta.vivienda, encuesta.tipo, encuesta.tstamp]
            + [respuestas_por_variable.get(c, "") for c in columnas]
        )

    return response
