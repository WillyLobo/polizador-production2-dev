from django import forms
from carga import models
from carga.views.ajaxviews import obrawidget, contratowidget
from polizador.custom_forms import DateHTMLWidget

class PlandeTrabajoForm(forms.ModelForm):
	class Meta:
		model = models.PlanDeTrabajos
		fields = (
			"trabajos_obra",
			"trabajos_fecha",
			"trabajos_meses",
			"trabajos_contrato",
		)
		widgets = {
			"trabajos_obra": obrawidget(attrs={"class": "form-control customSelect2"}),
			"trabajos_fecha": DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
			"trabajos_meses": forms.NumberInput(attrs={"class": "form-control"}),
			"trabajos_contrato": contratowidget(
				attrs={"class": "form-control", "data-minimum-input-length": 0},
				dependent_fields={"trabajos_obra": "contrato_obra"},
				max_results=10,
			),
		}
