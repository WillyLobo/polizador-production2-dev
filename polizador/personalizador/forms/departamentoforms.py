from django import forms
from personalizador import models
from personalizador.views.ajaxviews import agentewidget, directoriowidget, gerenciawidget, direccionwidget

class DepartamentoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Departamento
		fields = (
			"departamento_directorio",
			"departamento_gerencia",
			"departamento_direccion",
			"departamento_nombre",
			"departamento_autoridad_a_cargo",
			"departamento_autoridad_a_cargo_fk",
			"departamento_cuof",
			"departamento_ungi",
			"departamento_responsabilidadprimaria",
		)
		widgets = {
			"departamento_directorio": directoriowidget(attrs={"class": "form-control customSelect2"}),
			"departamento_gerencia": gerenciawidget(attrs={"class": "form-control customSelect2"}),
			"departamento_direccion": direccionwidget(attrs={"class": "form-control customSelect2"}),
			"departamento_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"departamento_autoridad_a_cargo": forms.TextInput(attrs={"class": "form-control"}),
			"departamento_autoridad_a_cargo_fk": agentewidget(attrs={"class": "form-control customSelect2"}),
			"departamento_cuof": forms.TextInput(attrs={"class": "form-control"}),
			"departamento_ungi": forms.TextInput(attrs={"class": "form-control"}),
			"departamento_responsabilidadprimaria": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}
