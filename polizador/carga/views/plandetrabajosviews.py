from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from carga.models import PlanDeTrabajos
from carga.forms.plandetrabajosforms import *
from secretariador.forms.mixins import FormsetViewMixin

@method_decorator(login_required, name="dispatch")
class CrearPlanDeTrabajos(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "carga.add_plandetrabajos"
	formset_name = PlanDeTrabajosItemFormset
	view_type = "create"

	model = PlanDeTrabajos
	template_name = "plandetrabajos/crear-plandetrabajos.html"
	form_class = PlandeTrabajoForm
	success_url = reverse_lazy("carga:crear-plandetrabajos")
	title = "Crear Plan de Trabajos"

	def get_title(self):
		return self.title

@method_decorator(login_required, name="dispatch")
class UpdatePlanDeTrabajos(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "carga.change_plandetrabajos"
	formset_name = PlanDeTrabajosItemFormset
	view_type = "update"

	model = PlanDeTrabajos
	template_name = "plandetrabajos/update-plandetrabajos.html"
	form_class = PlandeTrabajoForm
	success_url = reverse_lazy("carga:lista-obras")
