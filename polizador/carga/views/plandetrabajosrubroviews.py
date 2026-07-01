from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import generic
from carga.models import PlanDeTrabajos, PlanDeTrabajosRubro, ContratoMonto, Certificado
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

	def _plan(self):
		if not hasattr(self, "_plan_cache"):
			plan_id = self._plan_id()
			self._plan_cache = PlanDeTrabajos.objects.filter(pk=plan_id).first() if plan_id else None
		return self._plan_cache

	def _pedir_foja_numero_inicial(self):
		"""True si este rubro va a ser necesariamente raíz (sin rubro_anterior posible) para
		una obra que ya tiene certificados cargados: en ese caso hay que preguntar desde qué
		número arrancar la numeración de Fojas."""
		plan = self._plan()
		if not plan:
			return False
		obra_id = plan.trabajos_obra_id
		if not Certificado.objects.filter(certificado_obra_id=obra_id).exists():
			return False
		hay_candidatos_rubro_anterior = PlanDeTrabajosRubro.objects.filter(
			rubro_plan__trabajos_obra_id=obra_id
		).exclude(rubro_plan_id=plan.pk).exists()
		return not hay_candidatos_rubro_anterior

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs["pedir_foja_numero_inicial"] = self._pedir_foja_numero_inicial()
		return kwargs

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		plan_id = self._plan_id()
		if plan_id:
			plan = self._plan()
			obra_id = plan.trabajos_obra_id if plan else None
			form.fields["rubro_anterior"].queryset = PlanDeTrabajosRubro.objects.filter(
				rubro_plan__trabajos_obra_id=obra_id
			).exclude(rubro_plan_id=plan_id)
			if plan and plan.trabajos_contrato_id:
				form.fields["rubro_contratomonto"].queryset = ContratoMonto.objects.filter(
					contratomonto_contrato_id=plan.trabajos_contrato_id
				)
			else:
				form.fields["rubro_contratomonto"].queryset = ContratoMonto.objects.filter(
					contratomonto_contrato__contrato_obra_id=obra_id
				)
		return form

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		plan = self._plan()
		context["contrato_vinculado"] = plan.trabajos_contrato if plan and plan.trabajos_contrato_id else None
		context["pedir_foja_numero_inicial"] = self._pedir_foja_numero_inicial()
		return context

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

	def _pedir_foja_numero_inicial(self):
		"""En edición, "pedir" el campo equivale a "permitir editarlo": solo se habilita
		si el rubro todavía no tiene ninguna foja real (no-legacy) cargada, para no romper
		la continuidad de numeración ya materializada."""
		return not self.object.fojas.filter(foja_legacy=False).exists()

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs["pedir_foja_numero_inicial"] = self._pedir_foja_numero_inicial()
		return kwargs

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		plan = self.object.rubro_plan
		if plan.trabajos_contrato_id:
			form.fields["rubro_contratomonto"].queryset = ContratoMonto.objects.filter(
				contratomonto_contrato_id=plan.trabajos_contrato_id
			)
		else:
			form.fields["rubro_contratomonto"].queryset = ContratoMonto.objects.filter(
				contratomonto_contrato__contrato_obra_id=plan.trabajos_obra_id
			)
		return form

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		plan = self.object.rubro_plan
		context["contrato_vinculado"] = plan.trabajos_contrato if plan.trabajos_contrato_id else None
		context["pedir_foja_numero_inicial"] = self._pedir_foja_numero_inicial()
		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.success_url = reverse("carga:update-plandetrabajos", kwargs={"pk": self.object.rubro_plan_id})
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.success_url = reverse("carga:update-plandetrabajos", kwargs={"pk": self.object.rubro_plan_id})
		return super().post(request, *args, **kwargs)
