from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.template import loader, TemplateDoesNotExist
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Empresa
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from carga.forms.empresaforms import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class EliminarEmpresa(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
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
class CrearEmpresa(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.add_empresa"

	model = Empresa
	template_name = "empresa/crear-empresa.html"
	form_class = EmpresaForm
	success_url = reverse_lazy("carga:crear-empresa")

	title = "Crear Empresa"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateEmpresa(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.change_empresa"

	model = Empresa
	template_name = "empresa/update-empresa.html"
	form_class = EmpresaForm
	success_url = reverse_lazy("carga:lista-empresas")

@method_decorator(login_required, name="dispatch")
class EmpresaObra(generic.DetailView):
	login_url = "/"
	redirect_field_name = "login"

	model = Empresa
	template_name = "empresa/empresa-obra.html"

# def check_empresa(request):
# 	empresa = request.POST.get("empresa_nombre")
# 	empresas = models.Empresa.objects.filter(empresa_nombre__icontains=empresa)
# 	return render(request, "partials/check-empresa.html", {"empresas": empresas})

@login_required
def PaginaListaEmpresas(request):
	template_name = "Lista-empresas.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaEmpresasView(AjaxDatatableView):
	model = Empresa
	title = "Empresas"
	initial_order = [["id", "asc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False},
		{"name": "id","title":"ID", "visible": True},
		{"name":"empresa_nombre"},
		{"name":"empresa_cuit"},
		{"name":"empresa_titular_nombre"},
		{"name":"empresa_direccion"}
		]
	
	def customize_row(self, row, obj):
		id = str(obj.id)
		editarlink = f'<a href="/polizas/crear/empresa/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/polizas/crear/empresa/obra/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/polizas/eliminar/empresa/{id}">{eliminarlinkimg}</a>'
		if self.request.user.has_perm("carga.delete_empresa"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("carga.change_empresa"):
			row["edit"] = f"{editarlink}{detallelink}"
		else:
			row["edit"] = f"{detallelink}"
		return

	def render_row_details(self, pk, request=None):

        # we do some optimization on the request
		relateds = []
		if not self.disable_queryset_optimization_only and not self.disable_queryset_optimization_select_related:
			relateds = [f.name for f in self.model._meta.get_fields() if f.many_to_one and f.concrete]

		prefetchs = []
		if not self.disable_queryset_optimization_only and not self.disable_queryset_optimization_prefetch_related:
			prefetchs = [f.name for f in self.model._meta.get_fields() if f.many_to_many and f.concrete]

		obj = self.model.objects.filter(pk=pk).select_related(*relateds).prefetch_related(*prefetchs).first()

		# Extract "extra_data" from request
		extra_data = {k: v for k, v in request.GET.items() if k not in ['action', 'pk', ]}

		# Search a custom template for rendering, if available
		try:
			template = loader.get_template(
                'ajax_datatable/%s/%s/%s' % (self.model._meta.app_label,
                                             self.model._meta.model_name, self.render_row_details_template_name),
            )

			html = template.render({
				'model': self.model,
				'model_admin': self.get_model_admin(),
				'object': obj,
				'extra_data': extra_data,
				}, request)

		# Failing that, display a simple table with field values
		except TemplateDoesNotExist:
			fields = [f.name for f in self.model._meta.get_fields() if f.concrete]
			html = '<table class="row-details">'
			for field in fields:
				
				if field in prefetchs:
					value = ', '.join([str(x) for x in eval(f'obj.{field}').all()])
				else:
					try:
						value = getattr(obj, field)
					except AttributeError:
						continue
				html += '<tr><td>%s</td><td>%s</td></tr>' % (field, value)
			html += '</table>'
		return html