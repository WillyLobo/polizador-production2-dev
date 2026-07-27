from django import forms
from carga import models
from carga.views.ajaxviews import contratowidget, obrawidget

class ContratoDigitalForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = models.ContratosDigitales
        fields = (
            "contratodigital_contrato",
            "contratodigital_descripcion",
            "contratodigital_tipo",
            "contratodigital_archivo",
        )
        widgets = {
            "contratodigital_contrato": contratowidget(attrs={"class":"form-control customSelect2"}),
            "contratodigital_descripcion":forms.TextInput(attrs={"class":"form-control"}),
            "contratodigital_tipo":forms.Select(attrs={"class":"form-control"}),
            "contratodigital_archivo":forms.ClearableFileInput(attrs={"class":"form-control"}),
        }

class ObraDocumentoForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = models.ObraDocumento
        fields = (
            "obradocumento_obra",
            "obradocumento_descripcion",
            "obradocumento_archivo",
        )
        widgets = {
            "obradocumento_obra": obrawidget(attrs={"class":"form-control customSelect2"}),
            "obradocumento_descripcion":forms.TextInput(attrs={"class":"form-control"}),
            "obradocumento_archivo":forms.ClearableFileInput(attrs={"class":"form-control"}),
        }
