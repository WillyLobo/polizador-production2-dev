from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from carga.models import Obra
from gdu.models import Contratacion, ObraContratacion


@login_required
@permission_required("gdu.add_obracontratacion", raise_exception=True)
@require_POST
def vincular_obra(request, contratacion_id):
    """
    Vinculación manual desde gdu/lista-contrataciones-sin-obra.html: la obra se elige
    en la tabla anidada de gdu/_contratacion_sin_obra_detail.html (datatable filtrable
    de Obra, ver "gdu-obras-para-vincular" en api/views/gdu_views.py) y su botón postea
    directo acá, sin formulario intermedio.
    """
    contratacion = get_object_or_404(Contratacion, id=contratacion_id)
    obra = Obra.objects.filter(gdu_contratacion__isnull=True, id=request.POST.get("obra")).first()
    if obra is None:
        return JsonResponse(
            {"ok": False, "error": "La obra no existe o ya está vinculada a otra contratación."}, status=400,
        )
    ObraContratacion.objects.create(obra=obra, contratacion=contratacion, vinculado_manualmente=True)
    return JsonResponse({"ok": True})
