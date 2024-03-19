from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse_lazy
from carga import models
from carga.forms.areaforms import *

@method_decorator(login_required, name="dispatch")
class CrearArea(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.add_area"
	title = "Crear Area"

	model = models.Area
	template_name = "area/crear-area.html"
	form_class = AreaForm
	success_url = reverse_lazy("carga:crear-area")

	def get_title(self):
		return self.title
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context
	
@method_decorator(login_required, name="dispatch")
class UpdateArea(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required  = "carga.change_area"

	model = models.Area
	template_name = "area/update-area.html"
	form_class = AreaForm
	success_url = reverse_lazy("carga:crear-area")