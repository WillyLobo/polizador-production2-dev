from django import forms
from carga import models
from carga.views.ajaxviews import obrawidget, empresawidget

class PolizaForm(forms.ModelForm):
	CONCEPTO = (
		("C", "Garantía de Ejecución de Contrato"),
		("F", "Garantía de Sustitución de Fondo de Reparo"),
		("A", "Garantía de Anticipo Financiero")
	)
	poliza_fecha	= forms.DateField(input_formats=["%d/%m/%Y"], localize=True)
	poliza_concepto = forms.ChoiceField(choices=CONCEPTO)
	
	class Meta:
		model = models.Poliza
		fields = "__all__"

		widgets = {
			"poliza_obra":obrawidget,
			"poliza_tomador":empresawidget,
		}

class LegacyPolizaForm(forms.ModelForm):
	CONCEPTO = (
        ("C", "Garantía de Ejecución de Contrato"),
        ("F", "Garantía de Sustitución de Fondo de Reparo"),
        ("A", "Garantía de Anticipo Financiero")
    )
	legacy_poliza_concepto = forms.ChoiceField(choices=CONCEPTO)
	legacy_poliza_fecha	= forms.DateField(input_formats=['%d/%m/%Y'], localize=True)
	
	class Meta:
		model = models.LegacyPoliza
		fields = "__all__"

class PolizaMovimientoForm(forms.ModelForm):
	class Meta:
		model = models.Poliza_Movimiento
		fields = ("poliza_movimiento_fecha", "poliza_movimiento_receptor", "poliza_movimiento_area", "poliza_movimiento_numero")