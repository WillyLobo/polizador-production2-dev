from django import forms
from secretariador.models import Comisionado
from secretariador.forms.mixins import BaseFormMixin

class ComisionadoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Comisionado
        fields = (
            "comisionado_apellidos",
            "comisionado_nombres",
            "comisionado_abreviatura",
            "comisionado_sexo",
            "comisionado_cargo",
            "comisionado_dni",
            "comisionado_cuit",
            "comisionado_personal_transitorio",
        )
        widgets = {
            "comisionado_nombres":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "comisionado_apellidos":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "comisionado_abreviatura":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "comisionado_sexo":forms.Select(attrs={
                "class":"form-control",
                }),
            "comisionado_cargo":forms.Select(attrs={
                "class":"form-control",
                }),
            "comisionado_dni":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
                }),
            "comisionado_cuit":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "comisionado_personal_transitorio":forms.CheckboxInput(attrs={
                "class":"form-check-input"
                }),
        }