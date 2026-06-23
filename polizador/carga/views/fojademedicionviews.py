from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from carga.models import FojaDeMedicion, PlanDeTrabajosItem
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

	def get(self, request, *args, **kwargs):
		self.object = None

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		plan_id = self.request.GET.get("plan")
		if plan_id:
			form.fields["foja_plan"].initial = plan_id
			items = PlanDeTrabajosItem.objects.filter(planitem_plan_id=plan_id).order_by("planitem_orden")

			# Buscar la foja anterior del mismo plan para cargar valores previos
			foja_periodo = self.request.GET.get("periodo") or self.object.foja_periodo if hasattr(self, 'object') and self.object else None
			if foja_periodo:
				try:
					from datetime import date
					fecha_periodo = date.fromisoformat(foja_periodo)
					foja_anterior = FojaDeMedicion.objects.filter(
						foja_plan_id=plan_id,
						foja_periodo__lt=fecha_periodo,
					).order_by("-foja_periodo").first()
				except (ValueError, TypeError):
					foja_anterior = None
			else:
				foja_anterior = FojaDeMedicion.objects.filter(
					foja_plan_id=plan_id
				).order_by("-foja_periodo").first()

			formset_class = build_foja_item_formset_class(extra=items.count())

			if foja_anterior:
				anterior_map = {item.fojaitem_planitem_id: item.fojaitem_pct_acumulado for item in foja_anterior.items.all()}
				initial_data = []
				for item in items:
					inc = {"fojaitem_planitem": item.pk}
					if item.pk in anterior_map:
						inc["fojaitem_pct_anterior"] = anterior_map[item.pk]
					initial_data.append(inc)
				formset = formset_class(instance=self.object, initial=initial_data)
			else:
				formset = formset_class(
					instance=self.object,
					initial=[{"fojaitem_planitem": item.pk} for item in items],
				)

			for sub_form, item in zip(formset.forms, items):
				sub_form.instance.fojaitem_planitem = item
		else:
			items = PlanDeTrabajosItem.objects.none()

		formset_class = build_foja_item_formset_class(extra=items.count())
		formset = formset_class(
		instance=self.object,
		initial=[{"fojaitem_planitem": item.pk} for item in items],
		)
		# El formset todavía no está atado a la BD: dejamos cada fila apuntando
		# a su PlanDeTrabajosItem para poder mostrar el nombre del item en el template.
		for sub_form, item in zip(formset.forms, items):
			sub_form.instance.fojaitem_planitem = item		
		
		return self.render_to_response(self.get_context_data(form=form, formset=formset))


@method_decorator(login_required, name="dispatch")
class UpdateFojaDeMedicion(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "carga.change_fojademedicion"
	formset_name = FojaDeMedicionItemFormset
	view_type = "update"

	model = FojaDeMedicion
	template_name = "foja/update-fojademedicion.html"
	form_class = FojaDeMedicionForm
	success_url = reverse_lazy("carga:lista-obras")
