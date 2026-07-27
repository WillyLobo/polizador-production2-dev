from django import forms
from personalizador import models

class GrupoCargoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.GrupoCargo
		fields = (
			"grupo_numero",
		)
		widgets = {
			"grupo_numero": forms.NumberInput(attrs={"class": "form-control"})
		}
