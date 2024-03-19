from django.utils.safestring import SafeString
from django import forms
from carga import models

class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = models.Departamento
		fields = (
			"id",
			"departamento_nombre",
		)
		widgets = {
			"id":forms.NumberInput(attrs={"class":"form-control"}),
			"departamento_nombre":forms.TextInput(attrs={"class":"form-control"})
		}

	def as_div(self):
		return SafeString(super().as_div().replace("<div>","<div class='form-group'>"))