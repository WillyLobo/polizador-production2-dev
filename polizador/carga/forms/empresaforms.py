from django import forms
from carga import models

class EmpresaForm(forms.ModelForm):
	class Meta:
		model = models.Empresa
		fields = (
			"empresa_nombre",
			"empresa_cuit",
			"empresa_titular_titulo",
			"empresa_titular_nombre",
			"empresa_titular_dni",
			"empresa_direccion",
			"empresa_inscripcion",
			"empresa_correo_p",
			"empresa_correo_s"
		)
		widgets = {
			"empresa_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"empresa_cuit":forms.TextInput(attrs={"class":"form-control"}),
			"empresa_titular_titulo":forms.TextInput(attrs={"class":"form-control"}),
			"empresa_titular_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"empresa_titular_dni":forms.NumberInput(attrs={"class":"form-control"}),
			"empresa_direccion":forms.TextInput(attrs={"class":"form-control"}),
			"empresa_inscripcion":forms.TextInput(attrs={"class":"form-control"}),
			"empresa_correo_p":forms.EmailInput(attrs={"class":"form-control"}),
			"empresa_correo_s":forms.EmailInput(attrs={"class":"form-control"})
		}
