from django import forms
from personalizador.models import Agente
from secretariador.forms.mixins import BaseFormMixin
from polizador.custom_forms import CustomCheckboxInput

class ComisionadoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Agente
        fields = (
            "agente_apellidos",
            "agente_nombres",
            "abreviatura",
            "sexo",
            "oficina",
            "dni",
            "cuil",
            "agente_personal_transitorio",
            "agente_personal_de_gabinete",
        )
        widgets = {
            "agente_nombres":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "agente_apellidos":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "abreviatura":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "sexo":forms.Select(attrs={
                "class":"form-control",
                }),
            "oficina":forms.Select(attrs={
                "class":"form-control",
                }),
            "dni":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
                }),
            "cuil":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "agente_personal_transitorio":CustomCheckboxInput(attrs={
                "class":"form-check-input"
                }),
            "agente_personal_de_gabinete":CustomCheckboxInput(attrs={
                "class":"form-check-input"
                }),
        }
