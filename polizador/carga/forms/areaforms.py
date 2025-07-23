from django import forms
from carga import models

class AreaForm(forms.ModelForm):
	class Meta:
		model = models.Area
		fields = (
			"area_nombre",
		)
		widgets = {
			"area_nombre":forms.TextInput(attrs={"class":"form-control"})
		}
