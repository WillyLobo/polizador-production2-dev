from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render


@login_required
@permission_required("gdu.view_actuacion", raise_exception=True)
def lista_actuaciones(request):
    return render(request, "gdu/lista-actuaciones.html", {})


@login_required
@permission_required("gdu.view_contratacion", raise_exception=True)
def lista_contrataciones(request):
    return render(request, "gdu/lista-contrataciones.html", {})


@login_required
@permission_required("gdu.view_contratacion", raise_exception=True)
def lista_contrataciones_sin_obra(request):
    return render(request, "gdu/lista-contrataciones-sin-obra.html", {})


@login_required
@permission_required("gdu.view_intervencion", raise_exception=True)
def lista_intervenciones(request):
    return render(request, "gdu/lista-intervenciones.html", {})


@login_required
@permission_required("gdu.view_programa", raise_exception=True)
def lista_programas(request):
    return render(request, "gdu/lista-programas.html", {})


@login_required
@permission_required("gdu.view_barrio", raise_exception=True)
def lista_barrios(request):
    return render(request, "gdu/lista-barrios.html", {})


@login_required
@permission_required("gdu.view_parcela", raise_exception=True)
def lista_parcelas(request):
    return render(request, "gdu/lista-parcelas.html", {})


@login_required
@permission_required("gdu.view_uf", raise_exception=True)
def lista_ufs(request):
    return render(request, "gdu/lista-ufs.html", {})


@login_required
@permission_required("gdu.view_localidad", raise_exception=True)
def lista_localidades(request):
    return render(request, "gdu/lista-localidades.html", {})


@login_required
@permission_required("gdu.view_expropiacion", raise_exception=True)
def lista_expropiaciones(request):
    return render(request, "gdu/lista-expropiaciones.html", {})


@login_required
@permission_required("gdu.view_planomensura", raise_exception=True)
def lista_planos_mensura(request):
    return render(request, "gdu/lista-planos-mensura.html", {})


@login_required
@permission_required("gdu.view_adjudicacionbeneficiario", raise_exception=True)
def lista_adjudicaciones_beneficiario(request):
    return render(request, "gdu/lista-adjudicaciones-beneficiario.html", {})


@login_required
@permission_required("gdu.view_resolucioncostos", raise_exception=True)
def lista_resoluciones_costos(request):
    return render(request, "gdu/lista-resoluciones-costos.html", {})


@login_required
@permission_required("gdu.view_tipocontratacion", raise_exception=True)
def lista_tipos_contratacion(request):
    return render(request, "gdu/lista-tipos-contratacion.html", {})


@login_required
@permission_required("gdu.view_tipoestado", raise_exception=True)
def lista_tipos_estado(request):
    return render(request, "gdu/lista-tipos-estado.html", {})


@login_required
@permission_required("gdu.view_tipointervencion", raise_exception=True)
def lista_tipos_intervencion(request):
    return render(request, "gdu/lista-tipos-intervencion.html", {})


@login_required
@permission_required("gdu.view_tipouf", raise_exception=True)
def lista_tipos_uf(request):
    return render(request, "gdu/lista-tipos-uf.html", {})


@login_required
@permission_required("gdu.view_destinoparcela", raise_exception=True)
def lista_destinos_parcela(request):
    return render(request, "gdu/lista-destinos-parcela.html", {})


@login_required
@permission_required("gdu.view_estadogestionexpropiacion", raise_exception=True)
def lista_estados_gestion_expropiacion(request):
    return render(request, "gdu/lista-estados-gestion-expropiacion.html", {})


@login_required
@permission_required("gdu.view_adjudicatario3450", raise_exception=True)
def lista_adjudicatarios_3450(request):
    return render(request, "gdu/lista-adjudicatarios-3450.html", {})
