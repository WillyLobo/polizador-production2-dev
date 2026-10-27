import json
from decimal import Decimal

from django import forms
from django.db import transaction
from django.utils import timezone

from gdu.models import Encuesta, PreguntaRelevamiento, RespuestaEncuesta
from gdu.reglas import ReglaInvalida, evaluar

# ids de gdu.TipoPregunta (se conservan de la base heredada)
TIPO_MULTIPLE_CHOICE_UNICA = (1, 2)
TIPO_MULTIPLE_CHOICE_MULTIPLE = (9,)
TIPO_ESCALA = {3: 10, 4: 5}
TIPO_SI_NO = (5,)
TIPO_ENTERO = (6,)
TIPO_DECIMAL = (8,)
TIPO_TIEMPO_ANIOS_MESES = (10,)
TIPO_STRING = (2, 7)
# el resto (7 - Texto Simple, y cualquier tipo no contemplado) se renderiza como CharField


def _coercion(tipo_id):
    """Cómo se tipa el valor de una opción para las reglas: los Multiple Choice String
    comparan texto y el resto números, como en la app mobile."""
    return str if tipo_id in TIPO_STRING else int


def _regla_visible(pregunta_relevamiento):
    """La de la pregunta y la de su sección: se ve si se cumplen las dos."""
    reglas = [r for r in (pregunta_relevamiento.seccion.regla_visible, pregunta_relevamiento.regla_visible) if r]
    if not reglas:
        return None
    return reglas[0] if len(reglas) == 1 else {"and": reglas}


class EncuestaBaseForm(forms.Form):
    """Las preguntas son todas no obligatorias para Django: la obligatoriedad y la regla de
    validez dependen de si la pregunta está visible, y eso se decide en clean() con las
    mismas reglas que evalúa el navegador (gdu/reglas.py)."""
    pregunta_metadata = []

    def respuestas(self):
        """{variable: valor tipado} de lo cargado, como lo leen las reglas."""
        datos = {}
        for meta in self.pregunta_metadata:
            variable = meta["variable"]
            if meta["compuesto_anios_meses"]:
                anios = self.cleaned_data.get(f"{variable}_anios")
                meses = self.cleaned_data.get(f"{variable}_meses")
                datos[variable] = None if anios is None and meses is None else (anios or 0) * 12 + (meses or 0)
                continue
            valor = self.cleaned_data.get(variable)
            if valor in ("", []):
                valor = None
            if meta["tipo_pregunta"] in TIPO_SI_NO and valor is not None:
                valor = valor == "true"
            elif isinstance(valor, Decimal):
                valor = float(valor)
            datos[variable] = valor
        return datos

    def clean(self):
        cleaned = super().clean()
        datos = self.respuestas()
        self.visibles = set()
        for meta in self.pregunta_metadata:
            variable = meta["variable"]
            campo_error = f"{variable}_anios" if meta["compuesto_anios_meses"] else variable
            try:
                visible = meta["regla_visible"] is None or bool(evaluar(meta["regla_visible"], datos))
                valido = meta["regla_valido"] is None or bool(evaluar(meta["regla_valido"], datos))
            except (ReglaInvalida, TypeError):
                # una regla que no se puede evaluar no oculta ni rechaza la pregunta
                visible, valido = True, True
            if not visible:
                continue
            self.visibles.add(variable)
            if datos[variable] is None:
                if meta["requerida"]:
                    self.add_error(campo_error, "Este campo es obligatorio.")
            elif not valido:
                self.add_error(campo_error, "El valor no es válido para esta pregunta.")
        self.datos = datos
        return cleaned


def build_encuesta_form(relevamiento):
    """
    Arma dinámicamente una clase de Form a partir de las preguntas configuradas para un
    relevamiento (equivalente a lo que hacía la SPA Angular a partir del template GraphQL
    get-vivienda-relevamiento).
    """
    preguntas = list(
        PreguntaRelevamiento.objects
        .filter(relevamiento=relevamiento)
        .select_related("pregunta__tipo", "seccion")
        .prefetch_related("pregunta__opciones")
        .order_by("seccion__orden", "id")
    )

    campos = {}
    metadata = []

    for pr in preguntas:
        tipo_id = pr.pregunta.tipo_id
        label = pr.pregunta.texto
        help_text = pr.pregunta.subtexto or ""
        compuesto_anios_meses = tipo_id in TIPO_TIEMPO_ANIOS_MESES
        # el valor de una opción es Respuesta.valor (lo que comparan las reglas y lo que se guarda)
        opciones = [(_coercion(tipo_id)(r.valor), r.texto) for r in pr.pregunta.opciones.all()]
        comunes = {"required": False, "label": label, "help_text": help_text}

        if tipo_id in TIPO_MULTIPLE_CHOICE_UNICA:
            campos[pr.variable] = forms.TypedChoiceField(
                choices=[("", "---------")] + opciones, coerce=_coercion(tipo_id), empty_value=None, **comunes,
            )
        elif tipo_id in TIPO_MULTIPLE_CHOICE_MULTIPLE:
            campos[pr.variable] = forms.TypedMultipleChoiceField(
                choices=opciones, coerce=_coercion(tipo_id), widget=forms.CheckboxSelectMultiple, **comunes,
            )
        elif tipo_id in TIPO_ESCALA:
            maximo = TIPO_ESCALA[tipo_id]
            campos[pr.variable] = forms.TypedChoiceField(
                choices=[("", "---------")] + [(i, str(i)) for i in range(1, maximo + 1)],
                coerce=int, empty_value=None, **comunes,
            )
        elif tipo_id in TIPO_SI_NO:
            campos[pr.variable] = forms.TypedChoiceField(
                choices=[("", "---------"), ("true", "Sí"), ("false", "No")], empty_value=None, **comunes,
            )
        elif tipo_id in TIPO_ENTERO:
            campos[pr.variable] = forms.IntegerField(**comunes)
        elif tipo_id in TIPO_DECIMAL:
            campos[pr.variable] = forms.DecimalField(**comunes)
        elif compuesto_anios_meses:
            campos[f"{pr.variable}_anios"] = forms.IntegerField(min_value=0, required=False, label=f"{label} (años)")
            campos[f"{pr.variable}_meses"] = forms.IntegerField(
                min_value=0, max_value=11, required=False, label=f"{label} (meses)",
            )
        else:
            campos[pr.variable] = forms.CharField(**comunes)

        regla_visible = _regla_visible(pr)
        metadata.append({
            "pregunta_relevamiento_id": pr.id,
            "pregunta_id": pr.pregunta_id,
            "variable": pr.variable,
            "seccion": pr.seccion.nombre,
            "tipo_pregunta": tipo_id,
            "compuesto_anios_meses": compuesto_anios_meses,
            "requerida": pr.requerida,
            "regla_visible": regla_visible,
            "regla_valido": pr.regla_valido,
            # la misma regla, para que el navegador oculte la pregunta (gdu/encuesta-form.html)
            "visible": json.dumps(regla_visible) if regla_visible else "",
            "opciones": {_coercion(tipo_id)(r.valor): r for r in pr.pregunta.opciones.all()},
        })

    EncuestaForm = type("EncuestaForm", (EncuestaBaseForm,), campos)
    EncuestaForm.pregunta_metadata = metadata
    return EncuestaForm


@transaction.atomic
def guardar_encuesta(relevamiento, vivienda, form, usuario):
    """
    Persiste una Encuesta + sus RespuestaEncuesta a partir de un form ya validado
    (equivalente a controllers/gql/save-encuesta.js::formatRespuestas). Cada envío crea una
    Encuesta nueva (no se edita en el lugar), igual que hacía el código original. Las
    preguntas ocultas por sus reglas no se guardan.
    """
    encuesta = Encuesta.objects.create(
        relevamiento=relevamiento,
        vivienda=vivienda,
        usuario=usuario,
        tipo=Encuesta.Tipo.WEB,
        capturada_en=timezone.now(),
    )

    respuestas = []
    for meta in form.pregunta_metadata:
        valor = form.datos.get(meta["variable"])
        if meta["variable"] not in form.visibles or valor is None:
            continue
        if meta["tipo_pregunta"] in TIPO_MULTIPLE_CHOICE_MULTIPLE:
            for opcion in valor:
                respuestas.append(RespuestaEncuesta(
                    encuesta=encuesta, pregunta_relevamiento_id=meta["pregunta_relevamiento_id"],
                    respuesta=meta["opciones"][opcion], valor=str(opcion),
                ))
            continue
        if meta["tipo_pregunta"] in TIPO_SI_NO:
            valor = "true" if valor else "false"
        respuestas.append(RespuestaEncuesta(
            encuesta=encuesta, pregunta_relevamiento_id=meta["pregunta_relevamiento_id"],
            respuesta=meta["opciones"].get(valor) if meta["tipo_pregunta"] in TIPO_MULTIPLE_CHOICE_UNICA else None,
            valor=str(valor),
        ))

    RespuestaEncuesta.objects.bulk_create(respuestas)
    return encuesta
