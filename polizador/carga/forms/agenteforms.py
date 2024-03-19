from django.utils.safestring import SafeString
from django import forms
from carga import models

class AgenteForm(forms.ModelForm):
	class Meta:
		model = models.Agente
		fields = (
			"agente_nombre",
			"agente_apellido",
			"agente_dni",
			"agente_telefono",
			"agente_email",
			"agente_profesion",
			"agente_matricula",
		)

		widgets = {
			"agente_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"agente_apellido":forms.TextInput(attrs={"class":"form-control"}),
			"agente_dni":forms.NumberInput(attrs={"class":"form-control"}),
			"agente_telefono":forms.NumberInput(attrs={"class":"form-control"}),
			"agente_email":forms.EmailInput(attrs={"class":"form-control"}),
			"agente_profesion":forms.Select(attrs={"class":"form-control"}),
			"agente_matricula":forms.NumberInput(attrs={"class":"form-control"})
		}
	
	def as_div(self):
		return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))