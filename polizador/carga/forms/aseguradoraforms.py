from django import forms
from carga import models

class AseguradoraForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Aseguradora
		fields = (
			"aseguradora_nombre",
		)
		widgets = {
			"aseguradora_nombre":forms.TextInput(attrs={"class":"form-control"})
		}
