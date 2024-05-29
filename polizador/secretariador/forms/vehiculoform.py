from django import forms
from django.utils.safestring import SafeString
from secretariador.models import Vehiculo

class VehiculoForm(forms.ModelForm):
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

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
