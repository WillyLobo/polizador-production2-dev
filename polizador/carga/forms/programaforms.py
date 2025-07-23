from django import forms
from carga import models

class ProgramaForm(forms.ModelForm):
	class Meta:
		model = models.Programa
		fields = (
			"programa_nombre",
		)
		widgets = {
			"programa_nombre":forms.TextInput(attrs={"class":"form-control"})
		}
