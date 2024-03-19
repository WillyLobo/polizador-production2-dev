from django.utils.safestring import SafeString
from django import forms
from carga import models

class ConjuntoForm(forms.ModelForm):
	class Meta:
		model = models.ConjuntoLicitado
		fields = (
			"conjunto_nombre",
			"conjunto_soluciones",
			"conjunto_resolucion",
			"conjunto_subconjunto"
		)
		widgets = {
			"conjunto_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"conjunto_soluciones":forms.NumberInput(attrs={"class":"form-control"}),
			"conjunto_resolucion":forms.TextInput(attrs={"class":"form-control"}),
			"conjunto_subconjunto":forms.Select(attrs={"class":"form-control customSelect2"})
		}

	def as_div(self):
		return SafeString(super().as_div().replace("<div>", "<div class='form-group>'"))