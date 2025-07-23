from django import forms
from carga.models import Contrato, ContratoMonto
from django.forms import inlineformset_factory
from carga.forms.contratomontoforms import *
from carga.views.ajaxviews import *
from secretariador.forms.widgets import DateHTMLWidget

class ContratoForm(forms.ModelForm):
	class Meta:
		model = Contrato
		fields = (
			"contrato_obra",
			"contrato_fecha",
			"contrato_descripcion",
			"contrato_resolucion",
			"contrato_decreto",
		)
		widgets = {
			"contrato_obra":obrawidget(attrs={"class":"form-control customSelect2"}),
			"contrato_fecha":DateHTMLWidget(attrs={"type":"date", "class":"form-control"}),
			"contrato_descripcion":forms.TextInput(attrs={"class":"form-control"}),
			"contrato_resolucion":forms.TextInput(attrs={"class":"form-control"}),
			"contrato_decreto":forms.TextInput(attrs={"class":"form-control"}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Labels for fields without them.
		self.fields["contrato_obra"].label = "Obra"
class ContratoMontoFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

ContratoMontoFormset = inlineformset_factory(
	parent_model=Contrato,
    model=ContratoMonto,
    form=ContratoMontoForm,
    formset=ContratoMontoFormset,
    fk_name="contratomonto_contrato",
    extra=1,
    can_delete=False,
)
