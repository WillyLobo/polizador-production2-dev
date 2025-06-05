from django import forms
from secretariador.models import InstrumentosLegalesMemorandum, InstrumentosLegalesDecretos, InstrumentosLegalesResoluciones
from carga.views.ajaxviews import (
	localidadmultiplewidget,
	)
from secretariador.forms.mixins import BaseFormMixin
from datetime import datetime

class InstrumentosLegalesMemorandumForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = InstrumentosLegalesMemorandum
        fields = (
            "instrumentolegalmemorandum_tipo",
            "instrumentolegalmemorandum_numero",
            "instrumentolegalmemorandum_ano",
            "instrumentolegalmemorandum_fecha_aprobacion",
            "instrumentolegalmemorandum_descripcion",
            "instrumentolegalmemorandum",
            "instrumentolegalmemorandum_document"
        )
        widgets = {
            "instrumentolegalmemorandum_tipo":forms.Select(attrs={
                "class":"form-control customSelect2"
            }),
            "instrumentolegalmemorandum_numero":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegalmemorandum_ano":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegalmemorandum_fecha_aprobacion":forms.DateInput(attrs={
                "class":"form-control",
                "autocomplete":"off"
                }),
            "instrumentolegalmemorandum_descripcion":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegalmemorandum":forms.ClearableFileInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegalmemorandum_document":forms.Textarea(attrs={
                "class":"form-control",
                "rows":10,
                "cols":50,
                "readonly":"readonly"
            }),
        }

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.fields['instrumentolegalmemorandum_tipo'].initial = "P"
        self.fields['instrumentolegalmemorandum_ano'].initial = datetime.now().year

class InstrumentosLegalesDecretosForm(BaseFormMixin, forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.fields['instrumentolegaldecretos_tipo'].initial = "P"
        self.fields['instrumentolegaldecretos_ano'].initial = datetime.now().year

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get("instrumentolegaldecretos_numero")
        if numero:
            cleaned_data["instrumentolegaldecretos_numero"] = numero.zfill(5)
        return cleaned_data

class InstrumentosLegalesResolucionesPresidenciaForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = InstrumentosLegalesResoluciones
        fields = (
            "instrumentolegalresoluciones_tipo",
            "instrumentolegalresoluciones_numero",
            "instrumentolegalresoluciones_ano",
            "instrumentolegalresoluciones_fecha_aprobacion",
            "instrumentolegalresoluciones_descripcion",
            "instrumentolegalresoluciones",
            "instrumentolegalresoluciones_document"
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
            "instrumentolegalresoluciones_document":forms.Textarea(attrs={
                "class":"form-control",
                "rows":10,
                "cols":50,
                "readonly":"readonly"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get("instrumentolegalresoluciones_numero")
        if numero:
            cleaned_data["instrumentolegalresoluciones_numero"] = numero.zfill(5)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.fields['instrumentolegalresoluciones_tipo'].initial = "P"
        self.fields['instrumentolegalresoluciones_ano'].initial = datetime.now().year
    
class InstrumentosLegalesResolucionesDirectorioForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = InstrumentosLegalesResoluciones
        fields = (
            "instrumentolegalresoluciones_tipo",
            "instrumentolegalresoluciones_numero",
            "instrumentolegalresoluciones_acta",
            "instrumentolegalresoluciones_ano",
            "instrumentolegalresoluciones_fecha_aprobacion",
            "instrumentolegalresoluciones_descripcion",
            "instrumentolegalresoluciones",
            "instrumentolegalresoluciones_document"
        )
        widgets = {
            "instrumentolegalresoluciones_tipo":forms.Select(attrs={
                "class":"form-control customSelect2"
            }),
            "instrumentolegalresoluciones_numero":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "instrumentolegalresoluciones_acta":forms.TextInput(attrs={
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
            "instrumentolegalresoluciones_document":forms.Textarea(attrs={
                "class":"form-control",
                "rows":10,
                "cols":50,
                "readonly":"readonly"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get("instrumentolegalresoluciones_numero")
        if numero:
            cleaned_data["instrumentolegalresoluciones_numero"] = numero.zfill(5)
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.fields['instrumentolegalresoluciones_tipo'].initial = "D"
        self.fields['instrumentolegalresoluciones_ano'].initial = datetime.now().year