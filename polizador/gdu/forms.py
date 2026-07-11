from django import forms
from django.utils import timezone

from .models import Encuesta, PreguntaRelevamiento, Respuesta, RespuestaEncuesta

# our.encuesta.tipo no tiene tabla de referencia en la base heredada; los valores
# históricos (cargados por la app mobile) usan 1. Usamos un valor nuevo acá para
# poder distinguir las encuestas cargadas desde este formulario web.
TIPO_ENCUESTA_WEB = 5

TIPO_MULTIPLE_CHOICE_UNICA = (1, 2)
TIPO_MULTIPLE_CHOICE_MULTIPLE = (9,)
TIPO_ESCALA = {3: 10, 4: 5}
TIPO_SI_NO = (5,)
TIPO_ENTERO = (6,)
TIPO_DECIMAL = (8,)
TIPO_TIEMPO_ANIOS_MESES = (10,)
# el resto (7 - Texto Simple, y cualquier tipo no contemplado) se renderiza como CharField


def build_encuesta_form(relevamiento_id):
    """
    Arma dinámicamente una clase de Form a partir de las preguntas configuradas
    en our.pregunta_relevamiento para un relevamiento dado (equivalente a lo que
    hacía la SPA Angular a partir del mismo template GraphQL get-vivienda-relevamiento).
    """
    preguntas = list(
        PreguntaRelevamiento.objects
        .filter(relevamiento_id=relevamiento_id)
        .select_related("pregunta", "pregunta__tipo", "seccion")
        .order_by("seccion__orden", "id")
    )

    campos = {}
    metadata = []

    for pr in preguntas:
        tipo_id = pr.pregunta.tipo_id
        label = pr.pregunta.texto
        help_text = pr.pregunta.subtexto or ""
        required = pr.required
        compuesto_anios_meses = tipo_id in TIPO_TIEMPO_ANIOS_MESES

        if tipo_id in TIPO_MULTIPLE_CHOICE_UNICA:
            opciones = [
                (r.id, r.texto)
                for r in Respuesta.objects.filter(pregunta_id=pr.pregunta_id).order_by("nro_opcion")
            ]
            campos[pr.variable] = forms.TypedChoiceField(
                choices=[("", "---------")] + opciones, coerce=int, required=required,
                label=label, help_text=help_text,
            )
        elif tipo_id in TIPO_MULTIPLE_CHOICE_MULTIPLE:
            opciones = [
                (r.id, r.texto)
                for r in Respuesta.objects.filter(pregunta_id=pr.pregunta_id).order_by("nro_opcion")
            ]
            campos[pr.variable] = forms.TypedMultipleChoiceField(
                choices=opciones, coerce=int, required=required,
                label=label, help_text=help_text, widget=forms.CheckboxSelectMultiple,
            )
        elif tipo_id in TIPO_ESCALA:
            maximo = TIPO_ESCALA[tipo_id]
            campos[pr.variable] = forms.TypedChoiceField(
                choices=[("", "---------")] + [(i, str(i)) for i in range(1, maximo + 1)],
                coerce=int, required=required, label=label, help_text=help_text,
            )
        elif tipo_id in TIPO_SI_NO:
            campos[pr.variable] = forms.TypedChoiceField(
                choices=[("", "---------"), ("true", "Sí"), ("false", "No")],
                required=required, label=label, help_text=help_text,
            )
        elif tipo_id in TIPO_ENTERO:
            campos[pr.variable] = forms.IntegerField(required=required, label=label, help_text=help_text)
        elif tipo_id in TIPO_DECIMAL:
            campos[pr.variable] = forms.DecimalField(required=required, label=label, help_text=help_text)
        elif compuesto_anios_meses:
            campos[f"{pr.variable}_anios"] = forms.IntegerField(
                min_value=0, required=required, label=f"{label} (años)",
            )
            campos[f"{pr.variable}_meses"] = forms.IntegerField(
                min_value=0, max_value=11, required=required, label=f"{label} (meses)",
            )
        else:
            campos[pr.variable] = forms.CharField(required=required, label=label, help_text=help_text)

        metadata.append({
            "pregunta_relevamiento_id": pr.id,
            "variable": pr.variable,
            "seccion": pr.seccion.nombre,
            "tipo_pregunta": tipo_id,
            "compuesto_anios_meses": compuesto_anios_meses,
            # Reglas de la SPA Angular original ("(e) => {...}"), nunca se ejecutan acá:
            # se evalúan en el navegador para mostrar/ocultar preguntas, igual que hacía la SPA.
            "visible": (pr.visible or "").strip("|") or None,
            "valido": (pr.valido or "").strip("|") or None,
        })

    EncuestaForm = type("EncuestaForm", (forms.Form,), campos)
    EncuestaForm.pregunta_metadata = metadata
    return EncuestaForm


def guardar_encuesta(relevamiento_id, vivienda_id, form, username):
    """
    Persiste una Encuesta + sus RespuestaEncuesta a partir de un form ya validado
    (equivalente a controllers/gql/save-encuesta.js::formatRespuestas). Cada envío
    crea una Encuesta nueva (no se edita en el lugar), igual que hacía el código original;
    el trigger our.update_vivienda_relevado marca la vivienda como relevada automáticamente.
    """
    encuesta = Encuesta.objects.create(
        relevamiento_id=relevamiento_id,
        vivienda=vivienda_id,
        user=username,
        tstamp=timezone.now(),
        tipo=TIPO_ENCUESTA_WEB,
    )

    respuestas = []
    for meta in form.pregunta_metadata:
        if meta["compuesto_anios_meses"]:
            anios = form.cleaned_data.get(f"{meta['variable']}_anios")
            meses = form.cleaned_data.get(f"{meta['variable']}_meses")
            if anios is None and meses is None:
                continue
            total_meses = (anios or 0) * 12 + (meses or 0)
            respuestas.append(RespuestaEncuesta(
                encuesta=encuesta, pregunta_id=meta["pregunta_relevamiento_id"],
                respuesta=None, valor=str(total_meses),
            ))
            continue

        valor = form.cleaned_data.get(meta["variable"])
        if valor in (None, "", []):
            continue

        if meta["tipo_pregunta"] in TIPO_MULTIPLE_CHOICE_MULTIPLE:
            for opcion_id in valor:
                respuestas.append(RespuestaEncuesta(
                    encuesta=encuesta, pregunta_id=meta["pregunta_relevamiento_id"],
                    respuesta_id=opcion_id, valor=str(opcion_id),
                ))
        elif meta["tipo_pregunta"] in TIPO_MULTIPLE_CHOICE_UNICA:
            respuestas.append(RespuestaEncuesta(
                encuesta=encuesta, pregunta_id=meta["pregunta_relevamiento_id"],
                respuesta_id=valor, valor=str(valor),
            ))
        else:
            respuestas.append(RespuestaEncuesta(
                encuesta=encuesta, pregunta_id=meta["pregunta_relevamiento_id"],
                respuesta=None, valor=str(valor),
            ))

    RespuestaEncuesta.objects.bulk_create(respuestas)
    return encuesta
