from django import forms
from django.forms import inlineformset_factory
from carga import models

class ContratoTramoPagoForm(forms.ModelForm):
	class Meta:
		model = models.ContratoTramoPago
		fields = (
			"tramo_pct_pago",
			"tramo_pct_disparador",
		)
		widgets = {
			"tramo_pct_pago": forms.NumberInput(attrs={"class": "form-control"}),
			"tramo_pct_disparador": forms.NumberInput(attrs={"class": "form-control"}),
		}

class ContratoTramoPagoFormset(forms.models.BaseInlineFormSet):
	def clean(self):
		super().clean()
		total_pct_pago = 0
		disparador_anterior = None
		for form in self.forms:
			if not hasattr(form, "cleaned_data"):
				continue
			if form.cleaned_data.get("DELETE"):
				continue
			pct_pago = form.cleaned_data.get("tramo_pct_pago")
			if pct_pago is not None:
				total_pct_pago += pct_pago
			disparador = form.cleaned_data.get("tramo_pct_disparador")
			if disparador is not None:
				if disparador_anterior is not None and disparador < disparador_anterior:
					raise forms.ValidationError(
						"El % de Avance Acumulado que dispara cada tramo debe ser no decreciente "
						"entre tramos."
					)
				disparador_anterior = disparador
		if total_pct_pago and abs(total_pct_pago - 100) > 0.5:
			raise forms.ValidationError(
				f"La suma de los % a certificar de los tramos debe ser 100% (actual: {total_pct_pago}%)."
			)

ContratoTramoPagoFormset = inlineformset_factory(
	parent_model=models.Contrato,
	model=models.ContratoTramoPago,
	form=ContratoTramoPagoForm,
	formset=ContratoTramoPagoFormset,
	fk_name="tramo_contrato",
	extra=1,
	can_delete=True,
)
