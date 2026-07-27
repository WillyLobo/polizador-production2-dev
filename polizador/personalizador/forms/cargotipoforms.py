from django import forms
from personalizador import models

class CargoTipoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.CargoTipo
		fields = (
			"cargotipo",
		)
		widgets = {
			"cargotipo": forms.TextInput(attrs={"class": "form-control"})
		}
