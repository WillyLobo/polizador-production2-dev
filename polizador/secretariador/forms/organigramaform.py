from django import forms
from django.utils.safestring import SafeString
from secretariador.models import Organigrama

class OrganigramaForm(forms.ModelForm):
    class Meta:
        model = Organigrama
        fields = (
            "organigrama_cargo",
            "organigrama_escalafon"
        )
        widgets = {
            "organigrama_cargo":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "organigrama_escalafon":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
                }),

        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
