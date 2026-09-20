from django import forms
from django.core.exceptions import ValidationError

from carga import models
from carga.resolucion_texto import TextoResolucionError, compilar_bloque
from carga.views.ajaxviews import certificadomuestrawidget, programawidget

# Etiquetas de `clase` tal como las ve el usuario. El orden es el habitual de una
# resolución, para que el select se lea como el documento.
CLASE_CHOICES = (
    ("visto", "VISTO"),
    ("bloque", "Encabezado en negrita (CONSIDERANDO:, POR ELLO:, ...)"),
    ("considerando", "Considerando"),
    ("resuelve", "Fórmula «EL PRESIDENTE ... RESUELVE:»"),
    ("articulo", "Artículo"),
)

# La fórmula «EL PRESIDENTE ... RESUELVE:» es texto fijo del organismo: el bloque
# marca dónde va, no qué dice.
CLASES_SIN_TEXTO = ("resuelve",)


class TextoResolucionForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = models.TextoResolucionCertificado
        fields = (
            "textoresolucion_nombre",
            "textoresolucion_programa",
            "textoresolucion_financiamiento",
            "textoresolucion_tipo",
        )
        widgets = {
            "textoresolucion_nombre": forms.TextInput(attrs={"class": "form-control"}),
            "textoresolucion_programa": programawidget(attrs={"class": "form-control customSelect2"}),
            "textoresolucion_financiamiento": forms.Select(attrs={"class": "form-select"}),
            "textoresolucion_tipo": forms.Select(attrs={"class": "form-select"}),
        }


class BloqueForm(forms.Form):
    """Un bloque del cuerpo de la resolución.

    `texto` es fuente Jinja, no texto final: se valida que compile, pero no se
    renderiza acá (para eso hace falta un certificado de muestra)."""

    clase = forms.ChoiceField(label="Tipo", choices=CLASE_CHOICES, widget=forms.Select(attrs={"class": "form-select form-select-sm bloque-clase"}))
    label = forms.CharField(
        label="Etiqueta",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "automática"}),
        help_text="Sólo para artículos, y sólo si hace falta salirse de la numeración automática.",
    )
    texto = forms.CharField(
        label="Texto",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control form-control-sm bloque-texto", "rows": 3}),
    )

    def clean_texto(self):
        texto = self.cleaned_data.get("texto", "")
        try:
            compilar_bloque(texto)
        except TextoResolucionError as e:
            # Sin esta validación un `{%` suelto rompe la ficha de todos los
            # certificados que caen en el alcance de esta plantilla.
            raise ValidationError(str(e)) from e
        return texto

    def clean(self):
        cleaned = super().clean()
        clase = cleaned.get("clase")
        texto = (cleaned.get("texto") or "").strip()
        if clase and clase not in CLASES_SIN_TEXTO and not texto:
            self.add_error("texto", "Este tipo de bloque necesita texto.")
        return cleaned


class BaseBloqueFormSet(forms.BaseFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if not self.bloques_validos():
            raise ValidationError("La resolución tiene que tener al menos un bloque.")

    def bloques_validos(self):
        """Los bloques que se guardan: los que el usuario no marcó para borrar."""
        bloques = []
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue
            clase = form.cleaned_data["clase"]
            bloques.append({
                "clase": clase,
                "label": form.cleaned_data.get("label", "").strip(),
                "texto": "" if clase in CLASES_SIN_TEXTO else form.cleaned_data.get("texto", ""),
            })
        return bloques


BloqueFormSet = forms.formset_factory(BloqueForm, formset=BaseBloqueFormSet, extra=0, can_delete=True)


class CertificadoMuestraForm(forms.Form):
    """Elige contra qué certificado se previsualiza la plantilla.

    Hace falta porque la plantilla se edita a nivel de alcance (programa,
    financiamiento, tipo), donde no hay ningún certificado del que sacar valores."""

    certificado = forms.ModelChoiceField(
        label="Certificado de muestra",
        queryset=models.Certificado.objects.select_related("certificado_obra"),
        required=False,
        widget=certificadomuestrawidget(attrs={"class": "form-control customSelect2", "data-placeholder": "Buscar por expediente u obra..."}),
        help_text="Sólo para la vista previa: no se guarda con la plantilla.",
    )


# Bloques con los que arranca una plantilla nueva, para no enfrentar al usuario con
# una pantalla en blanco. Es el esqueleto de cualquier resolución del organismo.
BLOQUES_INICIALES = [
    {"clase": "visto", "label": "", "texto": "El Expediente N° {{ certificado.expediente }}, por el cual se tramita el {{ certificado.tipo }} de la obra: «{{ obra.nombre }}»;"},
    {"clase": "bloque", "label": "", "texto": "CONSIDERANDO:"},
    {"clase": "considerando", "label": "", "texto": "Que la Empresa {{ empresa.nombre }} (CUIT {{ empresa.cuit|cuit }}) es la contratista de la obra «{{ obra.nombre }}», adjudicada por {{ obra.resolucion }};"},
    {"clase": "considerando", "label": "", "texto": "Que corresponde aprobar el certificado del período {{ certificado.periodo }}, por un monto de {{ certificado.monto_pesos|pesos }} ({{ certificado.monto_pesos|letras }});"},
    {"clase": "bloque", "label": "", "texto": "Por ello;"},
    {"clase": "resuelve", "label": "", "texto": ""},
    {"clase": "articulo", "label": "", "texto": "Apruébase el {{ certificado.tipo }} N° {{ certificado.numero_obra }} de la obra «{{ obra.nombre }}», por la suma de {{ certificado.monto_pesos|pesos }}."},
    {"clase": "articulo", "label": "", "texto": "El gasto emergente de lo dispuesto en la presente Resolución deberá imputarse a la partida específica del Instituto, según la naturaleza de este."},
    {"clase": "articulo", "label": "", "texto": "Regístrese, comuníquese y archívese."},
]


class BloqueTextoForm(forms.Form):
    """Un bloque del texto YA RESUELTO de un certificado concreto.

    A diferencia de `BloqueForm`, acá el texto es final, no una plantilla: no se
    compila como Jinja (unas llaves sueltas en el texto de una resolución son
    llaves, no un error) y la clase no se puede cambiar — la estructura del
    documento la fija la plantilla, acá se retoca la redacción."""

    clase = forms.CharField(widget=forms.HiddenInput())
    label = forms.CharField(required=False, widget=forms.HiddenInput())
    texto = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )


class BaseBloqueTextoFormSet(forms.BaseFormSet):
    def bloques(self):
        return [
            {
                "clase": form.cleaned_data["clase"],
                "label": form.cleaned_data.get("label", ""),
                "texto": form.cleaned_data.get("texto", ""),
            }
            for form in self.forms
            if form.cleaned_data
        ]


BloqueTextoFormSet = forms.formset_factory(BloqueTextoForm, formset=BaseBloqueTextoFormSet, extra=0)
