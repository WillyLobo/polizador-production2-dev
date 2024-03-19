from django import forms
from carga.models import Contrato, ContratoMonto
from django.forms import inlineformset_factory
from carga.forms.contratomontoforms import *
from carga.views.ajaxviews import *

class ContratoForm(forms.ModelForm):
	class Meta:
		model = Contrato
		fields = (
			"contrato_obra",
			"contrato_fecha",
			"contrato_descripcion",
			"contrato_resolucion",
			"contrato_decreto",
		)
		widgets = {
			"contrato_obra":obrawidget(attrs={"class":"form-control customSelect2"}),
			"contrato_fecha":forms.DateInput(attrs={"class":"form-control"}),
			"contrato_descripcion":forms.TextInput(attrs={"class":"form-control"}),
			"contrato_resolucion":forms.TextInput(attrs={"class":"form-control"}),
			"contrato_decreto":forms.TextInput(attrs={"class":"form-control"}),
		}
	def as_div(self):
		return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

ContratoFormset = inlineformset_factory(
					Contrato,
					ContratoMonto,
					form = ContratoMontoForm,
					extra=1)