from django.utils.safestring import SafeString
from django import forms
from carga import models

class RegionForm(forms.ModelForm):
	class Meta:
		model = models.Region
		fields = (
			"region_numero",
		)
		widgets = {
			"region_numero":forms.NumberInput(attrs={"class":"form-control"})
		}
	def as_div(self):
		return SafeString(super().as_div().replace("<div>","<div class='form-group'>"))