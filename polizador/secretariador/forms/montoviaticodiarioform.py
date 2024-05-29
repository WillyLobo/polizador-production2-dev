from django import forms
from django.utils.safestring import SafeString
from extra_views import InlineFormSetView
from secretariador.models import MontoViaticoDiario, InstrumentosLegalesDecretos

class MontoViaticoDiarioForm(forms.ModelForm):
    class Meta:
        model = MontoViaticoDiario
        fields = (
            "montoviaticodiario_estrato_uno_interior",
            "montoviaticodiario_estrato_dos_interior",
            "montoviaticodiario_estrato_tres_interior",
            "montoviaticodiario_estrato_cuatro_interior",
            "montoviaticodiario_estrato_uno_exterior",
            "montoviaticodiario_estrato_dos_exterior",
            "montoviaticodiario_estrato_tres_exterior",
            "montoviaticodiario_estrato_cuatro_exterior",
            # "montoviaticodiario_decreto_reglamentario",
        )
        widgets = {
            "montoviaticodiario_estrato_uno_interior":      forms.TextInput(attrs={"class":"form-control", "inputmode":"numeric", "placeholder":"0", "min":"0"}),
            "montoviaticodiario_estrato_dos_interior":      forms.TextInput(attrs={"class":"form-control", "inputmode":"numeric", "placeholder":"0", "min":"0"}),
            "montoviaticodiario_estrato_tres_interior":     forms.TextInput(attrs={"class":"form-control", "inputmode":"numeric", "placeholder":"0", "min":"0"}),
            "montoviaticodiario_estrato_cuatro_interior":   forms.TextInput(attrs={"class":"form-control", "inputmode":"numeric", "placeholder":"0", "min":"0"}),
            "montoviaticodiario_estrato_uno_exterior":      forms.TextInput(attrs={"class":"form-control", "inputmode":"numeric", "placeholder":"0", "min":"0"}),
            "montoviaticodiario_estrato_dos_exterior":      forms.TextInput(attrs={"class":"form-control", "inputmode":"numeric", "placeholder":"0", "min":"0"}),
            "montoviaticodiario_estrato_tres_exterior":     forms.TextInput(attrs={"class":"form-control", "inputmode":"numeric", "placeholder":"0", "min":"0"}),
            "montoviaticodiario_estrato_cuatro_exterior":   forms.TextInput(attrs={"class":"form-control", "inputmode":"numeric", "placeholder":"0", "min":"0"}),
        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='col'>"))

MontoViaticoDiarioFormset = forms.models.inlineformset_factory(
					InstrumentosLegalesDecretos,
					MontoViaticoDiario,
					form = MontoViaticoDiarioForm,
					extra=1,
                    max_num=1,
                    can_delete=False)
