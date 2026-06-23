from django import forms
from django.forms import inlineformset_factory
from carga import models
from carga.forms.plandetrabajositemforms import PlanDeTrabajosItemForm
from carga.views.ajaxviews import obrawidget

class PlandeTrabajoForm(forms.ModelForm):
	class Meta:
		model = models.PlanDeTrabajos
		fields = (
			"trabajos_obra",
		)
		widgets = {
			"trabajos_obra": obrawidget(attrs={"class": "form-control customSelect2"}),
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
	parent_model=models.PlanDeTrabajos,
	model=models.PlanDeTrabajosItem,
	form=PlanDeTrabajosItemForm,
	formset=PlanDeTrabajosItemFormset,
	fk_name="planitem_plan",
	extra=1,
	can_delete=True,
)
