from django import forms
from carga import models
from polizador.custom_forms import DateHTMLWidget

class ContratoMontoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.ContratoMonto
		fields = (
			"contratomonto_contrato",
			"contratomonto_rubro",
			"contratomonto_financiamiento",
			"contratomonto_pesos",
			"contratomonto_uvi",
			"contratomonto_uvi_fecha",
		)
		widgets = {
			"contratomonto_rubro":forms.Select(attrs={"class":"form-control"}),
			"contratomonto_financiamiento":forms.Select(attrs={"class":"form-control"}),
			"contratomonto_pesos": forms.NumberInput(attrs={"class":"form-control"}),
			"contratomonto_uvi": forms.NumberInput(attrs={"class": "form-control"}),
			"contratomonto_uvi_fecha": DateHTMLWidget(attrs={"type":"date", "class":"form-control"})
		}
