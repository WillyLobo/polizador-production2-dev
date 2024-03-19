from django.utils.safestring import SafeString
from django import forms
from carga import models
from carga.views.ajaxviews import contratomontowidget

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
			"contratomonto_uvi_fecha": forms.DateInput(attrs={"class":"form-control"})
		}
	
	def as_div(self):
		return SafeString(super().as_div().replace("<div>", "<div class='col'>"))