from django import forms
from carga import models

class ProgramaForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Programa
		fields = (
			"programa_nombre",
		)
		widgets = {
			"programa_nombre":forms.TextInput(attrs={"class":"form-control"})
		}
