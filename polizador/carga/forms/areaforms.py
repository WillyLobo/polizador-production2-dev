from django import forms
from carga import models

class AreaForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Area
		fields = (
			"area_nombre",
		)
		widgets = {
			"area_nombre":forms.TextInput(attrs={"class":"form-control"})
		}
