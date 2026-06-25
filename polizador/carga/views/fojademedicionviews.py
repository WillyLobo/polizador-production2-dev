from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views import generic
from carga.models import FojaDeMedicion, PlanDeTrabajosItem, PlanDeTrabajosRubro
from carga.forms.fojademedicionforms import *
from secretariador.forms.mixins import FormsetViewMixin


@method_decorator(login_required, name="dispatch")
class CrearFojaDeMedicion(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "carga.add_fojademedicion"
	formset_name = FojaDeMedicionItemFormset
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

		return self.render_to_response(self.get_context_data(form=form, formset=formset))

	def post(self, request, *args, **kwargs):
		rubro_id = self.request.POST.get("foja_rubro")
		if rubro_id:
			self._set_success_url(rubro_id)
		return super().post(request, *args, **kwargs)

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
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self._set_success_url()
		return super().post(request, *args, **kwargs)

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
