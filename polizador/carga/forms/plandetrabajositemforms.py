from django import forms
from carga import models

class PlanDeTrabajosItemForm(forms.ModelForm):
	class Meta:
		model = models.PlanDeTrabajosItem
		fields = (
			"planitem_orden",
			"planitem_nombre",
			"planitem_incidencia_pct",
		)
		widgets = {
			"planitem_orden": forms.NumberInput(attrs={"class": "form-control"}),
			"planitem_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"planitem_incidencia_pct": forms.NumberInput(attrs={"class": "form-control"}),
		}
	
	def clean(self):
		super().clean()
		planitem_nombre = self.cleaned_data.get("planitem_nombre")
		if planitem_nombre:
			self.cleaned_data["planitem_nombre"] = str(planitem_nombre).upper()
		return self.cleaned_data