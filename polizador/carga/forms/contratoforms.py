from django import forms
from carga.models import Contrato, ContratoMonto
from django.forms import inlineformset_factory
from carga.forms.contratomontoforms import *
from carga.views.ajaxviews import *
from secretariador.views.ajaxviews import ResolucionWidget
from core.widgets import DateHTMLWidget

class ContratoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = Contrato
		fields = (
			"contrato_obra",
			"contrato_fecha",
			"contrato_descripcion",
			"contrato_resolucion_tipo",
			"contrato_resolucion_ano",
			"contrato_resolucion_numero",
			"contrato_resolucion_jurisdiccion",
			"contrato_resolucion_acta",
			"contrato_resolucion_fk",
			"contrato_decreto",
			"contrato_certificacion_por_etapas",
		)
		widgets = {
			"contrato_obra":obrawidget(attrs={"class":"form-control customSelect2"}),
			"contrato_fecha":DateHTMLWidget(attrs={"type":"date", "class":"form-control"}),
			"contrato_descripcion":forms.TextInput(attrs={"class":"form-control"}),
			"contrato_resolucion_tipo":forms.Select(attrs={"class":"form-control"}),
			"contrato_resolucion_ano":forms.TextInput(attrs={"class":"form-control", "placeholder":"Año"}),
			"contrato_resolucion_numero":forms.TextInput(attrs={"class":"form-control", "placeholder":"Número"}),
			"contrato_resolucion_jurisdiccion":forms.TextInput(attrs={"class":"form-control", "placeholder":"Jurisdicción"}),
			"contrato_resolucion_acta":forms.TextInput(attrs={"class":"form-control", "placeholder":"Acta"}),
			"contrato_resolucion_fk":ResolucionWidget(attrs={"class":"form-control customSelect2"}),
			"contrato_decreto":forms.TextInput(attrs={"class":"form-control"}),
			"contrato_certificacion_por_etapas":forms.CheckboxInput(attrs={"class":"form-check-input"}),
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
