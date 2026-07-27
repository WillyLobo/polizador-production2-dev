from django import forms
from personalizador import models

class CEICForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.CEIC
		fields = (
			"ceic",
		)
		widgets = {
			"ceic": forms.TextInput(attrs={"class": "form-control"})
		}
