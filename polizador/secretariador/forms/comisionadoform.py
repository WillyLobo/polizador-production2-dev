from django import forms
from personalizador.models import ComisionadoExterno
from core.mixins import BaseFormMixin

class ComisionadoExternoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = ComisionadoExterno
        fields = (
            "agente_apellidos",
            "agente_nombres",
            "abreviatura",
            "sexo",
            "dni",
            "cuil",
            "institucion_origen",
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
            "dni":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
                }),
            "cuil":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "institucion_origen":forms.TextInput(attrs={
                "class":"form-control"
                }),
        }
