from django import forms
from personalizador import models
from personalizador.views.ajaxviews import agentewidget, directoriowidget, gerenciawidget

class DireccionForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Direccion
		fields = (
			"direccion_directorio",
			"direccion_gerencia",
			"direccion_nombre",
			"direccion_autoridad_a_cargo",
			"direccion_autoridad_a_cargo_fk",
			"direccion_cuof",
			"direccion_ungi",
			"direccion_responsabilidadprimaria",
		)
		widgets = {
			"direccion_directorio": directoriowidget(attrs={"class": "form-control customSelect2"}),
			"direccion_gerencia": gerenciawidget(attrs={"class": "form-control customSelect2"}),
			"direccion_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"direccion_autoridad_a_cargo": forms.TextInput(attrs={"class": "form-control"}),
			"direccion_autoridad_a_cargo_fk": agentewidget(attrs={"class": "form-control customSelect2"}),
			"direccion_cuof": forms.TextInput(attrs={"class": "form-control"}),
			"direccion_ungi": forms.TextInput(attrs={"class": "form-control"}),
			"direccion_responsabilidadprimaria": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}
