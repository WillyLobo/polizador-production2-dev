from django import forms
from carga import models
from secretariador.forms.widgets import DateHTMLWidget

class ContratoMontoForm(forms.ModelForm):
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
