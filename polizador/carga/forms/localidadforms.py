from django import forms
from carga import models
from carga.views.ajaxviews import departamentowidget, municipiowidget 

class LocalidadForm(forms.ModelForm):
	class Meta:
		model = models.Localidad
		fields = (
			"localidad_nombre",
			"id",
			"localidad_centroide_lat",
			"localidad_centroide_lon",
			"localidad_funcion",
			"localidad_departamento",
			"localidad_municipio"
		)
		widgets = {
			"localidad_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"id":forms.NumberInput(attrs={"class":"form-control"}),
			"localidad_centroide_lat":forms.NumberInput(attrs={"class":"form-control"}),
			"localidad_centroide_lon":forms.NumberInput(attrs={"class":"form-control"}),
			"localidad_funcion":forms.TextInput(attrs={"class":"form-control"}),
			"localidad_departamento":departamentowidget(attrs={"class":"form-control customSelect2"}),
			"localidad_municipio":municipiowidget(attrs={"class":"form-control customSelect2"}),
		}
