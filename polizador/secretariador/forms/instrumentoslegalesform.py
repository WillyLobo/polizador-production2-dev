from django import forms
from django.utils.safestring import SafeString
from secretariador.models import InstrumentosLegalesDecretos, InstrumentosLegalesResoluciones
from carga.views.ajaxviews import (
	localidadmultiplewidget,
	)

class InstrumentosLegalesDecretosForm(forms.ModelForm):
    class Meta:
        model = InstrumentosLegalesDecretos
        fields = (
            "instrumentolegaldecretos_tipo",
            "instrumentolegaldecretos_numero",
            "instrumentolegaldecretos_ano",
            "instrumentolegaldecretos_fecha_aprobacion",
            "instrumentolegaldecretos_descripcion",
            "instrumentolegaldecretos",
        )
        widgets = {
            "instrumentolegaldecretos_tipo":forms.Select(attrs={
                "class":"form-control customSelect2"
            }),
            "instrumentolegaldecretos_numero":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegaldecretos_ano":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegaldecretos_fecha_aprobacion":forms.DateInput(attrs={
                "class":"form-control",
                "autocomplete":"off"
                }),
            "instrumentolegaldecretos_descripcion":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegaldecretos":forms.ClearableFileInput(attrs={
                "class":"form-control"
            }),
        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

class InstrumentosLegalesResolucionesForm(forms.ModelForm):
    class Meta:
        model = InstrumentosLegalesResoluciones
        fields = (
            "instrumentolegalresoluciones_tipo",
            "instrumentolegalresoluciones_numero",
            "instrumentolegalresoluciones_ano",
            "instrumentolegalresoluciones_fecha_aprobacion",
            "instrumentolegalresoluciones_descripcion",
            "instrumentolegalresoluciones",
        )
        widgets = {
            "instrumentolegalresoluciones_tipo":forms.Select(attrs={
                "class":"form-control customSelect2"
            }),
            "instrumentolegalresoluciones_numero":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegalresoluciones_ano":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegalresoluciones_fecha_aprobacion":forms.DateInput(attrs={
                "class":"form-control",
                "autocomplete":"off"
                }),
            "instrumentolegalresoluciones_descripcion":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegalresoluciones":forms.ClearableFileInput(attrs={
                "class":"form-control"
            }),
        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))