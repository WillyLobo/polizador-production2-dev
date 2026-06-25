from django import forms
from django.forms import inlineformset_factory
from carga import models
from carga.forms.plandetrabajositemforms import PlanDeTrabajosItemForm
from carga.views.ajaxviews import planwidget, rubrowidget

class PlanDeTrabajosRubroForm(forms.ModelForm):
	class Meta:
		model = models.PlanDeTrabajosRubro
		fields = (
			"rubro_plan",
			"rubro_nombre",
			"rubro_orden",
			"rubro_presupuesto",
			"rubro_anterior",
			"rubro_documento_digital",
		)
		widgets = {
			"rubro_plan": planwidget(attrs={"class": "form-control customSelect2"}),
			"rubro_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"rubro_orden": forms.NumberInput(attrs={"class": "form-control"}),
			"rubro_presupuesto": forms.NumberInput(attrs={"class": "form-control"}),
			"rubro_anterior": rubrowidget(attrs={"class": "form-control customSelect2"}),
			"rubro_documento_digital": forms.ClearableFileInput(attrs={"class": "form-control"}),
		}

class PlanDeTrabajosItemFormset(forms.models.BaseInlineFormSet):
	def clean(self):
		super().clean()
		total = 0
		for form in self.forms:
			if not hasattr(form, "cleaned_data"):
				continue
			if form.cleaned_data.get("DELETE"):
				continue
			incidencia = form.cleaned_data.get("planitem_incidencia_pct")
			if incidencia is not None:
				total += incidencia
		if total and abs(total - 100) > 0.5:
			raise forms.ValidationError(f"La suma de las incidencias de los items debe ser 100% (actual: {total}%).")

PlanDeTrabajosItemFormset = inlineformset_factory(
	parent_model=models.PlanDeTrabajosRubro,
	model=models.PlanDeTrabajosItem,
	form=PlanDeTrabajosItemForm,
	formset=PlanDeTrabajosItemFormset,
	fk_name="planitem_rubro",
	extra=1,
	can_delete=True,
)
