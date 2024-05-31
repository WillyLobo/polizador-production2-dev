from django import forms
from django.utils.safestring import SafeString
from secretariador.models import Incorporacion, ComisionadoSolicitud
from secretariador.forms.comisionadosolicitudform import ComisionadoSolicitudForm
from carga.views.ajaxviews import (
	localidadmultiplewidget,
	)
from secretariador.views.ajaxviews import ResolucionWidget, SolicitudWidget
from django.forms.models import inlineformset_factory

class IncorporacionForm(forms.ModelForm):
    class Meta:
        model = Incorporacion
        fields = (
            "incorporacion_solicitud",
            "incorporacion_actuacion",
            "incorporacion_solicitante",
            "incorporacion_resolucion",
        )
        widgets = {
            "incorporacion_solicitud":SolicitudWidget(attrs={
                "class":"form-control customSelect2"
                }),
            "incorporacion_actuacion":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "incorporacion_solicitante":forms.Select(attrs={
                "class":"form-control customSelect2"
                }),
            "incorporacion_resolucion":ResolucionWidget(attrs={
                "class":"form-control customSelect2"
                }),
        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
    def as_row(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group row'>"))

    # Logic for raising error if fecha_hasta < fecha_desde

ComisionadoIncorporacionFormset = inlineformset_factory(
					Incorporacion,
					ComisionadoSolicitud,
					form = ComisionadoSolicitudForm,
					extra=1,
                    can_delete=False)
