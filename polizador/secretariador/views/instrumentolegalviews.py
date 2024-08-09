from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import InstrumentosLegalesDecretos, InstrumentosLegalesResoluciones
from secretariador.forms.instrumentoslegalesform import *
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg, pdflinkimg
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class CrearInstrumentoLegalDecreto(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_instrumentoslegalesdecretos"

	model = InstrumentosLegalesDecretos
	template_name = "instrumentoslegales/crear-instrumento-legal-decreto.html"
	form_class = InstrumentosLegalesDecretosForm
	success_url = reverse_lazy("secretariador:crear-decreto")
	
	title = "Crear Decreto"

	def get_title(self):
		return self.title

@method_decorator(login_required, name="dispatch")
class CrearInstrumentoLegalResolucion(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "instrumentoslegales/crear-instrumento-legal-resolucion.html"
	form_class = InstrumentosLegalesResolucionesForm
	success_url = reverse_lazy("secretariador:crear-resolucion")
	
	title = "Crear Resolución"

	def get_title(self):
		return self.title

@method_decorator(login_required, name="dispatch")
class UpdateInstrumentoLegalDecreto(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_instrumentoslegalesdecretos"

	model = InstrumentosLegalesDecretos
	template_name = "instrumentoslegales/update-instrumento-legal-decreto.html"
	form_class = InstrumentosLegalesDecretosForm
	success_url = reverse_lazy("secretariador:lista-decretos")

@method_decorator(login_required, name="dispatch")
class UpdateInstrumentoLegalResolucion(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "instrumentoslegales/update-instrumento-legal-resolucion.html"
	form_class = InstrumentosLegalesResolucionesForm
	success_url = reverse_lazy("secretariador:lista-resoluciones")
	
@method_decorator(login_required, name="dispatch")
class EliminarInstrumentoLegalDecreto(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_instrumentoslegalesdecretos"

	model = InstrumentosLegalesDecretos
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-decretos")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

@method_decorator(login_required, name="dispatch")
class EliminarInstrumentoLegalResolucion(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-resoluciones")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

# @method_decorator(login_required, name="dispatch")
# class VerSolicitud(generic.DetailView):
# 	login_url = "/"
# 	redirect_field_name = "login"
# 	model = Solicitud
# 	template_name = "solicitud/ver-solicitud.html"

@login_required
def PaginaListaInstrumentosLegalesDecretos(request):
	template_name = "Lista-decretos.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaListaInstrumentosLegalesDecretosView(AjaxDatatableView):
	model = InstrumentosLegalesDecretos
	title = "Instrumentos Legales(Decretos)"
	initial_order = [["instrumentolegaldecretos_ano", "desc"], ["instrumentolegaldecretos_numero", "desc"] ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":65},
		{"name": "id","title":"ID", "visible": False},
		{"name":"instrumentolegaldecretos_tipo", "className": "align-left"},
		{"name":"instrumentolegaldecretos_numero", "className": "align-left"},
		{"name":"instrumentolegaldecretos_ano", "className": "align-left "},
		{"name":"instrumentolegaldecretos_fecha_aprobacion", "className": "align-left "},
		{"name":"instrumentolegaldecretos_descripcion", "className": "align-right"},
		{"name":"PDF", "placeholder": True, "searchable": False, "orderable": False, "width":30},
	]

	def render_clip_value_as_html(self, long_text, short_text, is_clipped):
		"""
		Dada una versión larga y una corta de un texto, la siguiente representación HTML:
		<span title="long_text">short_text[ellipsis]</span>

		Para sobreescribir la función para mas customización.
		"""
		return '<span title="{long_text}">{short_text}{ellipsis}</span>'.format(
		long_text=long_text,
		short_text=short_text,
		ellipsis="&hellip;" if is_clipped else ""
		)

	def customize_row(self, row, obj):
		id = str(obj.id)
				
		editarlink = f'<a href="/viaticos/creardecreto/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/viaticos/creardecreto/ver/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/decreto/{id}">{eliminarlinkimg}</a>'
		pdfimg = f'<a href="{obj.instrumentolegaldecretos.url}">{pdflinkimg}</a>'

		if self.request.user.has_perm("secretariador.delete_instrumentoslegalesdecretos"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
			row["PDF"] = f"{pdfimg}"
		elif self.request.user.has_perm("secretariador.change_instrumentoslegalesdecretos"):
			row["edit"] = f"{editarlink}{detallelink}"
			row["PDF"] = f"{pdfimg}"
		else:
			row["edit"] = f"{detallelink}"
			row["PDF"] = f"{pdfimg}"

		# # Conversion de numeros con separador de miles "." y decimales ",2"
		# locale.setlocale(locale.LC_ALL, "")
		# row['certificado_monto_cobrar'] 	= locale.format_string("%.2f", obj.certificado_monto_cobrar, True)
		# row['certificado_monto_cobrar_uvi'] = locale.format_string("%.2f", obj.certificado_monto_cobrar_uvi, True)

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
	
@login_required
def PaginaListaInstrumentosLegalesResoluciones(request):
	template_name = "Lista-resoluciones.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaListaInstrumentosLegalesResolucionesView(AjaxDatatableView):
	model = InstrumentosLegalesResoluciones
	title = "Instrumentos Legales(Resoluciones)"
	initial_order = [["instrumentolegalresoluciones_ano", "desc"], ["instrumentolegalresoluciones_numero", "desc"] ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":65},
		{"name": "id","title":"ID", "visible": False},
		{"name":"instrumentolegalresoluciones_tipo", "className":"align-left"},
		{"name":"instrumentolegalresoluciones_numero", "className":"align-left"},
		{"name":"instrumentolegalresoluciones_ano", "className":"align-left "},
		{"name":"instrumentolegalresoluciones_fecha_aprobacion", "className":"align-left "},
		{"name":"instrumentolegalresoluciones_descripcion", "className":"align-right"},
		{"name":"PDF", "placeholder":True, "searchable": False, "orderable": False, "width":30},
	]

	def render_clip_value_as_html(self, long_text, short_text, is_clipped):
		"""
		Dada una versión larga y una corta de un texto, la siguiente representación HTML:
		<span title="long_text">short_text[ellipsis]</span>

		Para sobreescribir la función para mas customización.
		"""
		return '<span title="{long_text}">{short_text}{ellipsis}</span>'.format(
		long_text=long_text,
		short_text=short_text,
		ellipsis="&hellip;" if is_clipped else ""
		)

	def customize_row(self, row, obj):
		id = str(obj.id)
				
		editarlink = f'<a href="/viaticos/crearresolucion/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/viaticos/crearresolucion/ver/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/resolucion/{id}">{eliminarlinkimg}</a>'
		pdfimg = f"<a href={obj.instrumentolegalresoluciones.url}>{pdflinkimg}</a>"
		
		if self.request.user.has_perm("secretariador.delete_instrumentoslegalesresoluciones"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
			row["PDF"] = f"{pdfimg}"
		elif self.request.user.has_perm("secretariador.change_instrumentoslegalesresoluciones"):
			row["edit"] = f"{editarlink}{detallelink}"
			row["PDF"] = f"{pdfimg}"
		else:
			row["edit"] = f"{detallelink}"
			row["PDF"] = f"{pdfimg}"

		# # Conversion de numeros con separador de miles "." y decimales ",2"
		# locale.setlocale(locale.LC_ALL, "")
		# row['certificado_monto_cobrar'] 	= locale.format_string("%.2f", obj.certificado_monto_cobrar, True)
		# row['certificado_monto_cobrar_uvi'] = locale.format_string("%.2f", obj.certificado_monto_cobrar_uvi, True)

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