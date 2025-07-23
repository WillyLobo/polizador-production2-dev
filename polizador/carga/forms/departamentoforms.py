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
