from django import forms
from carga import models
from carga.views.ajaxviews import obramultiplewidget

class ContratoDigitalForm(forms.ModelForm):
    class Meta:
        model = models.ContratosDigitales
        fields = (
            "contratodigital_obra",
            "contratodigital_descripcion",
            "contratodigital_tipo",
            "contratodigital_archivo",
        )
        widgets = {
            "contratodigital_obra": obramultiplewidget(attrs={"class":"form-control"}),
            "contratodigital_descripcion":forms.TextInput(attrs={"class":"form-control"}),
            "contratodigital_tipo":forms.Select(attrs={"class":"form-control"}),
            "contratodigital_archivo":forms.ClearableFileInput(attrs={"class":"form-control"}),
        }

class ResolucionDigitalForm(forms.ModelForm):
    class Meta:
        model = models.ResolucionesDigitales
        fields = (
            "resoluciondigital_obra",
            "resoluciondigital_descripcion",
            "resoluciondigital_numero",
            "resoluciondigital_archivo",
        )
        widgets = {
            "resoluciondigital_obra": obramultiplewidget(attrs={"class":"form-control"}),
            "resoluciondigital_descripcion":forms.TextInput(attrs={"class":"form-control"}),
            "resoluciondigital_numero":forms.TextInput(attrs={"class":"form-control"}),
            "resoluciondigital_archivo":forms.ClearableFileInput(attrs= {"class":"form-control"})
        }
