from django import forms
from personalizador import models
from core.widgets import DateHTMLWidget

class InstrumentoAgenteForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.InstrumentoAgente
		fields = (
			"instrumentoagente_tipo",
			"instrumentoagente_organismo",
			"instrumentoagente_numero",
			"instrumentoagente_fecha",
			"instrumentoagente_descripcion",
			"instrumentoagente",
		)
		widgets = {
			"instrumentoagente_tipo": forms.Select(attrs={"class": "form-control"}),
			"instrumentoagente_organismo": forms.TextInput(attrs={"class": "form-control"}),
			"instrumentoagente_numero": forms.TextInput(attrs={"class": "form-control"}),
			"instrumentoagente_fecha": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"instrumentoagente_descripcion": forms.TextInput(attrs={"class": "form-control"}),
			"instrumentoagente": forms.ClearableFileInput(attrs={"class": "form-control"}),
		}
