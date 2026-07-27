from django import forms
from personalizador import models

class DenominacionCargoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.DenominacionCargo
		fields = (
			"denominacion",
		)
		widgets = {
			"denominacion": forms.TextInput(attrs={"class": "form-control"})
		}
