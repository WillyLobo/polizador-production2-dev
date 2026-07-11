from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from gdu.models import Uf


@permission_required("gdu.editar_nro_adjudicatario", raise_exception=True)
@require_POST
def actualizar_nro_adjudicatario(request, uf_id):
    """
    Edición del número de adjudicatario de una UF (`catastro.uf`), la única de las
    dos ediciones que tenía el visor original (`Edición de Nro. de Adjudicatario`)
    que seguía activa al final de su historia — la de dominio se le había sacado el
    botón (`quitado boton de editar dominio`), así que no se replica acá.
    """
    valor_raw = request.POST.get("nro_adjudicatario", "").strip()
    valor = None
    if valor_raw:
        try:
            valor = int(valor_raw)
        except ValueError:
            return JsonResponse({"errors": "nro_adjudicatario debe ser numérico"}, status=400)

    actualizados = Uf.objects.filter(id=uf_id).update(
        nro_adjudicatario=valor,
        updated_by=request.user.get_username(),
        updated_at=timezone.now(),
    )
    if not actualizados:
        return JsonResponse({"errors": "UF no encontrada"}, status=404)

    return JsonResponse({"id": uf_id, "nro_adjudicatario": valor})
