from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse_lazy
from carga import models
from carga.forms.receptorforms import *
from carga.views.generics import get_deleted_objects, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarReceptor(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_receptor"

	model = models.Receptor
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:crear-receptor")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearReceptor(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_receptor"

	model = models.Receptor
	template_name = "receptor/crear-receptor.html"
	form_class = ReceptorForm
	success_url = reverse_lazy("carga:crear-receptor")
	popup_form_partial = "partials/receptor-form-partial.html"

	title = "Crear Receptor"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateReceptor(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_receptor"

	model = models.Receptor
	template_name = "receptor/update-receptor.html"
	form_class = ReceptorForm
	success_url = reverse_lazy("carga:crear-receptor")