from django import forms
from django.utils.safestring import SafeString
from secretariador.models import Solicitud, ComisionadoSolicitud
from secretariador.forms.comisionadosolicitud_exteriorform import ComisionadoSolicitudExteriorForm
from carga.views.ajaxviews import (
	localidadmultiplewidget,
    )
from secretariador.views.ajaxviews import (
    ResolucionWidget,
    ComisionadoWidget,
    VehiculoWidget,
    )
from django.forms.models import inlineformset_factory

class SolicitudExteriorForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = (
            "solicitud_actuacion_ano",
            "solicitud_actuacion_numero",
            "solicitud_solicitante",
            "solicitud_provincia",
            "solicitud_ciudad",
            "solicitud_decreto_viaticos",
            "solicitud_fecha_desde",
            "solicitud_fecha_hasta",
            "solicitud_tareas",
            "solicitud_aereo",
            "solicitud_vehiculo",
            "solicitud_dia_inhabil",
            "solicitud_resolucion"
            )
        widgets = {
            "solicitud_actuacion_ano":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "solicitud_actuacion_numero":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "solicitud_solicitante":ComisionadoWidget(attrs={
                "class":"form-control customSelect2"
                }),
            "solicitud_decreto_viaticos":forms.Select(attrs={
                "class":"form-control customSelect2"
                }),
            "solicitud_provincia":forms.Select(attrs={
                "class":"form-control",
                "default":"20"
                }),
            "solicitud_ciudad":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "solicitud_fecha_desde":forms.DateInput(attrs={
                "class":"form-control",
                "autocomplete":"off"
                }),
            "solicitud_fecha_hasta":forms.DateInput(attrs={
                "class":"form-control",
                "autocomplete":"off"
                }),
            "solicitud_tareas":forms.TextInput(attrs={
                "class":"form-control"
                }),
            "solicitud_aereo":forms.CheckboxInput(attrs={
                "class":"form-check-input",
                "style":'width: 2em;height: 2em;'
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

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
    def as_row(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group row'>"))

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

ComisionadoSolicitudExteriorFormset = inlineformset_factory(
					Solicitud,
					ComisionadoSolicitud,
					form = ComisionadoSolicitudExteriorForm,
					extra=1,
                    can_delete=False)