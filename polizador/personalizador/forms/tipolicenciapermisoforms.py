from django import forms
from personalizador import models

class TipoLicenciaPermisoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.TipoLicenciaPermiso
		fields = (
			"tipolicenciapermiso_categoria",
			"tipolicenciapermiso_nombre",
			"tipolicenciapermiso_articulo",
			"tipolicenciapermiso_unidad",
			"tipolicenciapermiso_tope_cantidad",
			"tipolicenciapermiso_tope_periodo",
			"tipolicenciapermiso_remunerada",
			"tipolicenciapermiso_antiguedad_meses",
			"tipolicenciapermiso_requiere_certificado",
			"tipolicenciapermiso_compensacion_horaria",
			"tipolicenciapermiso_observaciones",
			"tipolicenciapermiso_activo",
		)
		widgets = {
			"tipolicenciapermiso_categoria": forms.Select(attrs={"class": "form-control customSelect2"}),
			"tipolicenciapermiso_nombre": forms.TextInput(attrs={"class": "form-control"}),
			"tipolicenciapermiso_articulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Art. 10"}),
			"tipolicenciapermiso_unidad": forms.Select(attrs={"class": "form-control customSelect2"}),
			"tipolicenciapermiso_tope_cantidad": forms.NumberInput(attrs={"class": "form-control"}),
			"tipolicenciapermiso_tope_periodo": forms.Select(attrs={"class": "form-control customSelect2"}),
			"tipolicenciapermiso_remunerada": forms.Select(attrs={"class": "form-control customSelect2"}),
			"tipolicenciapermiso_antiguedad_meses": forms.NumberInput(attrs={"class": "form-control"}),
			"tipolicenciapermiso_requiere_certificado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"tipolicenciapermiso_compensacion_horaria": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"tipolicenciapermiso_observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
			"tipolicenciapermiso_activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
		}
