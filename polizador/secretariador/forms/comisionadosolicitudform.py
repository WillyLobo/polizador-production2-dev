from django import forms
from secretariador.models import ComisionadoSolicitud
from secretariador.forms.mixins import ColumnFormMixin

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
            "comisionadosolicitud_nombre":forms.Select(attrs={
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

    def __init__(self, *args, **kwargs):
        super(ComisionadoSolicitudForm, self).__init__(*args, **kwargs)
        self.fields["comisionadosolicitud_nombre"].label = "Nombre"