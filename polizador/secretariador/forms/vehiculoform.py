from django import forms
from secretariador.models import Vehiculo
from secretariador.forms.mixins import BaseFormMixin

class VehiculoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = (
            "vehiculo_caracter",
            "vehiculo_modelo",
            "vehiculo_patente",
            "vehiculo_poliza",
            "vehiculo_poliza_aseguradora",
        )
        widgets = {
            "vehiculo_caracter":forms.Select(attrs={
                "class":"form-control",
                }),
            "vehiculo_modelo":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "vehiculo_patente":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "vehiculo_poliza":forms.TextInput(attrs={
                "class":"form-control",
                }),
            "vehiculo_poliza_aseguradora":forms.Select(attrs={
                "class":"form-control customSelect2",
                }),
        }