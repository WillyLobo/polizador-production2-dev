from django import forms
from django.utils.safestring import SafeString
from secretariador.models import Comisionado

class ComisionadoForm(forms.ModelForm):
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
        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
