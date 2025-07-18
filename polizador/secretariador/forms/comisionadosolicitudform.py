from django import forms
from secretariador.models import ComisionadoSolicitud
from secretariador.forms.mixins import ColumnFormMixin
from secretariador.views.ajaxviews import ComisionadoWidget
from datetime import datetime

class DivErrorList(forms.utils.ErrorList):
    template_name = "generic/error_as_div.html"

class ComisionadoSolicitudForm(ColumnFormMixin, forms.ModelForm):
    class Meta:
        model = ComisionadoSolicitud
        fields = (
            "comisionadosolicitud_nombre",
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
            "comisionadosolicitud_gastos":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
                }),
            "comisionadosolicitud_combustible":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
                }),
            "comisionadosolicitud_chofer":forms.CheckboxInput(attrs={
                "class":"form-check-input",
                }),
            "comisionadosolicitud_colaborador":forms.CheckboxInput(attrs={
                "class":"form-check-input",
                }),
            "comisionadosolicitud_sin_viatico":forms.CheckboxInput(attrs={
                "class":"form-check-input",
                }),
        }

    def __init__(self, *args, **kwargs):
        super(ComisionadoSolicitudForm, self).__init__(*args, **kwargs)
        self.error_class = DivErrorList
        self.fields["comisionadosolicitud_nombre"].label = "Nombre"

    def clean(self):
        cleaned_data = super().clean()
        # check if comisionadosolicitud_nombre is included in another Solicitud in the same date
        comisionadoid = self.cleaned_data.get("id").pk if self.cleaned_data.get("id") else None
        comisionadosolicitud_nombre = cleaned_data.get("comisionadosolicitud_nombre")
        solicitud_fecha_desde = datetime.strptime(self.data.get("solicitud_fecha_desde"), "%Y-%m-%d")
        solicitud_fecha_hasta = datetime.strptime(self.data.get("solicitud_fecha_hasta"), "%Y-%m-%d")

        if not self.data.get("solicitud_anulada") and ComisionadoSolicitud.objects.filter(
            comisionadosolicitud_nombre=comisionadosolicitud_nombre,
            comisionadosolicitud_foreign__solicitud_fecha_desde=solicitud_fecha_desde,
            comisionadosolicitud_foreign__solicitud_fecha_hasta=solicitud_fecha_hasta
            ).exclude(id=comisionadoid).exclude(comisionadosolicitud_foreign__solicitud_anulada=True).count() > 0:
            self.add_error("comisionadosolicitud_nombre", f"El comisionado {comisionadosolicitud_nombre} ya está incluido en otra solicitud para la misma fecha.")
