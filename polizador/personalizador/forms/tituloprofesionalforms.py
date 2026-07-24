from django import forms
from personalizador import models

class TituloProfesionalForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.TituloProfesional
		fields = (
			"tituloprofesional_nombre",
			"tituloprofesional_abreviatura",
			"tituloprofesional_grado",
		)
		widgets = {
			"tituloprofesional_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"tituloprofesional_abreviatura": forms.TextInput(attrs={"class": "form-control"}),
			"tituloprofesional_grado": forms.TextInput(attrs={"class": "form-control"}),
		}
