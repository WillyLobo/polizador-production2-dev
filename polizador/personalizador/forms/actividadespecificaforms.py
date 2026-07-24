from django import forms
from personalizador import models

class ActividadEspecificaForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.ActividadEspecifica
		fields = (
			"actividad_especifica_codigo",
			"actividad_especifica_nombre",
		)
		widgets = {
			"actividad_especifica_codigo": forms.NumberInput(attrs={"class": "form-control"}),
			"actividad_especifica_nombre": forms.TextInput(attrs={"class": "form-control"}),
		}
