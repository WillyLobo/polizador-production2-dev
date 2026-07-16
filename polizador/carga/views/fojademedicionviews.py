from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views import generic
from carga.models import FojaDeMedicion, PlanDeTrabajosItem, PlanDeTrabajosRubro
from personalizador.models import Gerencia
from carga.forms.fojademedicionforms import *
from core.mixins import FormsetViewMixin


def _foja_detalle_context(foja):
    rubro = foja.foja_rubro
    plan = rubro.rubro_plan
    obra = plan.trabajos_obra
    items = list(
        foja.items
        .select_related("fojaitem_planitem")
        .order_by("fojaitem_planitem__planitem_orden")
    )
    anterior_map = FojaDeMedicion.anterior_items_map(rubro, exclude_foja_numero=foja.foja_numero)
    rows = [
        {
            "fojaitem": fi,
            "pct_anterior": anterior_map.get(fi.fojaitem_planitem_id, 0),
        }
        for fi in items
    ]
    responsable_institucional = Gerencia.objects.get(gerencia_nombre="Gerencia Operativa").gerencia_autoridad_a_cargo_fk
    total_pct_anterior = sum(r["pct_anterior"] for r in rows)
    total_pct_mes = sum(fi.fojaitem_pct_avance_mes for fi in items)
    total_pct_acumulado = sum(fi.fojaitem_pct_acumulado for fi in items)
    fotos = list(foja.fotos.all())
    foto_paginas = [fotos[i:i + 3] for i in range(0, len(fotos), 3)]
    return {
        "obra": obra,
        "plan": plan,
        "rubro": rubro,
        "rows": rows,
		"responsable_institucional": responsable_institucional,
        "total_pct_anterior": total_pct_anterior,
        "total_pct_mes": total_pct_mes,
        "total_pct_acumulado": total_pct_acumulado,
        "foto_paginas": foto_paginas,
    }


@method_decorator(login_required, name="dispatch")
class CrearFojaDeMedicion(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "carga.add_fojademedicion"
	formset_name = FojaDeMedicionItemFormset
	foto_formset_name = FojaDeMedicionFotoFormset
	view_type = "create"

	model = FojaDeMedicion
	template_name = "foja/crear-fojademedicion.html"
	form_class = FojaDeMedicionForm
	success_url = reverse_lazy("carga:crear-fojademedicion")
	title = "Crear Foja de Medición"

	def get_title(self):
		return self.title

	def get_initial(self):
		initial = super().get_initial()
		rubro_id = self.request.GET.get("rubro")
		if rubro_id:
			initial["foja_rubro"] = rubro_id
		return initial

	def _get_rubro(self):
		rubro_id = self.request.GET.get("rubro") or self.request.POST.get("foja_rubro")
		if rubro_id:
			return PlanDeTrabajosRubro.objects.filter(pk=rubro_id).select_related("rubro_plan").first()
		return None

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs["rubro"] = self._get_rubro()
		return kwargs

	def _set_success_url(self, rubro_id):
		obra_id = PlanDeTrabajosRubro.objects.filter(pk=rubro_id).values_list("rubro_plan__trabajos_obra_id", flat=True).first()
		self.success_url = reverse("carga:estado-obra", kwargs={"pk": obra_id}) if obra_id else reverse("carga:crear-fojademedicion")

	def get(self, request, *args, **kwargs):
		self.object = None

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		rubro_id = self.request.GET.get("rubro")
		items = PlanDeTrabajosItem.objects.none()
		anterior_map = {}

		if rubro_id:
			self._set_success_url(rubro_id)
			items = PlanDeTrabajosItem.objects.filter(planitem_rubro_id=rubro_id).order_by("planitem_orden")

			rubro = PlanDeTrabajosRubro.objects.filter(pk=rubro_id).first()
			if rubro:
				anterior_map = FojaDeMedicion.anterior_items_map(rubro, items=items)

		formset_class = build_foja_item_formset_class(extra=items.count())
		initial_data = []
		for item in items:
			inc = {"fojaitem_planitem": item.pk}
			if item.pk in anterior_map:
				inc["fojaitem_pct_anterior"] = anterior_map[item.pk]
			initial_data.append(inc)

		formset = formset_class(instance=self.object, initial=initial_data)

		# Asignar el planitem a cada formulario
		for sub_form, item in zip(formset.forms, items):
			sub_form.instance.fojaitem_planitem = item

		foto_formset = self.foto_formset_name(instance=self.object)

		return self.render_to_response(self.get_context_data(form=form, formset=formset, foto_formset=foto_formset))

	def post(self, request, *args, **kwargs):
		self.object = None

		rubro_id = self.request.POST.get("foja_rubro")
		if rubro_id:
			self._set_success_url(rubro_id)

		form_class = self.get_form_class()
		form = self.get_form(form_class)
		formset = self.formset_name(self.request.POST, self.request.FILES, instance=self.object)
		foto_formset = self.foto_formset_name(self.request.POST, self.request.FILES, instance=self.object)
		self.prepare_formset(formset)

		form_is_valid = form.is_valid()
		formset_is_valid = formset.is_valid()
		foto_formset_is_valid = foto_formset.is_valid()
		if form_is_valid and formset_is_valid and foto_formset_is_valid:
			self.object = form.save()
			self._save_fecha_inicio(form)
			self._vincular_certificados_legacy(form)
			formset.instance = self.object
			formset.save()
			foto_formset.instance = self.object
			foto_formset.save()
			return HttpResponseRedirect(self.get_success_url())
		return self.render_to_response(self.get_context_data(form=form, formset=formset, foto_formset=foto_formset))

	def _vincular_certificados_legacy(self, form):
		if not self.object.foja_legacy:
			return
		for certificado in form.cleaned_data.get("foja_legacy_certificados") or []:
			certificado.certificado_foja = self.object
			certificado.save(update_fields=["certificado_foja"])

	def _save_fecha_inicio(self, form):
		fecha_inicio = form.cleaned_data.get("trabajos_fecha_inicio")
		if not fecha_inicio:
			return
		plan = self.object.foja_rubro.rubro_plan
		if not plan.trabajos_fecha_inicio:
			plan.trabajos_fecha_inicio = fecha_inicio
			plan.save(update_fields=["trabajos_fecha_inicio"])

	def prepare_formset(self, formset):
		"""Repuebla el %% Anterior de cada fila al reconstruir el formset bindeado en el POST."""
		if not formset.is_bound:
			return

		rubro_id = self.request.POST.get("foja_rubro")
		rubro = PlanDeTrabajosRubro.objects.filter(pk=rubro_id).first() if rubro_id else None
		if not rubro:
			return

		item_ids = [
			sub_form.data.get(f"{sub_form.prefix}-fojaitem_planitem")
			for sub_form in formset.forms
		]
		items = PlanDeTrabajosItem.objects.in_bulk([i for i in item_ids if i])
		anterior_map = FojaDeMedicion.anterior_items_map(rubro, items=items.values())

		for sub_form, item_id in zip(formset.forms, item_ids):
			item_pk = int(item_id) if item_id else None
			if item_pk in anterior_map:
				sub_form.initial["fojaitem_pct_anterior"] = anterior_map[item_pk]


@method_decorator(login_required, name="dispatch")
class UpdateFojaDeMedicion(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "carga.change_fojademedicion"
	formset_name = FojaDeMedicionItemFormset
	foto_formset_name = FojaDeMedicionFotoFormset
	view_type = "update"

	model = FojaDeMedicion
	template_name = "foja/update-fojademedicion.html"
	form_class = FojaDeMedicionForm
	success_url = reverse_lazy("carga:lista-obras")

	def _set_success_url(self):
		self.success_url = reverse("carga:estado-obra", kwargs={"pk": self.object.foja_rubro.rubro_plan.trabajos_obra_id})

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		self._set_success_url()

		form_class = self.get_form_class()
		form = self.get_form(form_class)
		formset = self.formset_name(instance=self.object)
		self.prepare_formset(formset)
		foto_formset = self.foto_formset_name(instance=self.object)

		return self.render_to_response(self.get_context_data(form=form, formset=formset, foto_formset=foto_formset))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self._set_success_url()

		form_class = self.get_form_class()
		form = self.get_form(form_class)
		formset = self.formset_name(self.request.POST, self.request.FILES, instance=self.object)
		foto_formset = self.foto_formset_name(self.request.POST, self.request.FILES, instance=self.object)
		self.prepare_formset(formset)

		form_is_valid = form.is_valid()
		formset_is_valid = formset.is_valid()
		foto_formset_is_valid = foto_formset.is_valid()
		if form_is_valid and formset_is_valid and foto_formset_is_valid:
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			foto_formset.instance = self.object
			foto_formset.save()
			return HttpResponseRedirect(self.get_success_url())
		return self.render_to_response(self.get_context_data(form=form, formset=formset, foto_formset=foto_formset))

	def prepare_formset(self, formset):
		if not self.object:
			return

		anterior_map = FojaDeMedicion.anterior_items_map(
			self.object.foja_rubro, exclude_foja_numero=self.object.foja_numero
		)
		for sub_form in formset.forms:
			planitem_id = sub_form.instance.fojaitem_planitem_id
			if planitem_id in anterior_map:
				sub_form.initial["fojaitem_pct_anterior"] = anterior_map[planitem_id]


@method_decorator(login_required, name="dispatch")
class DetalleFojaDeMedicion(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_fojademedicion"
	model = FojaDeMedicion
	template_name = "foja/detalle-fojademedicion.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx.update(_foja_detalle_context(self.object))
		return ctx


@method_decorator(login_required, name="dispatch")
class ImprimirFojaDeMedicion(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_fojademedicion"
	model = FojaDeMedicion
	template_name = "foja/detalle-fojademedicion.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx.update(_foja_detalle_context(self.object))
		ctx["auto_print"] = True
		return ctx
