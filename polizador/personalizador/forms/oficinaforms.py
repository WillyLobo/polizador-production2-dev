from django import forms
from personalizador import models
from personalizador.views.ajaxviews import (
	directoriowidget,
	oficina_gerenciawidget, oficina_direccionwidget, oficina_departamentowidget,
)

class OficinaForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Oficina
		fields = (
			"cargo_directorio",
			"cargo_gerencia",
			"cargo_direccion",
			"cargo_departamento",
		)
		widgets = {
			"cargo_directorio": directoriowidget(attrs={"class": "form-control customSelect2"}),
			"cargo_gerencia": oficina_gerenciawidget(attrs={"class": "form-control customSelect2"}),
			"cargo_direccion": oficina_direccionwidget(attrs={"class": "form-control customSelect2"}),
			"cargo_departamento": oficina_departamentowidget(attrs={"class": "form-control customSelect2"}),
		}
