from decimal import Decimal
from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from carga import models
from carga.views.ajaxviews import rubrowidget, agentemultiplewidget
from personalizador.models import Agente
from polizador.custom_forms import DateHTMLWidget

class FojaDeMedicionForm(forms.ModelForm):
	class Meta:
		model = models.FojaDeMedicion
		fields = (
			"foja_rubro",
			"foja_periodo",
			"foja_fecha",
			"foja_inspector",
			"foja_observaciones",
		)
		widgets = {
			"foja_rubro": rubrowidget(attrs={"class": "form-control customSelect2"}),
			"foja_periodo": DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
			"foja_fecha": DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
			"foja_inspector": agentemultiplewidget(attrs={"class": "form-control customSelect2"}),
			"foja_observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["foja_rubro"].queryset = models.PlanDeTrabajosRubro.objects.filter(
			rubro_plan__in=models.PlanDeTrabajos.vigentes()
		)

		rubro_id = self.data.get("foja_rubro") or self.initial.get("foja_rubro")
		if rubro_id:
			inspectores = Agente.objects.filter(
				obra_inspector__plandetrabajos__rubros__pk=rubro_id
			).distinct()
		else:
			inspectores = Agente.objects.none()

		self.fields["foja_inspector"].queryset = inspectores
		if not self.is_bound and not self.instance.pk:
			self.initial["foja_inspector"] = list(inspectores.values_list("pk", flat=True))

class FojaDeMedicionItemForm(forms.ModelForm):
	fojaitem_pct_anterior = forms.DecimalField(
		required=False,
		disabled=True,
		widget=forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
	)
	# Solo a fines de visualización: el acumulado real lo calcula siempre FojaDeMedicionItem.save().
	fojaitem_pct_acumulado = forms.DecimalField(
		required=False,
		disabled=True,
		widget=forms.NumberInput(attrs={"class": "form-control foja-acumulado", "readonly": True}),
	)

	class Meta:
		model = models.FojaDeMedicionItem
		fields = (
			"fojaitem_planitem",
			"fojaitem_pct_avance_mes",
		)
		widgets = {
			"fojaitem_planitem": forms.HiddenInput(),
			"fojaitem_pct_avance_mes": forms.NumberInput(attrs={"class": "form-control foja-mes"}),
		}

class BaseFojaDeMedicionItemFormset(BaseInlineFormSet):
	"""Valida los items de la Foja entre sí y contra la foja anterior del mismo rubro."""

	def _anterior_map(self):
		rubro_id = self.data.get("foja_rubro")
		if not rubro_id:
			return {}

		rubro = models.PlanDeTrabajosRubro.objects.filter(pk=rubro_id).first()
		if not rubro:
			return {}

		exclude_foja_numero = self.instance.foja_numero if self.instance.pk else None
		items = [
			form.cleaned_data.get("fojaitem_planitem")
			for form in self.forms
			if form.cleaned_data.get("fojaitem_planitem")
		]
		return models.FojaDeMedicion.anterior_items_map(
			rubro, items=items, exclude_foja_numero=exclude_foja_numero
		)

	def clean(self):
		super().clean()
		if any(self.errors):
			return

		anterior_map = self._anterior_map()
		total_anterior = total_mes = total_acumulado = Decimal("0")

		for form in self.forms:
			if not form.cleaned_data:
				continue

			planitem = form.cleaned_data.get("fojaitem_planitem")
			mes = form.cleaned_data.get("fojaitem_pct_avance_mes") or Decimal("0")
			anterior = anterior_map.get(planitem.pk, Decimal("0")) if planitem else Decimal("0")

			if planitem and anterior + mes > planitem.planitem_incidencia_pct:
				form.add_error(
					"fojaitem_pct_avance_mes",
					f"La suma de Anterior ({anterior}%) y Avance del Mes ({mes}%) no puede superar "
					f"la Incidencia del item ({planitem.planitem_incidencia_pct}%)."
				)

			total_anterior += anterior
			total_mes += mes
			total_acumulado += anterior + mes

		if total_anterior > 100:
			raise forms.ValidationError(f"La suma total de Anterior % no puede superar 100% (actual: {total_anterior}%).")
		if total_mes > 100:
			raise forms.ValidationError(f"La suma total de Avance del Mes % no puede superar 100% (actual: {total_mes}%).")
		if total_acumulado > 100:
			raise forms.ValidationError(f"La suma total de Acumulado % no puede superar 100% (actual: {total_acumulado}%).")

FojaDeMedicionItemFormset = inlineformset_factory(
	parent_model=models.FojaDeMedicion,
	model=models.FojaDeMedicionItem,
	form=FojaDeMedicionItemForm,
	formset=BaseFojaDeMedicionItemFormset,
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
		formset=BaseFojaDeMedicionItemFormset,
		fk_name="fojaitem_foja",
		extra=extra,
		can_delete=False,
	)
