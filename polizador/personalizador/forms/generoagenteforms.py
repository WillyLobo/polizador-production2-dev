from django import forms
from personalizador import models

class GeneroAgenteForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.GeneroAgente
		fields = (
			"generoagente_nombre",
		)
		widgets = {
			"generoagente_nombre": forms.TextInput(attrs={"class": "form-control"})
		}
