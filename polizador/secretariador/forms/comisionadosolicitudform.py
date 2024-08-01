from django import forms
from django.utils.safestring import SafeString
from secretariador.models import ComisionadoSolicitud

class ComisionadoSolicitudForm(forms.ModelForm):
    class Meta:
        model = ComisionadoSolicitud
        fields = (
            "comisionadosolicitud_nombre",
            "comisionadosolicitud_gastos",
            "comisionadosolicitud_combustible",
            "comisionadosolicitud_chofer",
            "comisionadosolicitud_colaborador",
        )
        widgets = {
            "comisionadosolicitud_nombre":forms.Select(attrs={
                "class":"form-control"
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

        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='col'>"))
    
    def __init__(self, *args, **kwargs):
        super(ComisionadoSolicitudForm, self).__init__(*args, **kwargs)
        self.fields["comisionadosolicitud_nombre"].label = "Nombre"