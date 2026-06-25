from django import forms
from carga import models
from carga.views.ajaxviews import obrawidget
from polizador.custom_forms import DateHTMLWidget

class PlandeTrabajoForm(forms.ModelForm):
	class Meta:
		model = models.PlanDeTrabajos
		fields = (
			"trabajos_obra",
			"trabajos_fecha",
		)
		widgets = {
			"trabajos_obra": obrawidget(attrs={"class": "form-control customSelect2"}),
			"trabajos_fecha": DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
		}
