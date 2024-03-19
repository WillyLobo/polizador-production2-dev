from django.utils.safestring import SafeString
from django import forms
from carga import models

class MunicipioForm(forms.ModelForm):
	class Meta:
		model = models.Municipio
		fields = (
			"municipio_nombre",
			"id",
			"municipio_departamento",
			"municipio_region"
		)
		widgets = {
			"municipio_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"id":forms.NumberInput(attrs={"class":"form-control"}),
			"municipio_departamento":forms.Select(attrs={"class":"form-control customSelect2"}),
			"municipio_region":forms.Select(attrs={"class":"form-control"}),
		}

	def as_div(self):
		return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))