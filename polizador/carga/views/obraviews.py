from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse_lazy

from django.urls import reverse
from carga.models import Obra, obras_con_acumulado_anotado
from carga.forms.obraforms import *
from carga.views.generics import get_deleted_objects, UserKwargsMixin

@method_decorator(login_required, name="dispatch")
class EliminarObra(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_obra"

	model = Obra
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-obras")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context
	
@method_decorator(login_required, name="dispatch")
class CrearObra(PermissionRequiredMixin, UserKwargsMixin, generic.CreateView):
	permission_required = "carga.add_obra"

	model = Obra
	template_name = "obra/crear-obra.html"
	form_class = ObraForm
	success_url = reverse_lazy("carga:crear-obra")

	title = "Crear Obra"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

	def form_valid(self, form):
		response = super().form_valid(form)
		if self.request.POST.get("next") == "contrato":
			return HttpResponseRedirect(f"{reverse('carga:crear-contrato')}?obra={self.object.pk}")
		return response


@method_decorator(login_required, name="dispatch")
class UpdateObra(PermissionRequiredMixin, UserKwargsMixin, generic.UpdateView):
	permission_required = "carga.change_obra"

	model = Obra
	template_name = "obra/update-obra.html"
	form_class = ObraForm
	success_url = reverse_lazy("carga:lista-obras")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		contrato_vigente = self.object.contrato_vigente()
		context["contrato_vigente"] = contrato_vigente
		if contrato_vigente:
			context["montos_contrato_vigente"] = contrato_vigente.contratomonto_set.select_related(
				"contratomonto_rubro", "contratomonto_financiamiento"
			)
		context["tiene_contratos_anteriores"] = self.object.contrato_set.count() > 1
		return context

@method_decorator(login_required, name="dispatch")
class EstadoObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_obra"
	queryset = Obra.objects.select_related("obra_empresa", "obra_programa", "obra_conjunto").prefetch_related("certificado_set__certificado_rubro_db")

	model = Obra
	template_name = "obra/estado-obra.html"

@method_decorator(login_required, name="dispatch")
class PlanesAnterioresObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_plandetrabajos"

	model = Obra
	template_name = "obra/planes-anteriores.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		vigente = self.object.plan_vigente()
		planes = self.object.plandetrabajos_set.prefetch_related("rubros__items", "rubros__fojas__foja_inspector")
		if vigente:
			planes = planes.exclude(pk=vigente.pk)
		context["planes_anteriores"] = planes.order_by("-trabajos_fecha", "-pk")
		return context

@method_decorator(login_required, name="dispatch")
class ContratosAnterioresObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_contrato"

	model = Obra
	template_name = "obra/contratos-anteriores.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		vigente = self.object.contrato_vigente()
		contratos = self.object.contrato_set.prefetch_related("contratomonto_set__contratomonto_rubro", "contratomonto_set__contratomonto_financiamiento")
		if vigente:
			contratos = contratos.exclude(pk=vigente.pk)
		context["contratos_anteriores"] = contratos.order_by("-contrato_fecha", "-pk")
		return context

@login_required
@permission_required("carga.view_obra", raise_exception=True)
def PaginaListaObras(request):
    """
	Renderiza la página que contiene la tabla.
	Esta a su vez invoca (via ajax) object_datatable_view(), para rellenar el contenido de la tabla.
    """
    # model = Obra
    template_name = "Lista-obras.html"

    return render(request, template_name, {
        # "model": model,
    })

@login_required
def PaginaListaObrasExtendida(request):
	template_name = "Lista-obras-extendida.html"

	return render(request, template_name, {})

