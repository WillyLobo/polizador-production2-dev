from django import forms
from secretariador.models import Incorporacion, ComisionadoSolicitud
from secretariador.forms.comisionadosolicitudform import ComisionadoSolicitudForm
from carga.views.ajaxviews import (
	localidadmultiplewidget,
	)
from secretariador.views.ajaxviews import ResolucionWidget, SolicitudWidget
from django.forms.models import inlineformset_factory
from secretariador.forms.mixins import BaseFormMixin

class IncorporacionForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Incorporacion
        fields = (
            "incorporacion_solicitud",
            "incorporacion_actuacion_ano",
            "incorporacion_actuacion_numero",
            "incorporacion_solicitante",
            "incorporacion_resolucion",
        )
        widgets = {
            "incorporacion_solicitud":SolicitudWidget(attrs={
                "class":"form-control customSelect2"
                }),
            "incorporacion_actuacion_ano":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "incorporacion_actuacion_numero":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "incorporacion_solicitante":forms.Select(attrs={
                "class":"form-control customSelect2"
                }),
            "incorporacion_resolucion":ResolucionWidget(attrs={
                "class":"form-control customSelect2"
                }),
        }

ComisionadoIncorporacionFormset = inlineformset_factory(
					Incorporacion,
					ComisionadoSolicitud,
					form = ComisionadoSolicitudForm,
					extra=1,
                    can_delete=False)
