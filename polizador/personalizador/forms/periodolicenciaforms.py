from django import forms

from personalizador import models
from core.widgets import DateHTMLWidget

class PeriodoLicenciaForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.PeriodoLicencia
		fields = (
			"periodolicencia_categoria",
			"periodolicencia_anio",
			"periodolicencia_apertura",
			"periodolicencia_fecha_limite_solicitud",
			"periodolicencia_turno1_desde",
			"periodolicencia_turno1_hasta",
			"periodolicencia_turno2_desde",
			"periodolicencia_turno2_hasta",
		)
		widgets = {
			"periodolicencia_categoria": forms.Select(attrs={"class": "form-control customSelect2"}),
			"periodolicencia_anio": forms.NumberInput(attrs={"class": "form-control"}),
			"periodolicencia_apertura": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"periodolicencia_fecha_limite_solicitud": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"periodolicencia_turno1_desde": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"periodolicencia_turno1_hasta": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"periodolicencia_turno2_desde": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"periodolicencia_turno2_hasta": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
		}
