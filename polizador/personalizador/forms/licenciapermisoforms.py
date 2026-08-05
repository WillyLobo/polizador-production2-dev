from django import forms
from django.forms.models import inlineformset_factory

from personalizador import models
from personalizador.views.ajaxviews import (
	agentewidget, tipolicenciapermisowidget,
	instrumentoresolucionwidget, instrumentodecretowidget, instrumentomemorandumwidget,
)
from core.widgets import DateHTMLWidget

class LicenciaPermisoForm(forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.LicenciaPermiso
		fields = (
			"licenciapermiso_agente",
			"licenciapermiso_tipo",
			"licenciapermiso_fecha_otorgamiento",
			"licenciapermiso_fecha_desde",
			"licenciapermiso_fecha_hasta",
			"licenciapermiso_cantidad",
			"licenciapermiso_motivo",
			"licenciapermiso_instrumento_resolucion",
			"licenciapermiso_instrumento_decreto",
			"licenciapermiso_instrumento_memorandum",
			"licenciapermiso_adjunto",
			"licenciapermiso_anulada",
		)
		widgets = {
			"licenciapermiso_agente": agentewidget(attrs={"class": "form-control customSelect2"}),
			"licenciapermiso_tipo": tipolicenciapermisowidget(attrs={"class": "form-control customSelect2"}),
			"licenciapermiso_fecha_otorgamiento": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"licenciapermiso_fecha_desde": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"licenciapermiso_fecha_hasta": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"licenciapermiso_cantidad": forms.NumberInput(attrs={"class": "form-control"}),
			"licenciapermiso_motivo": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
			"licenciapermiso_instrumento_resolucion": instrumentoresolucionwidget(attrs={"class": "form-control customSelect2"}),
			"licenciapermiso_instrumento_decreto": instrumentodecretowidget(attrs={"class": "form-control customSelect2"}),
			"licenciapermiso_instrumento_memorandum": instrumentomemorandumwidget(attrs={"class": "form-control customSelect2"}),
			"licenciapermiso_anulada": forms.CheckboxInput(attrs={"class": "form-check-input"}),
		}

	def clean(self):
		cleaned_data = super().clean()
		fecha_desde = cleaned_data.get("licenciapermiso_fecha_desde")
		fecha_hasta = cleaned_data.get("licenciapermiso_fecha_hasta")
		if fecha_desde and fecha_hasta and fecha_hasta < fecha_desde:
			self.add_error("licenciapermiso_fecha_hasta", "No puede ser anterior a la fecha desde.")
		return cleaned_data

class DevolucionHorasPermisoForm(forms.ModelForm):
	class Meta:
		model = models.DevolucionHorasPermiso
		fields = (
			"devolucionhoras_fecha",
			"devolucionhoras_cantidad",
			"devolucionhoras_observaciones",
		)
		widgets = {
			"devolucionhoras_fecha": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"devolucionhoras_cantidad": forms.NumberInput(attrs={"class": "form-control"}),
			"devolucionhoras_observaciones": forms.TextInput(attrs={"class": "form-control"}),
		}

DevolucionHorasPermisoFormset = inlineformset_factory(
	parent_model=models.LicenciaPermiso,
	model=models.DevolucionHorasPermiso,
	form=DevolucionHorasPermisoForm,
	fk_name="devolucionhoras_licencia",
	extra=1,
	can_delete=True,
)
