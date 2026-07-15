from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse_lazy
from carga import models
from carga.forms.areaforms import *
from carga.views.generics import PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class CrearArea(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_area"
	title = "Crear Area"

	model = models.Area
	template_name = "area/crear-area.html"
	form_class = AreaForm
	success_url = reverse_lazy("carga:crear-area")
	popup_form_partial = "partials/area-form-partial.html"

	def get_title(self):
		return self.title
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context
	
@method_decorator(login_required, name="dispatch")
class UpdateArea(PermissionRequiredMixin, generic.UpdateView):
	permission_required  = "carga.change_area"

	model = models.Area
	template_name = "area/update-area.html"
	form_class = AreaForm
	success_url = reverse_lazy("carga:crear-area")