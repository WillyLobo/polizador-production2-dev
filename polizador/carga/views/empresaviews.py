from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Empresa
from carga.forms.empresaforms import *
from carga.views.generics import get_deleted_objects, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarEmpresa(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "carga.delete_empresa"

	model = Empresa
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-empresas")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearEmpresa(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_empresa"

	model = Empresa
	template_name = "empresa/crear-empresa.html"
	form_class = EmpresaForm
	success_url = reverse_lazy("carga:crear-empresa")
	popup_form_partial = "partials/empresa-form-partial.html"

	title = "Crear Empresa"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateEmpresa(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_empresa"

	model = Empresa
	template_name = "empresa/update-empresa.html"
	form_class = EmpresaForm
	success_url = reverse_lazy("carga:lista-empresas")

@method_decorator(login_required, name="dispatch")
class EmpresaObra(PermissionRequiredMixin, generic.DetailView):
	permission_required = "carga.view_empresa"

	model = Empresa
	template_name = "empresa/empresa-obra.html"

# def check_empresa(request):
# 	empresa = request.POST.get("empresa_nombre")
# 	empresas = models.Empresa.objects.filter(empresa_nombre__icontains=empresa)
# 	return render(request, "partials/check-empresa.html", {"empresas": empresas})

@login_required
@permission_required("carga.view_empresa", raise_exception=True)
def PaginaListaEmpresas(request):
	template_name = "Lista-empresas.html"

	return render(request, template_name, {})

