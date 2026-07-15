from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from carga.models import Poliza, Poliza_Movimiento
from carga.forms.polizaforms import *
from carga.views.generics import get_deleted_objects, UserKwargsMixin, UserFormsetKwargsMixin
from secretariador.forms.mixins import FormsetViewMixin

@method_decorator(login_required, name="dispatch")
class EliminarPoliza(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_poliza"

	model = Poliza
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-polizas")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearPoliza(PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "carga.add_poliza"
	formset_name = PolizaMovimientoFormset
	view_type = "create"

	model = Poliza
	template_name = "poliza/crear-poliza.html"
	form_class = PolizaForm
	success_url = reverse_lazy("carga:crear-poliza")

	title = "Crear Póliza"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

@method_decorator(login_required, name="dispatch")
class UpdatePoliza(PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "carga.change_poliza"
	formset_name = PolizaMovimientoFormset
	view_type = "update"

	model = Poliza
	template_name = "poliza/update-poliza.html"
	form_class = PolizaForm
	success_url = reverse_lazy("carga:lista-polizas")

@method_decorator(login_required, name="dispatch")
class EliminarPolizaMovimiento(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "generic/confirm_delete.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

@method_decorator(login_required, name="dispatch")
class EstadoPoliza(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_poliza"

	model = Poliza
	template_name = "poliza/estado-poliza.html"

	# def get(self, request, *args, **kwargs):
	# 	poliza = request.session.get('poliza', 0)
	# 	request.session['num_visits'] = num_visits + 1
	# 	return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		self.object = self.get_object()
		poliza = models.Poliza.objects.get(id=self.object.id)
		poliza_id = str(poliza.id)
		self.request.session["poliza_id"] = poliza_id
		return context

@method_decorator(login_required, name="dispatch")
class ImprimirPolizaMovimiento(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "poliza/imprimir-poliza.html"

@login_required
@permission_required("carga.view_poliza", raise_exception=True)
def PaginaListaPolizas(request):
	template_name = "Lista-polizas.html"

	return render(request, template_name, {})

