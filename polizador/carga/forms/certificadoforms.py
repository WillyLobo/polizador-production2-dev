from django import forms
from carga import models
from carga.views.ajaxviews import obrawidget

class CustomClearableFileInput(forms.widgets.ClearableFileInput):
	# template_name = "clearable_file_input.html"
	pass

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = models.Certificado
        fields = (
		"certificado_obra",
		"certificado_rubro_anticipo",
		"certificado_rubro_obra",
		"certificado_rubro_devanticipo",
		"certificado_rubro_db",
		"certificado_financiamiento",
		"certificado_expediente",
		"certificado_fecha",
		"certificado_mes_pct",
		"certificado_ante_pct",
		"certificado_acum_pct",
		"certificado_monto_pesos",
		"certificado_devolucion_monto",
		"certificado_monto_uvi",
		"certificado_devolucion_monto_uvi",
		"certificado_devolucion_expte",
		"certificado_digital",
        "certificado_fecha_carga_legacy"
    )
        
        widgets = {
            "certificado_obra":obrawidget(attrs={"class":"form-control customSelect2"}),
			"certificado_rubro_anticipo":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_rubro_obra":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_rubro_devanticipo":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_rubro_db":forms.Select(attrs={"class":"form-control"}),
			"certificado_financiamiento":forms.Select(attrs={"class":"form-control"}),
			"certificado_expediente":forms.TextInput(attrs={"class":"form-control"}),
			"certificado_fecha":forms.DateInput(attrs={"class":"form-control"}),
			"certificado_mes_pct":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_ante_pct":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_acum_pct":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_monto_pesos":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_devolucion_monto":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_monto_uvi":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_devolucion_monto_uvi":forms.NumberInput(attrs={"class":"form-control"}),
			"certificado_devolucion_expte":forms.NumberInput(attrs={"class":"form-control"}),
            "certificado_digital":CustomClearableFileInput(attrs={"class":"form-control"})
			}
