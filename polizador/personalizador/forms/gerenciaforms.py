from django import forms
from personalizador import models
from personalizador.views.ajaxviews import agentewidget, directoriowidget

class GerenciaForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Gerencia
		fields = (
			"gerencia_directorio",
			"gerencia_nombre",
			"gerencia_autoridad_a_cargo",
			"gerencia_autoridad_a_cargo_fk",
			"gerencia_cuof",
			"gerencia_ungi",
			"gerencia_responsabilidadprimaria",
		)
		widgets = {
			"gerencia_directorio": directoriowidget(attrs={"class": "form-control customSelect2"}),
			"gerencia_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"gerencia_autoridad_a_cargo": forms.TextInput(attrs={"class": "form-control"}),
			"gerencia_autoridad_a_cargo_fk": agentewidget(attrs={"class": "form-control customSelect2"}),
			"gerencia_cuof": forms.TextInput(attrs={"class": "form-control"}),
			"gerencia_ungi": forms.TextInput(attrs={"class": "form-control"}),
			"gerencia_responsabilidadprimaria": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}
