from django import forms
from django.forms import inlineformset_factory
from carga import models
from carga.forms.plandetrabajositemforms import PlanDeTrabajosItemForm
from carga.views.ajaxviews import planwidget, contratomontowidget, rubroanteriorwidget

class PlanDeTrabajosRubroForm(forms.ModelForm):
	class Meta:
		model = models.PlanDeTrabajosRubro
		fields = (
			"rubro_plan",
			"rubro_nombre",
			"rubro_orden",
			"rubro_presupuesto",
			"rubro_contratomonto",
			"rubro_anterior",
			"rubro_foja_numero_inicial",
			"rubro_documento_digital",
		)
		widgets = {
			"rubro_plan": planwidget(attrs={"class": "form-control customSelect2"}),
			"rubro_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"rubro_orden": forms.NumberInput(attrs={"class": "form-control"}),
			"rubro_presupuesto": forms.NumberInput(attrs={"class": "form-control"}),
			"rubro_contratomonto": contratomontowidget(
				attrs={"class": "form-control customSelect2"}
				),
			"rubro_anterior": rubroanteriorwidget(
				attrs={"class": "form-control customSelect2"}
				),
			"rubro_foja_numero_inicial": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
			"rubro_documento_digital": forms.ClearableFileInput(attrs={"class": "form-control"}),
		}

	def __init__(self, *args, **kwargs):
		self.pedir_foja_numero_inicial = kwargs.pop("pedir_foja_numero_inicial", False)
		super().__init__(*args, **kwargs)
		if not self.pedir_foja_numero_inicial:
			self.fields["rubro_foja_numero_inicial"].disabled = True
			self.fields["rubro_foja_numero_inicial"].required = False

	def clean(self):
		cleaned_data = super().clean()
		# Si hay rubro_anterior (o no corresponde preguntarlo), la numeración la determina
		# la cadena de reprogramaciones, no este campo: se fuerza a 1 para no dejar valores
		# espurios ingresados antes de elegir un rubro_anterior en el mismo submit.
		if cleaned_data.get("rubro_anterior") or not self.pedir_foja_numero_inicial:
			cleaned_data["rubro_foja_numero_inicial"] = 1
			self.instance.rubro_foja_numero_inicial = 1
		return cleaned_data

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
