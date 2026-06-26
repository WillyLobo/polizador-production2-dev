from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views import generic
from carga.models import PlanDeTrabajos, PlanDeTrabajosRubro, PlanDeTrabajosItem
from carga.forms.plandetrabajosforms import *

@method_decorator(login_required, name="dispatch")
class CrearPlanDeTrabajos(PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_plandetrabajos"

	model = PlanDeTrabajos
	template_name = "plandetrabajos/crear-plandetrabajos.html"
	form_class = PlandeTrabajoForm
	title = "Crear Plan de Trabajos"

	def get_title(self):
		return self.title

	def _origen_id(self):
		return self.request.GET.get("clonar") or self.request.POST.get("clonar")

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		origen_id = self._origen_id()
		obra_id = None
		if origen_id:
			obra_id = PlanDeTrabajos.objects.filter(pk=origen_id).values_list("trabajos_obra_id", flat=True).first()
		if not obra_id:
			obra_id = self.request.GET.get("obra")
		if obra_id:
			form.fields["trabajos_obra"].initial = obra_id

		return self.render_to_response(self.get_context_data(form=form))

	def form_valid(self, form):
		response = super().form_valid(form)
		origen_id = self._origen_id()
		if origen_id:
			self._clonar_desde(origen_id)
		return response

	def _clonar_desde(self, origen_id):
		for rubro_origen in PlanDeTrabajosRubro.objects.filter(rubro_plan_id=origen_id):
			rubro_nuevo = PlanDeTrabajosRubro.objects.create(
				rubro_plan=self.object,
				rubro_nombre=rubro_origen.rubro_nombre,
				rubro_orden=rubro_origen.rubro_orden,
				rubro_presupuesto=rubro_origen.rubro_presupuesto,
				rubro_anterior=rubro_origen,
			)
			for item_origen in rubro_origen.items.all():
				PlanDeTrabajosItem.objects.create(
					planitem_rubro=rubro_nuevo,
					planitem_nombre=item_origen.planitem_nombre,
					planitem_orden=item_origen.planitem_orden,
					planitem_incidencia_pct=item_origen.planitem_incidencia_pct,
					item_anterior=item_origen,
				)

@method_decorator(login_required, name="dispatch")
class UpdatePlanDeTrabajos(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_plandetrabajos"

	model = PlanDeTrabajos
	template_name = "plandetrabajos/update-plandetrabajos.html"
	form_class = PlandeTrabajoForm
