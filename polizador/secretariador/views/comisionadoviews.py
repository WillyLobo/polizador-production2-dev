from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from secretariador.models import Comisionado
from secretariador.forms.comisionadoform import ComisionadoForm
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class CrearComisionado(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_comisionado"

	model = Comisionado
	template_name = "comisionado/crear-comisionado.html"
	form_class = ComisionadoForm
	success_url = reverse_lazy("secretariador:crear-comisionado")
	
	title = "Crear Comisionado"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context
	
@method_decorator(login_required, name="dispatch")
class UpdateComisionado(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_comisionado"

	model = Comisionado
	template_name = "comisionado/update-comisionado.html"
	form_class = ComisionadoForm
	success_url = reverse_lazy("secretariador:crear-comisionado")

@method_decorator(login_required, name="dispatch")
class EliminarComisionado(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_comisionado"

	model = Comisionado
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-comisionados")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

# @method_decorator(login_required, name="dispatch")
# class CertificadoView(generic.DetailView):
# 	login_url = "/"
# 	redirect_field_name = "login"
# 	model = Certificado
# 	template_name = "certificado/certificado.html"

@login_required
def PaginaListaComisionados(request):
	template_name = "Lista-comisionados.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaComisionadosView(AjaxDatatableView):
	model = Comisionado
	title = "Comisionados"
	initial_order = [["comisionado_apellidos", "asc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":81},
		{"name": "id","title":"ID", "visible": False},
		{"name":"comisionado_apellidos", "title":"Apellidos", "className": "align-left"},
		{"name":"comisionado_nombres", "title":"Nombre", "className": "align-left"},
		{"name":"comisionado_cargo", "title":"Cargo", "foreign_field":"comisionado_cargo__organigrama_cargo"},
		{"name":"comisionado_cuit", "title":"CUIT"},
		{"name":"comisionado_personal_transitorio", "title":"Personal Contratado", "choices":True, "autofilter":True},
		{"name":"comisionado_personal_de_gabinete", "title":"Personal de Gabinete", "choices":True, "autofilter":True},
	]

	def customize_row(self, row, obj):
		id = str(obj.id)
		
		editarlink = f'<a href="/viaticos/crearcomisionado/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/comisionado/{id}">{eliminarlinkimg}</a>'
		
		if self.request.user.has_perm("secretariador.delete_comisionado"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("secretariador.change_comisionado"):
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