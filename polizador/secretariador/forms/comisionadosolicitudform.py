from django import forms
from secretariador.models import ComisionadoSolicitud
from core.mixins import BaseFormMixin
from secretariador.views.ajaxviews import ComisionadoWidget, ComisionadoExternoWidget
from datetime import datetime
from core.widgets import CustomCheckboxInput

class DivErrorList(forms.utils.ErrorList):
    template_name = "generic/error_as_div.html"

class ComisionadoSolicitudForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = ComisionadoSolicitud
        fields = (
            "comisionadosolicitud_nombre",
            "comisionadosolicitud_externo",
            "comisionadosolicitud_gastos",
            "comisionadosolicitud_combustible",
            "comisionadosolicitud_chofer",
            "comisionadosolicitud_colaborador",
            "comisionadosolicitud_sin_viatico",
        )

        widgets = {
            "comisionadosolicitud_nombre":ComisionadoWidget(attrs={
                "class":"form-control customSelect2",
                "style":"width: 40em;height: 3em;"
                }),
            "comisionadosolicitud_externo":ComisionadoExternoWidget(attrs={
                "class":"form-control customSelect2",
                "style":"width: 40em;height: 3em;"
                }),
            "comisionadosolicitud_gastos":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
                }),
            "comisionadosolicitud_combustible":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
                }),
            "comisionadosolicitud_chofer":CustomCheckboxInput(attrs={
                "class":"form-check-input",
                }),
            "comisionadosolicitud_colaborador":CustomCheckboxInput(attrs={
                "class":"form-check-input",
                }),
            "comisionadosolicitud_sin_viatico":CustomCheckboxInput(attrs={
                "class":"form-check-input",
                }),
        }

    def __init__(self, *args, **kwargs):
        super(ComisionadoSolicitudForm, self).__init__(*args, **kwargs)
        self.error_class = DivErrorList
        self.fields["comisionadosolicitud_nombre"].label = "Agente del organismo"
        self.fields["comisionadosolicitud_externo"].label = "Persona externa"

    def clean(self):
        cleaned_data = super().clean()
        comisionadoid = self.cleaned_data.get("id").pk if self.cleaned_data.get("id") else None
        agente = cleaned_data.get("comisionadosolicitud_nombre")
        externo = cleaned_data.get("comisionadosolicitud_externo")

        if not agente and not externo:
            self.add_error("comisionadosolicitud_nombre", "Debe elegir un agente del organismo o una persona externa.")
            return cleaned_data
        if agente and externo:
            self.add_error("comisionadosolicitud_nombre", "Elegí un agente del organismo o una persona externa, no ambos.")
            return cleaned_data

        campo = "comisionadosolicitud_nombre" if agente else "comisionadosolicitud_externo"
        persona = agente or externo
        solicitud_fecha_desde = datetime.strptime(self.data.get("solicitud_fecha_desde"), "%Y-%m-%d")
        solicitud_fecha_hasta = datetime.strptime(self.data.get("solicitud_fecha_hasta"), "%Y-%m-%d")

        # check if the same agente/externo is included in another Solicitud in the same date
        if not self.data.get("solicitud_anulada") and ComisionadoSolicitud.objects.filter(
            comisionadosolicitud_foreign__solicitud_fecha_desde=solicitud_fecha_desde,
            comisionadosolicitud_foreign__solicitud_fecha_hasta=solicitud_fecha_hasta,
            **{campo: persona},
            ).exclude(id=comisionadoid).exclude(comisionadosolicitud_foreign__solicitud_anulada=True).count() > 0:
            self.add_error(campo, f"El comisionado {persona} ya está incluido en otra solicitud para la misma fecha.")
        return cleaned_data
