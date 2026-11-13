from django import forms

from necesidades.models import Necesidad


class NecesidadForm(forms.ModelForm):
    class Meta:
        model = Necesidad
        fields = ["titulo", "detalle", "ejemplo", "modulo", "tipo", "urgencia", "oficina"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control",
                                             "placeholder": "Ej.: Buscar adjudicatarios por DNI desde el visor"}),
            "detalle": forms.Textarea(attrs={"class": "form-control", "rows": 4,
                                             "placeholder": "Qué estás haciendo cuando pasa, qué esperabas "
                                                            "y cómo lo resolvés hoy."}),
            "ejemplo": forms.TextInput(attrs={"class": "form-control"}),
            "modulo": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "urgencia": forms.RadioSelect(),
            "oficina": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej.: Adjudicaciones"}),
        }


class GestionForm(forms.ModelForm):
    class Meta:
        model = Necesidad
        fields = ["estado", "respuesta"]
        widgets = {
            "estado": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "respuesta": forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 2,
                                               "placeholder": "Respuesta visible para el equipo"}),
        }
