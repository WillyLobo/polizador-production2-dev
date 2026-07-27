from django import forms
from personalizador import models

class ApartadoCargoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.ApartadoCargo
		fields = (
			"apartadocargo_denominacion",
		)
		widgets = {
			"apartadocargo_denominacion": forms.TextInput(attrs={"class": "form-control"})
		}
