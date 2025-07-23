from django import forms
from carga import models

class ReceptorForm(forms.ModelForm):
	class Meta:
		model = models.Receptor
		fields = (
			"receptor_nombre",
		)
		widgets = {
			"receptor_nombre":forms.TextInput(attrs={"class":"form-control"})
		}
