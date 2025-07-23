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
