from django import forms
from personalizador import models
from personalizador.views.ajaxviews import (
	generoagentewidget, tituloprofesionalmultiplewidget, categoriawidget,
	denominacioncargowidget, apartadocargowidget, ceicwidget, grupocargowidget,
	actividadespecificawidget, oficinawidget,
	resolucionagentewidget, decretoagentewidget, instrumentoagentewidget,
)
from django.forms import BaseInlineFormSet, inlineformset_factory
from personalizador.instrumentos import CAMPO_POR_TIPO, CONCEPTOS, EXT, TIPO_LABELS, limpiar_heredado, tipo_heredado
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
			"porcentaje_bonificacion",
			"categoria",
			"denominacion_cargo",
			"cargo_interno",
			"apartado",
			"ceic",
			"grupo",
			"activdad_central",
			"actividad_especifica",
			"oficina",
			"domicilio_direccion",
			"domicilio_barrio",
			"domicilio_localidad",
			"domicilio_provincia",
			"agente_verificado_contra_padron",
			"agente_es_inpector_obra",
			"agente_personal_transitorio",
			"agente_personal_de_gabinete",
			"activo",
			"retirado",
			"jubilado",
			"fallecido",
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
			"agente_verificado_contra_padron": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"agente_es_inpector_obra": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"agente_personal_transitorio": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"agente_personal_de_gabinete": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"retirado": forms.CheckboxInput(attrs={"class": "form-check-input agente-baja"}),
			"jubilado": forms.CheckboxInput(attrs={"class": "form-check-input agente-baja"}),
			"fallecido": forms.CheckboxInput(attrs={"class": "form-check-input agente-baja"}),
			"con_errores": forms.CheckboxInput(attrs={"class": "form-check-input"}),
		}

	def __init__(self, *args, user=None, **kwargs):
		super().__init__(*args, user=user, **kwargs)
		# Un formset de AgenteInstrumento por concepto: cada concepto admite varios instrumentos.
		self.formsets = {
			concepto.clave: AgenteInstrumentoFormSet(
				self.data if self.is_bound else None,
				self.files if self.is_bound else None,
				instance=self.instance,
				prefix=f"instrumentos_{concepto.clave}",
				queryset=models.AgenteInstrumento.objects.filter(concepto=concepto.clave).select_related("resolucion", "decreto", "externo"),
				form_kwargs={"concepto": concepto, "user": user},
			)
			for concepto in CONCEPTOS
		}

	@property
	def instrumentos(self):
		"""{clave: {"label", "formset", "heredado"}} para el template; heredado es el texto
		viejo sin vincular."""
		grupos = {}
		for concepto in CONCEPTOS:
			heredado = getattr(self.instance, concepto.heredado)
			tipo_viejo = tipo_heredado(self.instance, concepto) if heredado else None
			grupos[concepto.clave] = {
				"label": concepto.label,
				"formset": self.formsets[concepto.clave],
				"heredado": f"{tipo_viejo or ''} {heredado}".strip() if heredado else None,
			}
		return grupos

	def is_valid(self):
		# Validar todos (no cortocircuitar) para que cada formset muestre sus errores.
		resultados = [super().is_valid(), *(formset.is_valid() for formset in self.formsets.values())]
		return all(resultados)

	def _conceptos_vinculados(self):
		"""Conceptos que quedan con al menos un instrumento despues de guardar."""
		claves = set()
		for clave, formset in self.formsets.items():
			for form in formset.forms:
				datos = getattr(form, "cleaned_data", None) or {}
				if datos.get("DELETE"):
					continue
				if any(datos.get(campo) for campo in CAMPO_POR_TIPO.values()):
					claves.add(clave)
		return claves

	def save(self, commit=True):
		# Un concepto vinculado ya no necesita el dato heredado.
		vinculados = self._conceptos_vinculados()
		for concepto in CONCEPTOS:
			if concepto.clave in vinculados:
				limpiar_heredado(self.instance, concepto)
		agente = super().save(commit)
		if commit:
			self._guardar_formsets()
		else:
			save_m2m = self.save_m2m

			def guardar_todo():
				save_m2m()
				self._guardar_formsets()
			self.save_m2m = guardar_todo
		return agente

	def _guardar_formsets(self):
		for formset in self.formsets.values():
			formset.instance = self.instance
			formset.save()


class AgenteInstrumentoForm(AddRelatedPermissionMixin, forms.ModelForm):
	"""Un instrumento de un concepto (ver personalizador/instrumentos.py::CONCEPTOS). Solo se
	ofrecen los tipos que admite el concepto; si hay mas de uno, un selector (no es campo del
	modelo) muestra solo el select del tipo elegido (JS en agente-form-partial.html)."""

	class Meta:
		model = models.AgenteInstrumento
		fields = ("resolucion", "decreto", "externo", "anios", "meses", "dias")
		widgets = {
			"resolucion": resolucionagentewidget(attrs={"class": "form-control customSelect2"}),
			"decreto": decretoagentewidget(attrs={"class": "form-control customSelect2"}),
			"externo": instrumentoagentewidget(attrs={"class": "form-control customSelect2"}),
			"anios": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
			"meses": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
			"dias": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
		}
		labels = {"anios": "Años", "meses": "Meses", "dias": "Días"}

	def __init__(self, *args, concepto, **kwargs):
		super().__init__(*args, **kwargs)
		self.concepto = concepto
		self.instance.concepto = concepto.clave
		for tipo, campo in CAMPO_POR_TIPO.items():
			if tipo not in concepto.tipos:
				del self.fields[campo]
			else:
				self.fields[campo].label = TIPO_LABELS[tipo] if tipo != EXT else "Instrumento externo"
		if not concepto.con_tiempo:
			for campo in ("anios", "meses", "dias"):
				del self.fields[campo]
		if len(concepto.tipos) > 1:
			self.fields["tipo"] = forms.ChoiceField(
				label="Tipo de instrumento", required=False,
				choices=[(tipo, TIPO_LABELS[tipo]) for tipo in concepto.tipos],
				initial=self.instance.tipo or concepto.tipos[0],
				widget=forms.Select(attrs={"class": "form-control instrumento-tipo-selector"}),
			)

	@property
	def selector(self):
		return self["tipo"] if "tipo" in self.fields else None

	@property
	def campos_instrumento(self):
		"""[{"tipo", "campo" (BoundField)}] de los tipos de instrumento del concepto."""
		return [{"tipo": tipo, "campo": self[CAMPO_POR_TIPO[tipo]]} for tipo in self.concepto.tipos]

	@property
	def campos_tiempo(self):
		return [self[campo] for campo in ("anios", "meses", "dias") if campo in self.fields]

	def clean(self):
		cleaned_data = super().clean()
		# Solo vale la FK del tipo elegido en el selector: las demas se descartan, aunque
		# hayan quedado con valor en el select oculto.
		if "tipo" in self.fields:
			elegido = cleaned_data.get("tipo")
			for tipo in self.concepto.tipos:
				if tipo != elegido:
					cleaned_data[CAMPO_POR_TIPO[tipo]] = None
		return cleaned_data


class BaseAgenteInstrumentoFormSet(BaseInlineFormSet):
	def clean(self):
		super().clean()
		vistos = set()
		for form in self.forms:
			datos = getattr(form, "cleaned_data", None) or {}
			if datos.get("DELETE"):
				continue
			for campo in CAMPO_POR_TIPO.values():
				if datos.get(campo):
					clave = (campo, datos[campo].pk)
					if clave in vistos:
						raise forms.ValidationError(f"{datos[campo]} está cargado más de una vez.")
					vistos.add(clave)


AgenteInstrumentoFormSet = inlineformset_factory(
	models.Agente, models.AgenteInstrumento,
	form=AgenteInstrumentoForm, formset=BaseAgenteInstrumentoFormSet,
	extra=0, can_delete=True,
)
