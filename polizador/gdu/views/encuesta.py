from itertools import groupby

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from gdu.forms import build_encuesta_form, guardar_encuesta
from gdu.models import Encuesta, Relevamiento, ViviendaRelevamiento


def _agrupar_por_seccion(form):
    secciones = []
    for nombre_seccion, entradas in groupby(form.pregunta_metadata, key=lambda m: m["seccion"]):
        preguntas = []
        for meta in entradas:
            if meta["compuesto_anios_meses"]:
                campo = None
                campo_anios = form[f"{meta['variable']}_anios"]
                campo_meses = form[f"{meta['variable']}_meses"]
            else:
                campo = form[meta["variable"]]
                campo_anios = campo_meses = None
            preguntas.append({
                "meta": meta,
                "campo": campo,
                "campo_anios": campo_anios,
                "campo_meses": campo_meses,
            })
        secciones.append({"nombre": nombre_seccion, "preguntas": preguntas})
    return secciones


@permission_required("gdu.view_relevamiento", raise_exception=True)
def relevamientos_list(request):
    relevamientos = (
        Relevamiento.objects
        .annotate(
            total_viviendas=Count("viviendas", distinct=True),
            total_relevadas=Count("viviendas", filter=Q(viviendas__encuestas__isnull=False), distinct=True),
        )
        .order_by("-fecha")
    )
    return render(request, "gdu/relevamientos-list.html", {"relevamientos": relevamientos})


@permission_required("gdu.view_relevamiento", raise_exception=True)
def relevamiento_viviendas(request, relevamiento_id):
    relevamiento = get_object_or_404(Relevamiento, pk=relevamiento_id)
    viviendas = ViviendaRelevamiento.objects.filter(relevamiento=relevamiento).con_relevado().order_by("numero")
    return render(request, "gdu/relevamiento-viviendas.html", {
        "relevamiento": relevamiento,
        "viviendas": viviendas,
    })


@permission_required("gdu.encuestar_relevamiento", raise_exception=True)
def encuesta_form(request, relevamiento_id, vivienda_id):
    # vivienda_id es el número de la vivienda dentro del relevamiento, como en la base heredada
    relevamiento = get_object_or_404(Relevamiento, pk=relevamiento_id)
    vivienda = get_object_or_404(ViviendaRelevamiento, relevamiento=relevamiento, numero=vivienda_id)
    EncuestaForm = build_encuesta_form(relevamiento)

    if request.method == "POST":
        form = EncuestaForm(request.POST)
        if form.is_valid():
            guardar_encuesta(relevamiento, vivienda, form, request.user)
            messages.success(request, "Encuesta guardada correctamente.")
            return redirect(reverse("gdu:relevamiento_viviendas", args=[relevamiento_id]))
    else:
        form = EncuestaForm()

    encuestas_previas = vivienda.encuestas.order_by("-enviada_en")

    return render(request, "gdu/encuesta-form.html", {
        "relevamiento": relevamiento,
        "vivienda": vivienda,
        "form": form,
        "secciones": _agrupar_por_seccion(form),
        "encuestas_previas": encuestas_previas,
    })
