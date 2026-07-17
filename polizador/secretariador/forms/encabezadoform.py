from django import forms
from django.core.exceptions import ValidationError
from secretariador.models import EncabezadoDocumento
from secretariador.docx_header import tiene_encabezado_valido
from core.mixins import BaseFormMixin


class EncabezadoDocumentoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = EncabezadoDocumento
        fields = (
            "encabezadodocumento_archivo",
        )
        widgets = {
            "encabezadodocumento_archivo": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_encabezadodocumento_archivo(self):
        archivo = self.cleaned_data["encabezadodocumento_archivo"]
        if not tiene_encabezado_valido(archivo):
            raise ValidationError(
                "El archivo no tiene un encabezado de primera página reconocible. "
                "Verificá que sea un .docx válido con un encabezado configurado en Word."
            )
        return archivo
