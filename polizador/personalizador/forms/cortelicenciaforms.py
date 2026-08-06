from django import forms

from personalizador import models
from core.widgets import DateHTMLWidget

class CorteLicenciaForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.CorteLicencia
		fields = (
			"cortelicencia_licencia",
			"cortelicencia_fecha_reintegro",
			"cortelicencia_dias_gozados",
			"cortelicencia_dias_pendientes",
			"cortelicencia_fecha_vencimiento",
			"cortelicencia_motivo",
			"cortelicencia_nota_jurisdiccion",
			"cortelicencia_nota_numero",
			"cortelicencia_nota_ano",
			"cortelicencia_adjunto",
		)
		widgets = {
			"cortelicencia_licencia": forms.HiddenInput(),
			"cortelicencia_fecha_reintegro": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"cortelicencia_dias_gozados": forms.NumberInput(attrs={"class": "form-control"}),
			"cortelicencia_dias_pendientes": forms.NumberInput(attrs={"class": "form-control"}),
			"cortelicencia_fecha_vencimiento": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"cortelicencia_motivo": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
			"cortelicencia_nota_jurisdiccion": forms.TextInput(attrs={"class": "form-control"}),
			"cortelicencia_nota_numero": forms.NumberInput(attrs={"class": "form-control"}),
			"cortelicencia_nota_ano": forms.NumberInput(attrs={"class": "form-control"}),
		}
