from django import forms
from personalizador import models
from personalizador.views.ajaxviews import (
	generoagentewidget, tituloprofesionalmultiplewidget, categoriawidget,
	denominacioncargowidget, apartadocargowidget, ceicwidget, grupocargowidget,
	actividadespecificawidget, oficinawidget,
	resolucionagentewidget, decretoagentewidget, instrumentoagentewidget,
)
from personalizador.instrumentos import CONCEPTOS, EXT, TIPO_LABELS, instrumento_vinculado, limpiar_heredado, tipo_heredado
from carga.forms.mixins import AddRelatedPermissionMixin
from carga.views.ajaxviews import localidadwidget, provinciawidget
from core.widgets import DateHTMLWidget

class AgenteForm(AddRelatedPermissionMixin, forms.ModelForm):
	required_css_class = "required"

	class Meta:
		model = models.Agente
		fields = (
			"agente_nombres",
			"agente_apellidos",
			"n_legajo",
			"sexo",
			"abreviatura",
			"telefono",
			"email",
			"titulo_profesional",
			"matricula",
			"dni",
			"cuil",
			"fecha_nacimiento",
			"fecha_ingreso",
			"fecha_pase_a_planta",
			"instrumento_pase_planta_decreto",
			"instrumento_bonificacion_resolucion",
			"instrumento_bonificacion_decreto",
			"porcentaje_bonificacion",
			"instrumento_contrato_servicio_resolucion",
			"instrumento_contrato_servicio_decreto",
			"categoria",
			"denominacion_cargo",
			"cargo_interno",
			"instrumento_cargo_interno_resolucion",
			"instrumento_cargo_interno_decreto",
			"apartado",
			"ceic",
			"grupo",
			"activdad_central",
			"actividad_especifica",
			"oficina",
			"instrumento_transferencia_definitiva_decreto",
			"instrumento_transferencia_definitiva_externo",
			"domicilio_direccion",
			"domicilio_barrio",
			"domicilio_localidad",
			"domicilio_provincia",
			"instrumento_aportes_ley_resolucion",
			"instrumento_aportes_ley_decreto",
			"instrumento_aportes_ley_externo",
			"aportes_ley_resolucion_anios",
			"aportes_ley_resolucion_meses",
			"aportes_ley_resolucion_dias",
			"instrumento_aportes_anses_externo",
			"aportes_anses_anios",
			"aportes_anses_meses",
			"aportes_anses_dias",
			"agente_verificado_contra_padron",
			"agente_es_inpector_obra",
			"agente_personal_transitorio",
			"agente_personal_de_gabinete",
			"activo",
			"con_errores",
		)
		widgets = {
			"agente_nombres": forms.TextInput(attrs={"class": "form-control"}),
			"agente_apellidos": forms.TextInput(attrs={"class": "form-control"}),
			"n_legajo": forms.NumberInput(attrs={"class": "form-control"}),
			"sexo": generoagentewidget(attrs={"class": "form-control customSelect2"}),
			"abreviatura": forms.TextInput(attrs={"class": "form-control"}),
			"telefono": forms.TextInput(attrs={"class": "form-control"}),
			"email": forms.EmailInput(attrs={"class": "form-control"}),
			"titulo_profesional": tituloprofesionalmultiplewidget(attrs={"class": "form-control customSelect2"}),
			"matricula": forms.TextInput(attrs={"class": "form-control"}),
			"dni": forms.NumberInput(attrs={"class": "form-control"}),
			"cuil": forms.TextInput(attrs={"class": "form-control"}),
			"fecha_nacimiento": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"fecha_ingreso": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"fecha_pase_a_planta": DateHTMLWidget(attrs={"class": "form-control", "type": "date"}),
			"porcentaje_bonificacion": forms.NumberInput(attrs={"class": "form-control"}),
			"categoria": categoriawidget(attrs={"class": "form-control customSelect2"}),
			"denominacion_cargo": denominacioncargowidget(attrs={"class": "form-control customSelect2"}),
			"cargo_interno": oficinawidget(attrs={"class": "form-control customSelect2"}),
			"apartado": apartadocargowidget(attrs={"class": "form-control customSelect2"}),
			"ceic": ceicwidget(attrs={"class": "form-control customSelect2"}),
			"grupo": grupocargowidget(attrs={"class": "form-control customSelect2"}),
			"activdad_central": forms.TextInput(attrs={"class": "form-control"}),
			"actividad_especifica": actividadespecificawidget(attrs={"class": "form-control customSelect2"}),
			"oficina": oficinawidget(attrs={"class": "form-control customSelect2"}),
			"domicilio_direccion": forms.TextInput(attrs={"class": "form-control"}),
			"domicilio_barrio": forms.TextInput(attrs={"class": "form-control"}),
			"domicilio_localidad": localidadwidget(attrs={"class": "form-control customSelect2"}),
			"domicilio_provincia": provinciawidget(attrs={"class": "form-control customSelect2"}),
			"aportes_ley_resolucion_anios": forms.NumberInput(attrs={"class": "form-control"}),
			"aportes_ley_resolucion_meses": forms.NumberInput(attrs={"class": "form-control"}),
			"aportes_ley_resolucion_dias": forms.NumberInput(attrs={"class": "form-control"}),
			"aportes_anses_anios": forms.NumberInput(attrs={"class": "form-control"}),
			"aportes_anses_meses": forms.NumberInput(attrs={"class": "form-control"}),
			"aportes_anses_dias": forms.NumberInput(attrs={"class": "form-control"}),
			"agente_verificado_contra_padron": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"agente_es_inpector_obra": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"agente_personal_transitorio": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"agente_personal_de_gabinete": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"con_errores": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"instrumento_pase_planta_decreto": decretoagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_bonificacion_resolucion": resolucionagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_bonificacion_decreto": decretoagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_contrato_servicio_resolucion": resolucionagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_contrato_servicio_decreto": decretoagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_cargo_interno_resolucion": resolucionagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_cargo_interno_decreto": decretoagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_transferencia_definitiva_decreto": decretoagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_transferencia_definitiva_externo": instrumentoagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_aportes_ley_resolucion": resolucionagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_aportes_ley_decreto": decretoagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_aportes_ley_externo": instrumentoagentewidget(attrs={"class": "form-control customSelect2"}),
			"instrumento_aportes_anses_externo": instrumentoagentewidget(attrs={"class": "form-control customSelect2"}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Conceptos con mas de un tipo posible: un selector (no es campo del modelo) muestra
		# solo el select de la FK elegida (ver agente-instrumento-campos.html).
		for concepto in CONCEPTOS:
			if len(concepto.fks) > 1:
				for tipo, campo in concepto.fks.items():
					self.fields[campo].label = TIPO_LABELS[tipo] if tipo != EXT else "Instrumento externo"
				self.fields[self.nombre_selector(concepto)] = forms.ChoiceField(
					label="Tipo de instrumento", required=False,
					choices=[(tipo, TIPO_LABELS[tipo]) for tipo in concepto.fks],
					initial=self._tipo_inicial(concepto),
					widget=forms.Select(attrs={"class": "form-control instrumento-tipo-selector"}),
				)

	@staticmethod
	def nombre_selector(concepto):
		return f"tipo_instrumento_{concepto.clave}"

	def _tipo_inicial(self, concepto):
		tipo, _ = instrumento_vinculado(self.instance, concepto)
		if tipo:
			return tipo
		heredado = tipo_heredado(self.instance, concepto) if getattr(self.instance, concepto.heredado) else None
		if heredado == "DIS" and EXT in concepto.fks:
			return EXT
		return heredado if heredado in concepto.fks else next(iter(concepto.fks))

	@property
	def instrumentos(self):
		"""{clave: {"label", "selector", "campos", "heredado"}} para el template: campos es la
		lista de {"tipo", "campo" (BoundField)} de las FKs del concepto; heredado, el texto
		viejo sin vincular."""
		grupos = {}
		for concepto in CONCEPTOS:
			nombre = self.nombre_selector(concepto)
			heredado = getattr(self.instance, concepto.heredado)
			tipo_viejo = tipo_heredado(self.instance, concepto) if heredado else None
			grupos[concepto.clave] = {
				"label": concepto.label,
				"selector": self[nombre] if nombre in self.fields else None,
				"campos": [{"tipo": tipo, "campo": self[campo]} for tipo, campo in concepto.fks.items()],
				"heredado": f"{tipo_viejo or ''} {heredado}".strip() if heredado else None,
			}
		return grupos

	def clean(self):
		cleaned_data = super().clean()
		# Solo vale la FK del tipo elegido en el selector: las demas se descartan, aunque
		# hayan quedado con valor en el select oculto.
		for concepto in CONCEPTOS:
			nombre = self.nombre_selector(concepto)
			if nombre not in self.fields:
				continue
			elegido = cleaned_data.get(nombre)
			for tipo, campo in concepto.fks.items():
				if tipo != elegido:
					cleaned_data[campo] = None
		return cleaned_data

	def save(self, commit=True):
		# Un concepto vinculado ya no necesita el dato heredado.
		for concepto in CONCEPTOS:
			if instrumento_vinculado(self.instance, concepto)[0]:
				limpiar_heredado(self.instance, concepto)
		return super().save(commit)
