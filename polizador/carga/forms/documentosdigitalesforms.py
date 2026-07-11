from django import forms
from carga import models
from carga.views.ajaxviews import contratowidget

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

class ResolucionDigitalForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = models.ResolucionesDigitales
        fields = (
            "resoluciondigital_contrato",
            "resoluciondigital_descripcion",
            "resoluciondigital_numero",
            "resoluciondigital_archivo",
        )
        widgets = {
            "resoluciondigital_contrato": contratowidget(attrs={"class":"form-control customSelect2"}),
            "resoluciondigital_descripcion":forms.TextInput(attrs={"class":"form-control"}),
            "resoluciondigital_numero":forms.TextInput(attrs={"class":"form-control"}),
            "resoluciondigital_archivo":forms.ClearableFileInput(attrs= {"class":"form-control"})
        }
