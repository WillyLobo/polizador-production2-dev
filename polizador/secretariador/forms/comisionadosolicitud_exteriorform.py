from django import forms
from django.utils.safestring import SafeString
from secretariador.models import ComisionadoSolicitud

class ComisionadoSolicitudExteriorForm(forms.ModelForm):
    class Meta:
        model = ComisionadoSolicitud
        fields = (
            "comisionadosolicitud_nombre",
            "comisionadosolicitud_pasaje",
            "comisionadosolicitud_gastos",
            "comisionadosolicitud_combustible",
            "comisionadosolicitud_chofer",
            "comisionadosolicitud_colaborador",
            "comisionadosolicitud_sin_viatico",
        )
        widgets = {
            "comisionadosolicitud_nombre":forms.Select(attrs={
                "class":"form-control"
                }),
            "comisionadosolicitud_pasaje":forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"0"
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
                "style":'width: 2em;height: 2em;'
                }),
            "comisionadosolicitud_colaborador":forms.CheckboxInput(attrs={
                "class":"form-check-input",
                "style":'width: 2em;height: 2em;'
                }),
            "comisionadosolicitud_sin_viatico":forms.CheckboxInput(attrs={
                "class":"form-check-input",
                "style":'width: 2em;height: 2em;'
                }),

        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='col'>"))

    def __init__(self, *args, **kwargs):
        super(ComisionadoSolicitudExteriorForm, self).__init__(*args, **kwargs)
        self.fields["comisionadosolicitud_nombre"].label = "Nombre"