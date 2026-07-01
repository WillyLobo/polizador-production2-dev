from decimal import Decimal
from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from carga import models
from carga.models import Certificado
from carga.views.ajaxviews import rubrowidget, agentemultiplewidget, certificadolegacywidget
from personalizador.models import Agente
from polizador.custom_forms import DateHTMLWidget

class FojaDeMedicionForm(forms.ModelForm):
	foja_numero_manual = forms.IntegerField(
		label="Número de Foja",
		required=False,
		min_value=1,
		widget=forms.NumberInput(attrs={"class": "form-control"}),
	)
	foja_legacy_certificados = forms.ModelMultipleChoiceField(
		label="Certificados a vincular",
		queryset=Certificado.objects.none(),
		required=False,
		widget=certificadolegacywidget(attrs={"class": "form-control customSelect2"}),
	)

	class Meta:
		model = models.FojaDeMedicion
		fields = (
			"foja_rubro",
			"foja_legacy",
			"foja_periodo",
			"foja_fecha",
			"foja_inspector",
			"foja_observaciones",
		)
		widgets = {
			"foja_rubro": rubrowidget(attrs={"class": "form-control customSelect2"}),
			"foja_legacy": forms.CheckboxInput(attrs={"class": "form-check-input"}),
			"foja_periodo": DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
			"foja_fecha": DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
			"foja_inspector": agentemultiplewidget(attrs={"class": "form-control customSelect2"}),
			"foja_observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}

	def __init__(self, *args, **kwargs):
		rubro = kwargs.pop("rubro", None)
		super().__init__(*args, **kwargs)
		self.fields["foja_rubro"].queryset = models.PlanDeTrabajosRubro.objects.filter(
			rubro_plan__in=models.PlanDeTrabajos.vigentes()
		)

		rubro_id = self.data.get("foja_rubro") or self.initial.get("foja_rubro")
		if rubro_id:
			inspectores = Agente.objects.filter(
				obra_inspector__plandetrabajos__rubros__pk=rubro_id
			).distinct()
			obra_id = models.PlanDeTrabajosRubro.objects.filter(pk=rubro_id).values_list(
				"rubro_plan__trabajos_obra_id", flat=True
			).first()
			self.fields["foja_legacy_certificados"].queryset = (
				Certificado.objects.filter(certificado_obra_id=obra_id, certificado_foja__isnull=True)
				if obra_id else Certificado.objects.none()
			)
		else:
			inspectores = Agente.objects.none()

		self.fields["foja_inspector"].queryset = inspectores
		if not self.is_bound and not self.instance.pk:
			self.initial["foja_inspector"] = list(inspectores.values_list("pk", flat=True))

		if self.instance.pk and self.instance.foja_legacy:
			self.initial["foja_numero_manual"] = self.instance.foja_numero

		if rubro is not None and not rubro.rubro_plan.trabajos_fecha_inicio:
			label = (
				"Fecha de Reinicio de Obra"
				if rubro.rubro_anterior_id
				else "Fecha de Inicio de Obra"
			)
			self.fields["trabajos_fecha_inicio"] = forms.DateField(
				label=label,
				required=True,
				widget=DateHTMLWidget(attrs={"type": "date", "class": "form-control"}),
			)

	def clean(self):
		cleaned_data = super().clean()
		if not cleaned_data.get("foja_legacy"):
			return cleaned_data

		foja_rubro = cleaned_data.get("foja_rubro")
		numero = cleaned_data.get("foja_numero_manual")

		if numero is None:
			self.add_error("foja_numero_manual", "Ingresá el número de foja para una foja legacy.")
			return cleaned_data

		if not foja_rubro:
			return cleaned_data

		if numero >= foja_rubro.rubro_foja_numero_inicial:
			if foja_rubro.rubro_foja_numero_inicial <= 1:
				self.add_error(
					"foja_numero_manual",
					"Para cargar fojas legacy primero hay que configurar el 'Número de Foja "
					"Inicial' en el Rubro de Plan de Trabajos."
				)
			else:
				self.add_error(
					"foja_numero_manual",
					f"El número debe ser menor al Número de Foja Inicial configurado en el "
					f"Rubro ({foja_rubro.rubro_foja_numero_inicial})."
				)
			return cleaned_data

		duplicado = models.FojaDeMedicion.objects.filter(foja_rubro=foja_rubro, foja_numero=numero)
		if self.instance.pk:
			duplicado = duplicado.exclude(pk=self.instance.pk)
		if duplicado.exists():
			self.add_error("foja_numero_manual", f"Ya existe una Foja N°{numero} para este Rubro.")
			return cleaned_data

		self.instance.foja_numero = numero
		return cleaned_data

class FojaDeMedicionItemForm(forms.ModelForm):
	fojaitem_pct_anterior = forms.DecimalField(
		required=False,
		disabled=True,
		widget=forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
	)
	# Solo a fines de visualización: el acumulado real lo calcula siempre FojaDeMedicionItem.save().
	fojaitem_pct_acumulado = forms.DecimalField(
		required=False,
		disabled=True,
		widget=forms.NumberInput(attrs={"class": "form-control foja-acumulado", "readonly": True}),
	)

	class Meta:
		model = models.FojaDeMedicionItem
		fields = (
			"fojaitem_planitem",
			"fojaitem_pct_avance_mes",
		)
		widgets = {
			"fojaitem_planitem": forms.HiddenInput(),
			"fojaitem_pct_avance_mes": forms.NumberInput(attrs={"class": "form-control foja-mes"}),
		}

class BaseFojaDeMedicionItemFormset(BaseInlineFormSet):
	"""Valida los items de la Foja entre sí y contra la foja anterior del mismo rubro."""

	def _anterior_map(self):
		rubro_id = self.data.get("foja_rubro")
		if not rubro_id:
			return {}

		rubro = models.PlanDeTrabajosRubro.objects.filter(pk=rubro_id).first()
		if not rubro:
			return {}

		exclude_foja_numero = self.instance.foja_numero if self.instance.pk else None
		items = [
			form.cleaned_data.get("fojaitem_planitem")
			for form in self.forms
			if form.cleaned_data.get("fojaitem_planitem")
		]
		return models.FojaDeMedicion.anterior_items_map(
			rubro, items=items, exclude_foja_numero=exclude_foja_numero
		)

	def clean(self):
		super().clean()
		if any(self.errors):
			return

		anterior_map = self._anterior_map()
		total_anterior = total_mes = total_acumulado = Decimal("0")

		for form in self.forms:
			if not form.cleaned_data:
				continue

			planitem = form.cleaned_data.get("fojaitem_planitem")
			mes = form.cleaned_data.get("fojaitem_pct_avance_mes") or Decimal("0")
			anterior = anterior_map.get(planitem.pk, Decimal("0")) if planitem else Decimal("0")

			if planitem and anterior + mes > planitem.planitem_incidencia_pct:
				form.add_error(
					"fojaitem_pct_avance_mes",
					f"La suma de Anterior ({anterior}%) y Avance del Mes ({mes}%) no puede superar "
					f"la Incidencia del item ({planitem.planitem_incidencia_pct}%)."
				)

			total_anterior += anterior
			total_mes += mes
			total_acumulado += anterior + mes

		if total_anterior > 100:
			raise forms.ValidationError(f"La suma total de Anterior % no puede superar 100% (actual: {total_anterior}%).")
		if total_mes > 100:
			raise forms.ValidationError(f"La suma total de Avance del Mes % no puede superar 100% (actual: {total_mes}%).")
		if total_acumulado > 100:
			raise forms.ValidationError(f"La suma total de Acumulado % no puede superar 100% (actual: {total_acumulado}%).")

FojaDeMedicionItemFormset = inlineformset_factory(
	parent_model=models.FojaDeMedicion,
	model=models.FojaDeMedicionItem,
	form=FojaDeMedicionItemForm,
	formset=BaseFojaDeMedicionItemFormset,
	fk_name="fojaitem_foja",
	extra=0,
	can_delete=False,
)

def build_foja_item_formset_class(extra):
	"""Formset con tantas filas extra como items tenga el Plan de Trabajos elegido."""
	return inlineformset_factory(
		parent_model=models.FojaDeMedicion,
		model=models.FojaDeMedicionItem,
		form=FojaDeMedicionItemForm,
		formset=BaseFojaDeMedicionItemFormset,
		fk_name="fojaitem_foja",
		extra=extra,
		can_delete=False,
	)

class FojaDeMedicionFotoForm(forms.ModelForm):
	class Meta:
		model = models.FojaDeMedicionFoto
		fields = ("fotofoja_archivo",)
		widgets = {
			"fotofoja_archivo": forms.ClearableFileInput(attrs={"class": "form-control"}),
		}

FojaDeMedicionFotoFormset = inlineformset_factory(
	parent_model=models.FojaDeMedicion,
	model=models.FojaDeMedicionFoto,
	form=FojaDeMedicionFotoForm,
	fk_name="fotofoja_foja",
	extra=1,
	can_delete=True,
)
