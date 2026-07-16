from django import forms
from carga import models
from carga.forms.mixins import AddRelatedPermissionMixin
from carga.views.ajaxviews import (
	empresawidget,
	conjuntowidget,
	programawidget,
	agentemultiplewidget,
	departamentomultiplewidget,
	localidadmultiplewidget,
	municipiomultiplewidget,
	obramultiplewidget
	)
from personalizador.views.ajaxviews import (
    representantetecnicoMultipleWidget,
	)
from secretariador.views.ajaxviews import ResolucionWidget
from polizador.custom_forms import DateHTMLWidget, LatLngField, LatLngWidget

class ObraForm(AddRelatedPermissionMixin, forms.ModelForm):
	required_css_class = "required"

	obra_georeferencia = LatLngField(
		required=False,
		label="Georeferencia (Latitud / Longitud)",
		widget=LatLngWidget(attrs={"class": "form-control"}),
	)

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
			"obra_resolucion_fk",
			"obra_licitacion_tipo",
			"obra_licitacion_numero",
			"obra_licitacion_ano",
			"obra_nomenclatura",
			"obra_fecha_contrato",
			"obra_fecha_entrega",
			"obra_inspector",
			"obra_representantetecnico",
			"obra_observaciones",
			"obra_principal",
			"obra_georeferencia",
		)
		
		# localized_fields = "__all__"
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
			"obra_conjunto": conjuntowidget(attrs={
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
			"obra_programa": programawidget(attrs={
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
			"obra_resolucion_fk": ResolucionWidget(attrs={
				"class": "form-control customSelect2",
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
			"obra_fecha_contrato": DateHTMLWidget(attrs={
				"type":"date",
				"class": "form-control",
			}),
			"obra_fecha_entrega": DateHTMLWidget(attrs={
				"type":"date",
				"class": "form-control",
			}),
			"obra_inspector": agentemultiplewidget(attrs={
				"class": "form-control customSelect2",
			}),
			"obra_representantetecnico": representantetecnicoMultipleWidget(attrs={
				"class": "form-control customSelect2",
			}),
			"obra_observaciones": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Observaciones"
			}),
			"obra_principal":obramultiplewidget(attrs={
				"class": "form-control customSelect2"
			}),
		}