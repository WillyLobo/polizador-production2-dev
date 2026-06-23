from django import forms
from django.forms import inlineformset_factory
from carga import models
from carga.views.ajaxviews import planwidget, agentewidget
from polizador.custom_forms import DateHTMLWidget

class FojaDeMedicionForm(forms.ModelForm):
	class Meta:
		model = models.FojaDeMedicion
		fields = (
			"foja_plan",
			"foja_periodo",
			"foja_fecha",
			"foja_inspector",
			"foja_observaciones",
		)
		widgets = {
			"foja_plan": planwidget(attrs={"class": "form-control customSelect2"}),
			"foja_periodo": DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
			"foja_fecha": DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
			"foja_inspector": agentewidget(attrs={"class": "form-control customSelect2"}),
			"foja_observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}

class FojaDeMedicionItemForm(forms.ModelForm):
	class Meta:
		model = models.FojaDeMedicionItem
		fields = (
			"fojaitem_planitem",
			"fojaitem_pct_avance_mes",
			"fojaitem_pct_acumulado",
		)
		widgets = {
			"fojaitem_planitem": forms.HiddenInput(),
			"fojaitem_pct_avance_mes": forms.NumberInput(attrs={"class": "form-control foja-mes"}),
			"fojaitem_pct_acumulado": forms.NumberInput(attrs={"class": "form-control foja-acumulado"}),
		}

FojaDeMedicionItemFormset = inlineformset_factory(
	parent_model=models.FojaDeMedicion,
	model=models.FojaDeMedicionItem,
	form=FojaDeMedicionItemForm,
	fk_name="fojaitem_foja",
	extra=0,
	can_delete=False,
)

def build_foja_item_formset_class(extra):
	"""Formset con tantas filas extra como items tenga el Plan de Trabajos elegido."""
	return inlineformset_factory(
		parent_model=models.FojaDeMedicion,
		model=models.FojaDeMedicionItem,
		form=FojaDeMedicionItemForm,
		fk_name="fojaitem_foja",
		extra=extra,
		can_delete=False,
	)
