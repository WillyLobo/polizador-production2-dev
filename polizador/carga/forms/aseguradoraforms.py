from django.utils.safestring import SafeString
from django import forms
from carga import models

class AseguradoraForm(forms.ModelForm):
	class Meta:
		model = models.Aseguradora
		fields = (
			"aseguradora_nombre",
		)
		widgets = {
			"aseguradora_nombre":forms.TextInput(attrs={"class":"form-control"})
		}
	def as_div(self):
		return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
