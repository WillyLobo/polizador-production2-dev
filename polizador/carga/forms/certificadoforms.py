from django import forms
from django.core.exceptions import ValidationError
from carga import certificacion, models
from carga.views.ajaxviews import contratowidget, obrawidget
from polizador.custom_forms import DateHTMLWidget

class CustomClearableFileInput(forms.widgets.ClearableFileInput):
	# template_name = "clearable_file_input.html"
	pass

class CertificadoForm(forms.ModelForm):
	class Meta:
		model = models.Certificado
		fields = (
		"certificado_obra",
		"certificado_foja",
		"certificado_rubro_anticipo",
		"certificado_rubro_obra",
		"certificado_rubro_devanticipo",
		"certificado_rubro_db",
		"certificado_financiamiento",
		"certificado_expediente",
		"certificado_fecha",
		"certificado_mes_pct",
		"certificado_ante_pct",
		"certificado_acum_pct",
		"certificado_anticipo_pct",
		"certificado_monto_pesos",
		"certificado_devolucion_monto",
		"certificado_monto_uvi",
		"certificado_devolucion_monto_uvi",
		"certificado_devolucion_expte",
		"certificado_fondoreparo_pct",
		"certificado_digital",
		"certificado_fecha_carga_legacy"
		)

		widgets = {
		"certificado_obra":obrawidget(attrs={"class":"form-control customSelect2"}),
		"certificado_foja":forms.HiddenInput(),
		"certificado_rubro_anticipo":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_rubro_obra":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_rubro_devanticipo":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_rubro_db":forms.Select(attrs={"class":"form-control"}),
		"certificado_financiamiento":forms.Select(attrs={"class":"form-control"}),
		"certificado_expediente":forms.TextInput(attrs={"class":"form-control"}),
		"certificado_fecha":DateHTMLWidget(attrs={"type":"date","class":"form-control", "autocomplete":"off"}),
		"certificado_mes_pct":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_ante_pct":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_acum_pct":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_anticipo_pct":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_monto_pesos":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_devolucion_monto":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_monto_uvi":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_devolucion_monto_uvi":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_devolucion_expte":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_fondoreparo_pct":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_digital":CustomClearableFileInput(attrs={"class":"form-control"})
		}

class GenerarCertificadosDesdeFojaForm(forms.Form):
	"""Datos de actuación necesarios para generar los certificados Parciales de una Foja."""
	certificado_expediente = forms.CharField(
		label="Número de Expediente",
		max_length=18,
		widget=forms.TextInput(attrs={"class":"form-control"})
		)
	certificado_fecha = forms.DateField(
		label="Fecha",
		widget=DateHTMLWidget(attrs={"type":"date","class":"form-control", "autocomplete":"off"})
		)

class CertificadoAnticipoForm(forms.ModelForm):
	"""Certificado de Anticipo: no lleva Foja, se carga a mano un % del monto de contrato
	de la obra+financiamiento; el monto en pesos/UVI se deriva (ver certificacion.calcular_monto_anticipo)."""
	class Meta:
		model = models.Certificado
		fields = (
		"certificado_obra",
		"certificado_financiamiento",
		"certificado_expediente",
		"certificado_fecha",
		"certificado_anticipo_pct",
		"certificado_digital",
		)
		labels = {
		"certificado_anticipo_pct": "% de Anticipo",
		}
		widgets = {
		"certificado_obra":obrawidget(attrs={"class":"form-control customSelect2"}),
		"certificado_financiamiento":forms.Select(attrs={"class":"form-control"}),
		"certificado_expediente":forms.TextInput(attrs={"class":"form-control"}),
		"certificado_fecha":DateHTMLWidget(attrs={"type":"date","class":"form-control", "autocomplete":"off"}),
		"certificado_anticipo_pct":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_digital":CustomClearableFileInput(attrs={"class":"form-control"})
		}

	def clean(self):
		cleaned_data = super().clean()
		obra = cleaned_data.get("certificado_obra")
		financiamiento = cleaned_data.get("certificado_financiamiento")
		pct = cleaned_data.get("certificado_anticipo_pct")
		if obra and financiamiento and pct is not None:
			try:
				certificacion.validar_anticipo_nuevo(obra, financiamiento, pct)
			except ValidationError as error:
				raise forms.ValidationError(error.message)
		return cleaned_data

class CertificadoHechoConsumadoForm(forms.ModelForm):
	"""Certificado por Hecho Consumado: no lleva Foja, certifica directo contra un
	Contrato/Resolución de origen con un % cargado a mano (ver certificacion.calcular_monto_hecho_consumado)."""
	class Meta:
		model = models.Certificado
		fields = (
		"certificado_obra",
		"certificado_contrato_origen",
		"certificado_financiamiento",
		"certificado_rubro_db",
		"certificado_expediente",
		"certificado_fecha",
		"certificado_mes_pct",
		"certificado_fondoreparo_pct",
		"certificado_digital",
		)
		labels = {
		"certificado_mes_pct": "% Certificado",
		}
		widgets = {
		"certificado_obra":obrawidget(attrs={"class":"form-control customSelect2"}),
		"certificado_contrato_origen":contratowidget(attrs={"class":"form-control customSelect2"}),
		"certificado_financiamiento":forms.Select(attrs={"class":"form-control"}),
		"certificado_rubro_db":forms.Select(attrs={"class":"form-control"}),
		"certificado_expediente":forms.TextInput(attrs={"class":"form-control"}),
		"certificado_fecha":DateHTMLWidget(attrs={"type":"date","class":"form-control", "autocomplete":"off"}),
		"certificado_mes_pct":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_fondoreparo_pct":forms.NumberInput(attrs={"class":"form-control"}),
		"certificado_digital":CustomClearableFileInput(attrs={"class":"form-control"})
		}
