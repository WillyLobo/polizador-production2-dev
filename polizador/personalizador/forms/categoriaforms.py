from django import forms
from personalizador import models

class CategoriaForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Categoria
		fields = (
			"categoria_codigo",
			"categoria_nombre",
		)
		widgets = {
			"categoria_codigo": forms.NumberInput(attrs={"class": "form-control"}),
			"categoria_nombre": forms.TextInput(attrs={"class": "form-control"}),
		}
