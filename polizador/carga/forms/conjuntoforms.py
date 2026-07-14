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
			"conjunto_resolucion",
			"conjunto_resolucion_fk",
			"conjunto_subconjunto"
		)
		widgets = {
			"conjunto_nombre":forms.TextInput(attrs={"class":"form-control"}),
			"conjunto_soluciones":forms.NumberInput(attrs={"class":"form-control"}),
			"conjunto_resolucion":forms.TextInput(attrs={"class":"form-control"}),
			"conjunto_resolucion_fk":ResolucionWidget(attrs={"class":"form-control customSelect2"}),
			"conjunto_subconjunto":forms.Select(attrs={"class":"form-control customSelect2"})
		}
