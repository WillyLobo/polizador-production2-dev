from django import forms
from personalizador import models
from personalizador.views.ajaxviews import agentewidget

class DirectorioForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Directorio
		fields = (
			"directorio_nombre",
			"directorio_autoridad_a_cargo",
			"directorio_autoridad_a_cargo_fk",
			"directorio_cuof",
			"directorio_ungi",
		)
		widgets = {
			"directorio_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"directorio_autoridad_a_cargo": forms.TextInput(attrs={"class": "form-control"}),
			"directorio_autoridad_a_cargo_fk": agentewidget(attrs={"class": "form-control customSelect2"}),
			"directorio_cuof": forms.TextInput(attrs={"class": "form-control"}),
			"directorio_ungi": forms.TextInput(attrs={"class": "form-control"}),
		}
