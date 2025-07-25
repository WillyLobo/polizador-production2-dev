from django import forms
from secretariador.models import Solicitud, ComisionadoSolicitud, InstrumentosLegalesDecretos, MontoViaticoDiario
from carga.models import Provincia
from secretariador.forms.comisionadosolicitudform import ComisionadoSolicitudForm
from carga.views.ajaxviews import (
	localidadmultiplewidget,
    provinciawidget,
    )
from secretariador.views.ajaxviews import (
    ResolucionWidget,
    ComisionadoWidget,
    VehiculoWidget,
    DecretoWidget,
    )
from django.forms.models import inlineformset_factory
from secretariador.forms.mixins import BaseFormMixin
from secretariador.forms.widgets import DateHTMLWidget

class SolicitudForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = (
            "solicitud_anulada",
            "solicitud_actuacion_jurisdiccion",
            "solicitud_actuacion_ano",
            "solicitud_actuacion_numero",
            "solicitud_solicitante",
            "solicitud_provincia",
            "solicitud_localidades",
            "solicitud_decreto_viaticos",
            "solicitud_fecha_desde",
            "solicitud_fecha_hasta",
            "solicitud_tareas",
            "solicitud_vehiculo",
            "solicitud_dia_inhabil",
            "solicitud_resolucion"
            )

        widgets = {
            "solicitud_anulada":forms.CheckboxInput(attrs={
                "class":"form-check-input",
                "style":'width: 2em;height: 2em;'
                }),
            "solicitud_actuacion_jurisdiccion":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Jurisdicción",
                }),
            "solicitud_actuacion_ano":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "solicitud_actuacion_numero":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "solicitud_solicitante":ComisionadoWidget(attrs={
                "class":"form-control customSelect2"
                }),
            "solicitud_decreto_viaticos":DecretoWidget(attrs={
                "class":"form-control customSelect2"
                }),
            "solicitud_provincia":provinciawidget(attrs={
                "class":"form-control",
                "default":"22", # Provincia del Chaco
                }),
            "solicitud_localidades":localidadmultiplewidget(attrs={
                "class":"form-control customSelect2",
                "data-mdb-filter":"true"
                }),
            "solicitud_fecha_desde":DateHTMLWidget(attrs={
                "type":"date",
                "class":"form-control",
                "autocomplete":"off"
                }),
            "solicitud_fecha_hasta":DateHTMLWidget(attrs={
                "type":"date",
                "class":"form-control",
                "autocomplete":"off"
                }),
            "solicitud_tareas":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "solicitud_vehiculo":VehiculoWidget(attrs={
                "class":"form-control customSelect2"
                }),
            "solicitud_dia_inhabil":forms.CheckboxInput(attrs={
                "class":"form-check-input",
                "style":'width: 2em;height: 2em;'
                }),
            "solicitud_resolucion":ResolucionWidget(attrs={
                "class":"form-control customSelect2"
                }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = MontoViaticoDiario.objects.all()
        self.fields["solicitud_decreto_viaticos"].queryset = queryset
        self.fields["solicitud_decreto_viaticos"].initial = queryset.last().id
        self.fields["solicitud_provincia"].initial = Provincia.objects.get(pk=22)
        # Labels for fields without them.
        self.fields["solicitud_solicitante"].label = "Solicitante"
        self.fields["solicitud_provincia"].label = "Provincia"
        self.fields["solicitud_localidades"].label = "Localidades"
        self.fields["solicitud_decreto_viaticos"].label = "Decreto Reglamentario"
        self.fields["solicitud_vehiculo"].label = "Vehículo"
        

    # Logic for raising error if fecha_hasta < fecha_desde
    def clean(self):
        """
        Validates the form data and raises a ValidationError if the "fecha_hasta" field is less than the "fecha_desde" field.

        This function is called by the Django form framework to validate the form data before it is saved. It checks if the value 
        of the "fecha_hasta" field is less than the value of the "fecha_desde" field. If it is, a ValidationError is raised with 
        the message "Fecha final tiene que ser mayor a fecha inicial."

        Parameters:
            self (object): The current instance of the form.

        Returns:
            None

        Raises:
            forms.ValidationError: If the "fecha_hasta" field is less than the "fecha_desde" field.
        """
        cleaned_data = super().clean()
        fecha_desde = cleaned_data.get("solicitud_fecha_desde")
        fecha_hasta = cleaned_data.get("solicitud_fecha_hasta")
        if fecha_hasta < fecha_desde:
            raise forms.ValidationError("Fecha final tiene que ser mayor a fecha inicial.")

class ComisionadoSolicitudFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

ComisionadoSolicitudFormset = inlineformset_factory(
    parent_model = Solicitud,
    model = ComisionadoSolicitud,
    form = ComisionadoSolicitudForm,
    formset = ComisionadoSolicitudFormset,
    fk_name = "comisionadosolicitud_foreign",
    extra = 1,
    can_delete = False,
)
