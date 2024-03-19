from django import forms
from carga import models

class PlandeTrabajoForm(forms.ModelForm):
	class Meta:
		model = models.PlanDeTrabajos
		fields = "__all__"
