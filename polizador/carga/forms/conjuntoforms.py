from django import forms
from carga import models
from secretariador.views.ajaxviews import ResolucionWidget

class ConjuntoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.ConjuntoLicitado
		fields = (
			"conjunto_nombre",
			"conjunto_soluciones",
			"conjunto_resolucion_tipo",
			"conjunto_resolucion_ano",
			"conjunto_resolucion_numero",
			"conjunto_resolucion_jurisdiccion",
			"conjunto_resolucion_acta",
			"conjunto_resolucion_fk",
			"conjunto_subconjunto"
		)
		widgets = {
			"conjunto_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"conjunto_soluciones":forms.NumberInput(attrs={"class":"form-control"}),
			"conjunto_resolucion_tipo":forms.Select(attrs={"class":"form-control"}),
			"conjunto_resolucion_ano":forms.TextInput(attrs={"class":"form-control", "placeholder":"Año"}),
			"conjunto_resolucion_numero":forms.TextInput(attrs={"class":"form-control", "placeholder":"Número"}),
			"conjunto_resolucion_jurisdiccion":forms.TextInput(attrs={"class":"form-control", "placeholder":"Jurisdicción"}),
			"conjunto_resolucion_acta":forms.TextInput(attrs={"class":"form-control", "placeholder":"Acta"}),
			"conjunto_resolucion_fk":ResolucionWidget(attrs={"class":"form-control customSelect2"}),
			"conjunto_subconjunto":forms.Select(attrs={"class":"form-control customSelect2"})
		}
