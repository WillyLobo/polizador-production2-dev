from django import forms
from django.utils.safestring import SafeString
from carga import models
from carga.views.ajaxviews import (
	empresawidget,
	departamentomultiplewidget,
	localidadmultiplewidget,
	municipiomultiplewidget,
	obramultiplewidget
	)

class ObraForm(forms.ModelForm):
	class Meta:
		model = models.Obra
		fields = (
			"obra_nombre",
			"obra_soluciones",
			"obra_empresa",
			"obra_region",
			"obra_departamento_m",
			"obra_municipio_m",
			"obra_localidad_m",
			"obra_conjunto",
			"obra_grupo",
			"obra_plazo",
			"obra_programa",
			"obra_convenio",
			"obra_expediente",
			"obra_resolucion",
			"obra_licitacion_tipo",
			"obra_licitacion_numero",
			"obra_licitacion_ano",
			"obra_nomenclatura",
			"obra_fecha_contrato",
			"obra_inspector",
			"obra_observaciones",
			"obra_contrato_nacion_pesos",
			"obra_contrato_nacion_uvi",
			"obra_contrato_nacion_uvi_fecha",
			"obra_contrato_provincia_pesos",
			"obra_contrato_provincia_uvi",
			"obra_contrato_provincia_uvi_fecha",
			"obra_contrato_terceros_pesos",
			"obra_contrato_terceros_uvi",
			"obra_contrato_terceros_uvi_fecha",
			"obra_principal",
		)
		
		localized_fields = "__all__"
		widgets = {
			"obra_nombre": forms.TextInput(attrs={
				"class": "form-control", 
				"placeholder" : "Nombre de Obra",
			}),
			"obra_soluciones": forms.TextInput(attrs={
				"class": "form-control", 
				"placeholder" : "Cantidad de Soluciones",
			}),
			"obra_empresa":empresawidget(attrs={
				"class": "form-control customSelect2",
			}),
			"obra_region": forms.Select(attrs={
				"class": "form-control"
			}),
			"obra_departamento_m": departamentomultiplewidget(attrs={
				"class": "form-control customSelect2"
			}),
			"obra_localidad_m":localidadmultiplewidget(attrs={
				"class": "form-control customSelect2"
			}),
			"obra_municipio_m":municipiomultiplewidget(attrs={
				"class": "form-control customSelect2"
			}),
			"obra_conjunto": forms.Select(attrs={
				"class": "form-control customSelect2"
			}),
			"obra_grupo": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Grupo"
			}),
			"obra_plazo": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Plazo de Ejecución"
			}),
			"obra_programa": forms.Select(attrs={
				"class": "form-control customSelect2"
			}),
			"obra_convenio": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Convenio"
			}),
			"obra_expediente": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Expediente"
			}),
			"obra_resolucion": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Resolución"
			}),
			"obra_licitacion_tipo": forms.Select(attrs={
				"class": "form-control",
				"placeholder": "Tipo de Compulsa"
			}),
			"obra_licitacion_numero": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Número de Compulsa"
			}),
			"obra_licitacion_ano": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Año de Compulsa"
			}),
			"obra_nomenclatura": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Nomenclatura Catastral"
			}),
			"obra_fecha_contrato": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Fecha de Firma de Contrato"
			}),
			"obra_inspector": forms.SelectMultiple(attrs={
				"class": "form-control customSelect2",
			}),
			"obra_observaciones": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Observaciones"
			}),
			"obra_contrato_nacion_pesos": forms.NumberInput(attrs={
				"class": "form-control",
				"placeholder": "0"
			}),
			"obra_contrato_nacion_uvi": forms.NumberInput(attrs={
				"class": "form-control",
				"placeholder": "0"
			}),
			"obra_contrato_nacion_uvi_fecha": forms.DateInput(attrs={
				"class": "form-control",
			}),
			"obra_contrato_provincia_pesos": forms.NumberInput(attrs={
				"class": "form-control",
				"placeholder": "0"
			}),
			"obra_contrato_provincia_uvi": forms.NumberInput(attrs={
				"class": "form-control",
				"placeholder": "0"
			}),
			"obra_contrato_provincia_uvi_fecha": forms.DateInput(attrs={
				"class": "form-control",
			}),
			"obra_contrato_terceros_pesos": forms.NumberInput(attrs={
				"class": "form-control",
				"placeholder": "0"
			}),
			"obra_contrato_terceros_uvi": forms.NumberInput(attrs={
				"class": "form-control",
				"placeholder": "0"
			}),
			"obra_contrato_terceros_uvi_fecha": forms.DateInput(attrs={
				"class": "form-control",
			}),
			"obra_principal":obramultiplewidget(attrs={
				"class": "form-control customSelect2"
			}),
		}
	
	def as_div(self):
		return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
	
