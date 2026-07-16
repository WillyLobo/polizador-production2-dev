from django import forms
from secretariador.models import Organigrama
from core.mixins import BaseFormMixin

class OrganigramaForm(BaseFormMixin, forms.ModelForm):
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