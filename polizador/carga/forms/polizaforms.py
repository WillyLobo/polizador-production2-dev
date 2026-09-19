from django import forms
from django.forms.models import inlineformset_factory
from carga import models
from carga.forms.mixins import AddRelatedPermissionMixin
from carga.views.ajaxviews import obrawidget, empresawidget, aseguradorawidget, contratowidget
from core.widgets import DateHTMLWidget
from carga.models import Poliza, Poliza_Movimiento
from carga.views.ajaxviews import areawidget, polizawidget, receptorwidget


# class LegacyPolizaForm(forms.ModelForm):
# 	class Meta:
# 		model = models.LegacyPoliza
# 		fields = "__all__"

class PolizaForm(AddRelatedPermissionMixin, forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Poliza
		fields = (
			"poliza_fecha",
			"poliza_expediente",
			"poliza_numero",
			"poliza_concepto",
			"poliza_anexo",
			"poliza_recibo",
			"poliza_aseguradora",
			"poliza_tomador",
			"poliza_obra",
			"poliza_contrato",
			"poliza_financiamiento",
			"poliza_anticipo_pct",
			"poliza_monto_pesos",
			"poliza_monto_uvi",
			"poliza_digital",
		)

		widgets = {
			"poliza_fecha":DateHTMLWidget(attrs={"type":"date","class":"form-control", "autocomplete":"off"}),
			"poliza_expediente":forms.TextInput(attrs={"class":"form-control"}),
			"poliza_numero":forms.NumberInput(attrs={"class":"form-control"}),
			"poliza_concepto":forms.Select(attrs={"class":"form-control customSelect2"}),
			"poliza_anexo":forms.TextInput(attrs={"class":"form-control"}),
			"poliza_recibo":forms.TextInput(attrs={"class":"form-control"}),
			"poliza_aseguradora":aseguradorawidget(attrs={"class":"form-control customSelect2"}),
			"poliza_tomador":empresawidget(attrs={"class":"form-control customSelect2"}),
			"poliza_obra":obrawidget(attrs={"class":"form-control customSelect2"}),
			"poliza_contrato":contratowidget(
				attrs={"class":"form-control", "data-minimum-input-length": 0},
				dependent_fields={"poliza_obra": "contrato_obra"},
				max_results=10,
			),
			"poliza_financiamiento":forms.Select(attrs={"class":"form-control customSelect2"}),
			"poliza_anticipo_pct":forms.NumberInput(attrs={"class":"form-control", "step": "0.001"}),
			"poliza_monto_pesos":forms.NumberInput(attrs={"class":"form-control"}),
			"poliza_monto_uvi":forms.NumberInput(attrs={"class":"form-control"}),
			"poliza_digital":forms.FileInput(attrs={"class":"form-control"}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["poliza_contrato"].required = True
		self.fields["poliza_financiamiento"].required = True

class PolizaMovimientoForm(AddRelatedPermissionMixin, forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Poliza_Movimiento
		fields = (
			"poliza_movimiento_fecha",
			"poliza_movimiento_receptor",
			"poliza_movimiento_area",
			"poliza_movimiento_numero"
		)

		widgets = {
			"poliza_movimiento_fecha":DateHTMLWidget(attrs={"type":"date","class":"form-control", "autocomplete":"off"}),
			"poliza_movimiento_receptor":receptorwidget(attrs={"class":"form-control customSelect2"}),
			"poliza_movimiento_area":areawidget(attrs={"class":"form-control customSelect2"}),
			"poliza_movimiento_numero":polizawidget(attrs={"class":"form-control customSelect2"}),
		}

class PolizaMovimientoFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

PolizaMovimientoFormset = inlineformset_factory(
    parent_model = Poliza,
    model = Poliza_Movimiento,
    form = PolizaMovimientoForm,
    formset = PolizaMovimientoFormset,
    fk_name = "poliza_movimiento_numero",
    extra = 1,
    can_delete = False,
)
