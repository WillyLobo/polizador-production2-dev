from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import generic
from carga.models import PlanDeTrabajos, PlanDeTrabajosRubro
from carga.forms.plandetrabajosrubroforms import *
from secretariador.forms.mixins import FormsetViewMixin


@method_decorator(login_required, name="dispatch")
class CrearPlanDeTrabajosRubro(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "carga.add_plandetrabajosrubro"
	formset_name = PlanDeTrabajosItemFormset
	view_type = "create"

	model = PlanDeTrabajosRubro
	template_name = "plandetrabajosrubro/crear-plandetrabajosrubro.html"
	form_class = PlanDeTrabajosRubroForm
	title = "Crear Rubro de Plan de Trabajos"

	def get_title(self):
		return self.title

	def _plan_id(self):
		return self.request.GET.get("plan") or self.request.POST.get("rubro_plan")

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		plan_id = self._plan_id()
		if plan_id:
			obra_id = PlanDeTrabajos.objects.filter(pk=plan_id).values_list("trabajos_obra_id", flat=True).first()
			form.fields["rubro_anterior"].queryset = PlanDeTrabajosRubro.objects.filter(
				rubro_plan__trabajos_obra_id=obra_id
			).exclude(rubro_plan_id=plan_id)
		return form

	def get(self, request, *args, **kwargs):
		self.object = None
		plan_id = self._plan_id()
		self.success_url = reverse("carga:update-plandetrabajos", kwargs={"pk": plan_id}) if plan_id else reverse("carga:crear-plandetrabajos")

		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if plan_id:
			form.fields["rubro_plan"].initial = plan_id

		formset = self.formset_name(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, formset=formset))

	def post(self, request, *args, **kwargs):
		plan_id = self._plan_id()
		self.success_url = reverse("carga:update-plandetrabajos", kwargs={"pk": plan_id}) if plan_id else reverse("carga:crear-plandetrabajos")
		return super().post(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class UpdatePlanDeTrabajosRubro(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "carga.change_plandetrabajosrubro"
	formset_name = PlanDeTrabajosItemFormset
	view_type = "update"

	model = PlanDeTrabajosRubro
	template_name = "plandetrabajosrubro/update-plandetrabajosrubro.html"
	form_class = PlanDeTrabajosRubroForm

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.success_url = reverse("carga:update-plandetrabajos", kwargs={"pk": self.object.rubro_plan_id})
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.success_url = reverse("carga:update-plandetrabajos", kwargs={"pk": self.object.rubro_plan_id})
		return super().post(request, *args, **kwargs)
