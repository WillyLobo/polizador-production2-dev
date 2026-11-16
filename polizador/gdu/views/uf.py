from decimal import Decimal

from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST

from gdu.models import Parcela, Uf
from gdu.models.base import EstadoDominial


@login_required
@permission_required("gdu.add_uf", raise_exception=True)
@require_http_methods(["GET", "POST"])
def generar_uf(request, parcela_id):
    """
    Reemplaza la acción Python "Generar UF" (UF(|)) del gdu.qgz heredado: crea la UF 1 de una
    parcela que todavía no tiene ninguna, con la geometría de la parcela. El proyecto OAPIF no
    lleva código Python, así que QGIS la abre como acción "Abrir URL" en el navegador; el GET
    muestra la parcela y el POST crea la UF. Pone IPDUV aunque el usuario no tenga
    gdu.editar_dominio: es el valor fijo que ponía la acción vieja, no una edición del dominio.
    QGIS manda id 0 cuando la parcela todavía no se guardó (su "id" es NULL).
    """
    parcela = Parcela.objects.filter(pk=parcela_id).first() if parcela_id else None
    if parcela is None:
        estado = 404 if parcela_id else 400
        return render(request, "gdu/generar-uf.html", {"parcela_id": parcela_id}, status=estado)

    creada = None
    if request.method == "POST":
        with transaction.atomic():
            # bloquea la parcela: dos clics seguidos no crean dos UF
            parcela = Parcela.objects.select_for_update().get(pk=parcela.pk)
            if not parcela.ufs.exists():
                creada = Uf(
                    parcela=parcela, uf="1", coefuf=Decimal("100"), poligono="00-01",
                    estado_dominial=EstadoDominial.IPDUV, geom=parcela.geom, updated_by=request.user,
                )
                creada.full_clean()
                creada.save()
    contexto = {"parcela": parcela, "ufs": parcela.ufs.order_by("uf", "pk"), "creada": creada}
    return render(request, "gdu/generar-uf.html", contexto, status=201 if creada else 200)


@permission_required("gdu.editar_nro_adjudicatario", raise_exception=True)
@require_POST
def actualizar_nro_adjudicatario(request, uf_id):
    """
    Edición del número de adjudicatario (Sistema 3450) de una UF desde el visor, la única de
    las dos ediciones que tenía el visor original (`Edición de Nro. de Adjudicatario`) que
    seguía activa al final de su historia — la de dominio se le había sacado el botón
    (`quitado boton de editar dominio`), así que no se replica acá. Pasa por el ORM: queda
    en el historial con el usuario.
    """
    valor_raw = request.POST.get("nro_adjudicatario", "").strip()
    valor = None
    if valor_raw:
        try:
            valor = int(valor_raw)
        except ValueError:
            return JsonResponse({"errors": "nro_adjudicatario debe ser numérico"}, status=400)

    uf = Uf.objects.filter(id=uf_id).first()
    if uf is None:
        return JsonResponse({"errors": "UF no encontrada"}, status=404)
    uf.adjudicatario_id = valor
    uf.updated_by = request.user
    uf.save(update_fields=["adjudicatario", "updated_by", "updated_at"])
    return JsonResponse({"id": uf_id, "nro_adjudicatario": valor})
