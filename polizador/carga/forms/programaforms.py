from django.utils.safestring import SafeString
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
	def as_div(self):
		return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))