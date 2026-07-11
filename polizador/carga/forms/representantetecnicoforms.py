from django import forms
from personalizador import models

class RepresentanteTecnicoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.RepresentanteTecnico
		fields = (
			"representantetecnico_nombre",
			"representantetecnico_apellido",
			"representantetecnico_dni",
			"representantetecnico_cuil",
			"representantetecnico_email",
			"representantetecnico_telefono",
			"representantetecnico_profesion",
			"representantetecnico_matricula",
		)
		widgets = {
			"representantetecnico_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"representantetecnico_apellido":forms.TextInput(attrs={"class":"form-control"}),
			"representantetecnico_dni":forms.NumberInput(attrs={"class":"form-control"}),
			"representantetecnico_cuil":forms.TextInput(attrs={"class":"form-control"}),
			"representantetecnico_email":forms.EmailInput(attrs={"class":"form-control"}),
			"representantetecnico_telefono":forms.TextInput(attrs={"class":"form-control"}),
			"representantetecnico_profesion":forms.Select(attrs={"class":"form-control customSelect2"}),
			"representantetecnico_matricula":forms.TextInput(attrs={"class":"form-control"}),
		}
