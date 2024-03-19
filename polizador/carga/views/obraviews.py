from ajax_datatable.views import AjaxDatatableView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.template import loader, TemplateDoesNotExist
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Obra
from carga.forms.obraforms import *
from django.utils.formats import date_format
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from carga.views.generics import get_deleted_objects
import locale

@method_decorator(login_required, name="dispatch")
class EliminarObra(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
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
class CrearObra(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
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


@method_decorator(login_required, name="dispatch")
class UpdateObra(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.change_obra"

	model = Obra
	template_name = "obra/update-obra.html"
	form_class = ObraForm
	success_url = reverse_lazy("carga:lista-obras")

@method_decorator(login_required, name="dispatch")
class EstadoObra(generic.DetailView):
	login_url = "/"
	redirect_field_name = "login"
	
	model = Obra
	template_name = "obra/estado-obra.html"

	def get_context_data(self, **kwargs):
		context = super(EstadoObra, self).get_context_data(**kwargs)
		obra = Obra.objects.get(pk=self.object.pk)
		certificados = obra.certificado_set.all().order_by("certificado_fecha")
		vivienda_nacion_fecha = []
		vivienda_nacion_pesos = []
		vivienda_nacion_acumulado = []
		vivienda_nacion_certificados = []
		vivienda_provincia_fecha = []
		vivienda_provincia_pesos = []
		vivienda_provincia_acumulado = []
		vivienda_provincia_certificados = []
		frentista_nacion_fecha = []
		frentista_nacion_pesos = []
		frentista_nacion_acumulado = []
		frentista_nacion_certificados = []
		frentista_provincia_fecha = []
		frentista_provincia_pesos = []
		frentista_provincia_acumulado = []
		frentista_provincia_certificados = []
		nexos_nacion_fecha = []
		nexos_nacion_pesos = []
		nexos_nacion_acumulado = []
		nexos_nacion_certificados = []
		nexos_provincia_fecha = []
		nexos_provincia_pesos = []
		nexos_provincia_acumulado = []
		nexos_provincia_certificados = []

		for certificado in certificados:
			if certificado.certificado_rubro_db.certificadorubro_nombre_corto == "V":
				if certificado.certificado_financiamiento == "N":
					vivienda_nacion_fecha.append(date_format(certificado.certificado_fecha,format="b/y"))
					vivienda_nacion_pesos.append(float(certificado.certificado_monto_pesos))
					vivienda_nacion_acumulado.append(float(certificado.certificado_acum_pct))
					vivienda_nacion_certificados.append(certificado)
				elif certificado.certificado_financiamiento == "P":
					vivienda_provincia_fecha.append(date_format(certificado.certificado_fecha, format="b/y"))
					vivienda_provincia_pesos.append(float(certificado.certificado_monto_pesos))
					vivienda_provincia_acumulado.append(float(certificado.certificado_acum_pct))
					vivienda_provincia_certificados.append(certificado)
			elif certificado.certificado_rubro_db.certificadorubro_nombre_corto == "F":
				if certificado.certificado_financiamiento == "N":
					frentista_nacion_fecha.append(date_format(certificado.certificado_fecha, format="b/y"))
					frentista_nacion_pesos.append(float(certificado.certificado_monto_pesos))
					frentista_nacion_acumulado.append(float(certificado.certificado_acum_pct))
					frentista_nacion_certificados.append(certificado)
				elif certificado.certificado_financiamiento == "P":
					frentista_provincia_fecha.append(date_format(certificado.certificado_fecha, format="b/y"))
					frentista_provincia_pesos.append(float(certificado.certificado_monto_pesos))
					frentista_provincia_acumulado.append(float(certificado.certificado_acum_pct))
					frentista_provincia_certificados.append(certificado)
			elif certificado.certificado_rubro_db.certificadorubro_nombre_corto == "I":
				if certificado.certificado_financiamiento == "N":
					nexos_nacion_fecha.append(date_format(certificado.certificado_fecha, format="b/y"))
					nexos_nacion_pesos.append(float(certificado.certificado_monto_pesos))
					nexos_nacion_acumulado.append(float(certificado.certificado_acum_pct))
					nexos_nacion_certificados.append(certificado)
				elif certificado.certificado_financiamiento == "P":
					nexos_provincia_fecha.append(date_format(certificado.certificado_fecha, format="b/y"))
					nexos_provincia_pesos.append(float(certificado.certificado_monto_pesos))
					nexos_provincia_acumulado.append(float(certificado.certificado_acum_pct))
					nexos_provincia_certificados.append(certificado)

		
		context["certificados_vivienda_nacion_fecha"] = vivienda_nacion_fecha
		context["certificados_vivienda_nacion_pesos"] = vivienda_nacion_pesos
		context["certificados_vivienda_nacion_acumulado"] = vivienda_nacion_acumulado
		context["certificados_vivienda_nacion"] = vivienda_nacion_certificados
		context["certificados_vivienda_provincia_fecha"] = vivienda_provincia_fecha
		context["certificados_vivienda_provincia_pesos"] = vivienda_provincia_pesos
		context["certificados_vivienda_provincia_acumulado"] = vivienda_provincia_acumulado
		context["certificados_vivienda_provincia"] = vivienda_provincia_certificados
		context["certificados_frentista_nacion_fecha"] = frentista_nacion_fecha
		context["certificados_frentista_nacion_pesos"] = frentista_nacion_pesos
		context["certificados_frentista_nacion_acumulado"] = frentista_nacion_acumulado
		context["certificados_frentista_nacion"] = frentista_nacion_certificados
		context["certificados_frentista_provincia_fecha"] = frentista_provincia_fecha
		context["certificados_frentista_provincia_pesos"] = frentista_provincia_pesos
		context["certificados_frentista_provincia_acumulado"] = frentista_provincia_acumulado
		context["certificados_frentista_provincia"] = frentista_provincia_certificados
		context["certificados_nexos_nacion_fecha"] = nexos_nacion_fecha
		context["certificados_nexos_nacion_pesos"] = nexos_nacion_pesos
		context["certificados_nexos_nacion_acumulado"] = nexos_nacion_acumulado
		context["certificados_nexos_nacion"] = nexos_nacion_certificados
		context["certificados_nexos_provincia_fecha"] = nexos_provincia_fecha
		context["certificados_nexos_provincia_pesos"] = nexos_provincia_pesos
		context["certificados_nexos_provincia_acumulado"] = nexos_provincia_acumulado
		context["certificados_nexos_provincia"] = nexos_provincia_certificados

		return context

@login_required
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

@method_decorator(login_required, name="dispatch")
class ListaObrasView(AjaxDatatableView):
	model = Obra
	title = "Obras"
	initial_order = [["id", "desc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{"name": "id", "visible": True},
		{"name": "obra_programa", "foreign_field": "obra_programa__programa_nombre"},
		{"name": "obra_convenio", "title":"Convenio"},
		{"name": "obra_nombre", "visible": True, "title":"Obra", "max_length":100},
		{"name": "obra_empresa", "foreign_field": "obra_empresa__empresa_nombre", "visible": True},
		{"name": "obra_localidad_m", "m2m_foreign_field": "obra_localidad_m__localidad_nombre", "visible": True},
		{"name": "obra_acumulado", "title":"Avance Acumulado", "searchable":False, "orderable":False},
		{'name': 'edit', 'title': 'Acciones', 'placeholder': True, 'searchable': False, 'orderable': False},
	]
	
	def customize_row(self, row, obj):
		if obj.certificado_set:
				if obj.certificado_set.last():
					acumulado = str(obj.certificado_set.latest("certificado_fecha").certificado_acum_pct)
				else:
					acumulado = "0.00"
		if obj is not None:
			row['obra_acumulado'] = acumulado+"%"
		else:
			row['obra_acumulado'] = ''

		id = str(obj.id)
		editarlink = f"<a href='/polizas/crear/obra/{id}'>{editlinkimg}</a>"
		detallelink = f"<a href='/polizas/crear/obra/estado/{id}'>{detallelinkimg}</a>"
		eliminarlink = f"<a href='/polizas/eliminar/obra/{id}'>{eliminarlinkimg}</a>"
		if self.request.user.has_perm("carga.delete_obra"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("carga.change_obra"):
			row["edit"] = f"{editarlink}{detallelink}"
		else:
			row["edit"] = f"{detallelink}"

		return

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
def PaginaListaObrasExtendida(request):
	template_name = "Lista-obras-extendida.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaObrasExtendidaView(AjaxDatatableView):
	model = Obra
	title = "Obras"
	initial_order = [["id", "desc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{"name": "id", "visible": True},
		{"name": "obra_nombre", "visible": True, "title":"Obra", "max_length":100},
		{"name": "obra_soluciones", "title":"Cant. Soluciones"},
		{"name": "obra_empresa", "foreign_field": "obra_empresa__empresa_nombre", "visible": True},
		{"name": "obra_region", "title":"Región", "foreign_field": "obra_region__region_numero"},
		{"name": "obra_departamento_m", "title": "Departamento", "m2m_foreign_field": "obra_departamento_m__departamento_nombre"},
		{"name": "obra_municipio_m", "title": "Municipio", "m2m_foreign_field": "obra_municipio_m__municipio_nombre"},
		{"name": "obra_localidad_m", "m2m_foreign_field": "obra_localidad_m__localidad_nombre", "visible": True},
		{"name": "obra_conjunto", "foreign_field": "obra_conjunto__conjunto_nombre", "max_length":100},
		{"name": "obra_grupo", "title": "Grupo"},
		{"name": "obra_plazo", "title": "Plazo"},
		{"name": "obra_programa", "title": "Programa", "foreign_field": "obra_programa__programa_nombre", "max_length":100, "choices": True, "autofilter": True},
		{"name": "obra_convenio", "title": "Convenio"},
		{"name": "obra_expediente", "title": "Expediente"},
		{"name": "obra_resolucion", "title": "Resolución"},
		{"name": "obra_licitacion_tipo", "title": "Compulsa", "choices": True, "autofilter": True},
		{"name": "obra_licitacion_numero", "title": "Numero"},
		{"name": "obra_licitacion_ano", "title": "Año", "choices": True, "autofilter": True},
		{"name": "obra_nomenclatura", "title": "Nomenclatura Catastral", "max_length":100},
		{"name": "obra_nomenclatura_plano", "title": "Número de Plano"},
		{"name": "obra_fecha_entrega", "title": "Fecha de Entrega"},
		{"name": "obra_fecha_contrato", "title": "Fecha de Contrato"},
		{"name": "obra_inspector", "title": "Inspector", "searchable":False},
		{"name": "obra_observaciones", "title": "Observaciones", "max_length":100},
		{"name": "obra_contrato_nacion_pesos", "title": "Contrato Nacion Pesos"},
		{"name": "obra_contrato_nacion_uvi", "title": "Contrato Nacion UVI"},
		{"name": "obra_contrato_nacion_uvi_fecha", "title": "Fecha UVI"},
		{"name": "obra_contrato_provincia_pesos", "title": "Contrato Provincia Pesos"},
		{"name": "obra_contrato_provincia_uvi", "title": "Contrato Provincia UVI"},
		{"name": "obra_contrato_provincia_uvi_fecha", "title": "Fecha UVI"},
		{"name": "obra_contrato_terceros_pesos", "title": "Contrato Terceros Pesos"},
		{"name": "obra_contrato_terceros_uvi", "title": "Contrato Terceros UVI"},
		{"name": "obra_contrato_terceros_uvi_fecha", "title": "Fecha UVI"},
		{"name": "obra_principal", "title": "Obra Madre", "m2m_foreign_field": "obra_principal__obra_nombre", "max_length":100},
		{"name": "obra_acumulado", "title":"Avance Acumulado", "searchable":False},
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False},
	]

	def customize_row(self, row, obj):
		"""
		Obtiene último % Acumulado en la Columna "obra_acumulado".
		"""
		if obj.certificado_set:
				if obj.certificado_set.last():
					acumulado = str(obj.certificado_set.last().certificado_acum_pct)
				else:
					acumulado = "0.00"
		if obj is not None:
			row['obra_acumulado'] = acumulado+"%"
		else:
			row['obra_acumulado'] = ''
		
		row["obra_inspector"] = ", ".join(str(agente) for agente in obj.obra_inspector.all() if obj.obra_inspector.all())
		
		id = str(obj.id)
		if self.request.user.has_perm("carga.change_obra"):
			row["edit"] = '<a href="/polizas/crear/obra/{id}"><img src="/static/edit.png" title="Editar" width="30" height="30" /></a> <a href="/polizas/crear/obra/estado/{id}"><img src="/static/search.svg" title="Detalles" width="30" heigth="30" /></a>'.format(id=id)
		else:
			row["edit"] = '<a href="/polizas/crear/obra/estado/{id}"><img src="/static/search.svg" title="Detalles" width="30" heigth="30" /></a>'.format(id=id)
		
		# Conversion de numeros con separador de miles "." y decimales ",2"
		locale.setlocale(locale.LC_ALL, "")
		row['obra_contrato_nacion_pesos'] 		= locale.format_string("%.2f", obj.obra_contrato_nacion_pesos, True)
		row['obra_contrato_nacion_uvi'] 		= locale.format_string("%.2f", obj.obra_contrato_nacion_uvi, True)
		row['obra_contrato_provincia_pesos'] 	= locale.format_string("%.2f", obj.obra_contrato_provincia_pesos, True)
		row['obra_contrato_provincia_uvi'] 		= locale.format_string("%.2f", obj.obra_contrato_provincia_uvi, True)
		row['obra_contrato_terceros_pesos'] 	= locale.format_string("%.2f", obj.obra_contrato_terceros_pesos, True)
		row['obra_contrato_terceros_uvi'] 		= locale.format_string("%.2f", obj.obra_contrato_terceros_uvi, True)

		return

	def render_clip_value_as_html(self, long_text, short_text, is_clipped):
		"""
		Dada una versión larga y una corta de un text, la siguiente representación HTML:
		<span title="long_text">short_text[ellipsis]</span>

		Para sobreescribir la función para mas customización.
		"""
		return '<span title="{long_text}">{short_text}{ellipsis}</span>'.format(
		long_text=long_text,
		short_text=short_text,
		ellipsis="&hellip;" if is_clipped else ""
		)
	
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
