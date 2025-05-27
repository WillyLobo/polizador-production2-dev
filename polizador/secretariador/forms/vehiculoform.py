from django import forms
from secretariador.models import Vehiculo
from secretariador.forms.mixins import BaseFormMixin
from secretariador.views.ajaxviews import (
    ResolucionWidget,
    ComisionadoWidget,
    VehiculoWidget,
    DecretoWidget,
    )
from carga.views.ajaxviews import empresawidget, aseguradorawidget

class VehiculoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = (
            "vehiculo_caracter",
            "vehiculo_modelo",
            "vehiculo_patente",
            "vehiculo_poliza",
            "vehiculo_poliza_aseguradora",
            "vehiculo_titular_agente",
            "vehiculo_titular_empresa",
            "vehiculo_n_motor",
            "vehiculo_n_chasis",
            "vehiculo_modelo",
        )
        widgets = {
            "vehiculo_caracter":forms.Select(attrs={
                "class":"form-control",
                }),
            "vehiculo_modelo":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "vehiculo_patente":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "vehiculo_poliza":forms.TextInput(attrs={
                "class":"form-control",
                }),
            "vehiculo_poliza_aseguradora":aseguradorawidget(attrs={
                "class":"form-control customSelect2",
                }),
            "vehiculo_titular_agente":ComisionadoWidget(attrs={
                "class":"form-control customSelect2",
                }),
            "vehiculo_titular_empresa":empresawidget(attrs={
                "class":"form-control customSelect2",
                }),
            "vehiculo_n_motor":forms.TextInput(attrs={
                "class":"form-control",
                }),
            "vehiculo_n_chasis":forms.TextInput(attrs={
                "class":"form-control",
                }),
            "vehiculo_modelo":forms.NumberInput(attrs={
                "class":"form-control",
                }),
        }