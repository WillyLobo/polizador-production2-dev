from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import Solicitud, InstrumentosLegalesDecretos
from carga.models import Provincia
from secretariador.forms.solicitudform import *
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg, generarlinkimg, pdflinkimg
from carga.views.generics import get_deleted_objects
import jinja2
from docxtpl import DocxTemplate

def solicitud_docx(request, pk):
	jinja_env = jinja2.Environment()
	jinja_env.trim_blocks = True
	jinja_env.lstrip_blocks = True

	actuacion = Solicitud.objects.get(pk=pk)
	agentes = actuacion.comisionadosolicitud_set.all().order_by("comisionadosolicitud_chofer")
	localidades = actuacion.solicitud_localidades.all()
	tareas = actuacion.solicitud_tareas
	fechas = actuacion.solicitud_fechas()
	vehiculo = actuacion.solicitud_vehiculo
	decreto_viaticos = actuacion.solicitud_decreto_viaticos.montoviaticodiario_decreto_reglamentario
	
	def separate_items(items):
	    # Concatenate the items in the list into a string
		concatenated_items = ", ".join(items)
		
		# Replace the last comma with "y"
		last_comma_index = concatenated_items.rfind(",")
		if last_comma_index != -1:
			concatenated_items = concatenated_items[:last_comma_index] + " y" + concatenated_items[last_comma_index + 1:]
		
		return concatenated_items

	def generate_agente_list(agentes):
		lista_agentes = []
		final_text = {}
		for agente in agentes:
			chofer = ""
			colaborador = ""
			agente_denominacion = f"{agente.comisionadosolicitud_nombre.comisionado_abreviatura} {agente.comisionadosolicitud_nombre.comisionado_nombres} {agente.comisionadosolicitud_nombre.comisionado_apellidos}"
			if agente.comisionadosolicitud_nombre.comisionado_sexo == "M":
				text = "el"
			else:
				text = "la"
				
			if agente.comisionadosolicitud_colaborador:
				colaborador = ", en carácter de colaborador"
			else:
				colaborador = ""
		
			if agente.comisionadosolicitud_chofer:
				if agente.comisionadosolicitud_nombre.comisionado_sexo == "M":
					chofer = f"el {agente_denominacion}"
				else:
					chofer = f"la {agente_denominacion}"

			if len(agentes) > 1:
				traslado = "trasladar a los mencionados agentes"
			else:
				traslado = "trasladar al mencionado agente"
			
			dni = "{:,}".format(agente.comisionadosolicitud_nombre.comisionado_dni).replace(",", "@").replace(".", ",").replace("@", ".")
			lista_agentes.append(f"{text} {agente_denominacion} - D.N.I.Nº{dni}{colaborador}")
		lista_agentes = separate_items(lista_agentes)

		final_text.update({
			"lista_agentes": lista_agentes,
			"traslado":traslado,
			"chofer":chofer,
		})
		return final_text

	def generate_localidad_list(localidades):
		lista_localidades = []
		final_text = ""
		if len(localidades) > 1:
			text_localidad = "las localidades de"
		else:
			text_localidad = "la localidad de"
		for localidad in localidades:
			lista_localidades.append(str(localidad.localidad_nombre))
		lista_localidades = separate_items(lista_localidades)
		
		final_text = f"{text_localidad} {lista_localidades}"
		return final_text

	def generate_fechas_list(fechas):
		lista_fechas = []
		final_text = ""
		if len(fechas) > 1:
			text_fechas = "los días"
		else:
			text_fechas = "el día"
		for fecha in fechas:
			lista_fechas.append(f"{fecha}")
		lista_fechas = separate_items(lista_fechas)

		final_text = f"{text_fechas} {lista_fechas}"
		return final_text

	def generate_agente_list_articulo(agentes):
		colaborador = ""
		
		final_text = []
		for agente in agentes:
			lista_agentes = []
			agente_cuit = f"{agente.comisionadosolicitud_nombre.comisionado_abreviatura} {agente.comisionadosolicitud_nombre.comisionado_nombreyapellido} – CUIL Nº{agente.comisionadosolicitud_nombre.comisionado_cuit}"
			cantidad_de_dias = f"{actuacion.solicitud_cantidad_de_dias.days} {' dias' if actuacion.solicitud_cantidad_de_dias.days > 1 else ' dia'}"
			comisionadosolicitud_combustible = "{:,.2f}".format(agente.comisionadosolicitud_combustible).replace(",", "@").replace(".", ",").replace("@", ".")
			comisionadosolicitud_pasaje = "{:,.2f}".format(agente.comisionadosolicitud_pasaje).replace(",", "@").replace(".", ",").replace("@", ".")
			comisionadosolicitud_gastos = "{:,.2f}".format(agente.comisionadosolicitud_gastos).replace(",", "@").replace(".", ",").replace("@", ".")
			valor_viatico_dia = "{:,.2f}".format(agente.valor_viatico_dia()).replace(",", "@").replace(".", ",").replace("@", ".")
			valor_viatico_total = "{:,.2f}".format(agente.viaticos_total()).replace(",", "@").replace(".", ",").replace("@", ".")

			subparrafo = f"(Viáticos: {cantidad_de_dias} a razón de ${valor_viatico_dia} diarios"
			if comisionadosolicitud_pasaje != "0,00":
				subparrafo += f" + Pasaje: ${comisionadosolicitud_pasaje}"
			if comisionadosolicitud_gastos != "0,00":
				subparrafo += f" + Gastos: ${comisionadosolicitud_gastos}"
			if comisionadosolicitud_combustible != "0,00":
				subparrafo += f" + Combustible: ${comisionadosolicitud_combustible}"
			subparrafo += f")."

			lista_agentes.append(agente_cuit)
			lista_agentes.append(valor_viatico_total)	
			lista_agentes.append(subparrafo)
			final_text.append(lista_agentes)
		return final_text

	lista_agentes       = generate_agente_list(agentes)
	lista_localidades   = generate_localidad_list(localidades)
	lista_fechas        = generate_fechas_list(fechas)
	lista_agentes_articulo = generate_agente_list_articulo(agentes)

	parrafo_uno     = f"Que por la misma se tramita autorización y anticipo de viáticos para {lista_agentes['lista_agentes']} de este Organismo, para trasladarse a {lista_localidades} {lista_fechas};"
	parrafo_dos     = f"Que dicha comisión, en el marco de las actividades del Organismo, tendrá como objetivo, {lista_agentes['traslado']}, a fin de {tareas} en {lista_localidades};"
	parrafo_tres_1  = f"Que el vehículo afectado será {vehiculo.vehiculo_modelo} – Dominio {vehiculo.vehiculo_patente}"
	parrafo_tres_2  = f", asegurado bajo póliza Nº{ vehiculo.vehiculo_poliza} emitida por {vehiculo.vehiculo_poliza_aseguradora}," if vehiculo.vehiculo_poliza else ""
	parrafo_tres_3  = f" conducido por {lista_agentes['chofer']};"
	parrafo_tres    = parrafo_tres_1+parrafo_tres_2+parrafo_tres_3
	parrafo_cuatro  = f"Que, en consecuencia, deben anticiparse los fondos necesarios para hacer frente a los gastos a realizar, de acuerdo a lo dispuesto en los Decretos Nº1324/1978 y Nº{decreto_viaticos.instrumentolegaldecretos_numero}/{decreto_viaticos.instrumentolegaldecretos_ano};"
	parrafo_cinco   = f"Que el trámite se encuadra dentro de lo establecido en el Decreto Nº 1324/78 – “Régimen de Viáticos”; y que debido a la fecha a realizarse, incluye días inhábiles deben encuadrarse dentro de las excepciones en el Inciso A; IV Decreto Nº211/20;"

	articulo_uno            = f"Autorizar a los agentes, detallados a continuación, a trasladarse a {lista_localidades}, {lista_fechas} a fin de {tareas} y anticipar los importes que se consignan, conforme con el Visto y Considerando de la presente, debiendo rendir cuentas documentadas de sus inversiones, de acuerdo con las reglamentaciones vigentes."
	articulo_dos            = lista_agentes_articulo

	if actuacion.solicitud_provincia.provincia_nombre == "Chaco":
		doc = DocxTemplate("secretariador/media/solicitud_template.docx")
		context = {
			"actuacion":actuacion,
			"parrafo_uno":parrafo_uno,
			"parrafo_dos":parrafo_dos,
			"parrafo_tres":parrafo_tres,
			"parrafo_cuatro":parrafo_cuatro,
			"parrafo_cinco":parrafo_cinco,
			"articulo_uno":articulo_uno,
			"articulo_dos":articulo_dos,
		}
	else:
		doc = DocxTemplate("secretariador/media/solicitud_exterior.docx")
		context = {
			"actuacion":actuacion,
			"parrafo_uno":parrafo_uno,
			"parrafo_dos":parrafo_dos,
			"parrafo_tres":parrafo_tres,
			"parrafo_cuatro":parrafo_cuatro,
			"parrafo_cinco":parrafo_cinco,
			"articulo_uno":articulo_uno,
			"articulo_dos":articulo_dos,
		}

	filename = actuacion.solicitud_actuacion+".docx"
	response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
	response["Content-Disposition"] = f'filename="{filename}"'
	doc.render(context)
	doc.save(response)
	return response

@method_decorator(login_required, name="dispatch")
class CrearSolicitud(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_solicitud"

	model = Solicitud
	template_name = "solicitud/crear-solicitud.html"
	form_class = SolicitudForm
	initial={
		"solicitud_provincia":Provincia.objects.all().filter(provincia_nombre__icontains="Chaco").last(),
		"solicitud_decreto_viaticos":InstrumentosLegalesDecretos.objects.filter(instrumentolegaldecretos_tipo="P").filter(instrumentolegaldecretos_descripcion__icontains="Viáticos").latest()
		}
	success_url = reverse_lazy("secretariador:crear-solicitud")
	
	title = "Crear Solicitud"

	def get_title(self):
		return self.title
	
	def get_context_data(self, **kwargs):
		context = super(CrearSolicitud, self).get_context_data(**kwargs)

		context["comisionadosformset"] = ComisionadoSolicitudFormset(instance=self.object)
		return context

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoSolicitudFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset = comisionadosformset))
	
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoSolicitudFormset(self.request.POST, instance=self.object)
		if form.is_valid() and comisionadosformset.is_valid():
			form.save()
			return self.form_valid(form, comisionadosformset)
		else:
			return self.form_invalid(form, comisionadosformset)

	def form_valid(self, form, formset):
		"""If the form is valid, save the associated model."""
		self.object = form.save()
		if formset.is_valid():
			response = super().form_valid(form)
			formset.instance = self.object
			formset.save()
			return response
		else:
			return super().form_invalid(form, formset)
	
	def form_invalid(self, form, comisionadosformset):
		"""
		Renders the response based on the context data with the form and formset if the form is invalid.

		:param form: The form instance.
		:param comisionadosformset: The comisionados formset instance.
		:return: The response rendered based on the context data.
		"""
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset=comisionadosformset))
	
@method_decorator(login_required, name="dispatch")
class UpdateSolicitud(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_solicitud"

	model = Solicitud
	template_name = "solicitud/update-solicitud.html"
	form_class = SolicitudForm
	success_url = reverse_lazy("secretariador:lista-solicitudes")
	
	def get_context_data(self, **kwargs):
		context = super(UpdateSolicitud, self).get_context_data(**kwargs)

		context["comisionadosformset"] = ComisionadoSolicitudFormset(instance=self.object)
		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoSolicitudFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset = comisionadosformset))
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoSolicitudFormset(self.request.POST, instance=self.object)
		if form.is_valid() and comisionadosformset.is_valid():
			form.save()
			return self.form_valid(form, comisionadosformset)
		else:
			return self.form_invalid(form, comisionadosformset)
		
	def form_valid(self, form, comisionadosformset):
		formset = comisionadosformset.save(commit=False)
		for field in formset:
			field.comisionadosolicitud_foreign = self.object
			field.save()
		return redirect(reverse_lazy("secretariador:lista-solicitudes"))
	
	def form_invalid(self, form, comisionadosformset):
		"""
		Renders the response based on the context data with the form and formset if the form is invalid.

		:param form: The form instance.
		:param comisionadosformset: The comisionados formset instance.
		:return: The response rendered based on the context data.
		"""
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset=comisionadosformset))


@method_decorator(login_required, name="dispatch")
class EliminarSolicitud(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_solicitud"

	model = Solicitud
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-solicitudes")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context
	
@method_decorator(login_required, name="dispatch")
class VerSolicitud(generic.DetailView):
	login_url = "/"
	redirect_field_name = "login"
	model = Solicitud
	template_name = "solicitud/ver-solicitud.html"

@login_required
def PaginaListaSolicitudes(request):
	template_name = "Lista-solicitudes.html"

	return render(request, template_name, {})
@method_decorator(login_required, name="dispatch")
class ListaSolicitudesView(AjaxDatatableView):
	model = Solicitud
	title = "Solicitudes"
	initial_order = [["solicitud_actuacion_ano", "desc"], ["solicitud_actuacion_numero", "desc"]]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":81},
		{"name": "id","title":"ID", "visible": False},
		{"name":"solicitud_actuacion_ano"},
		{"name":"solicitud_actuacion_numero"},
		{"name":"solicitud_solicitante", "foreign_field":"solicitud_solicitante__comisionado_nombreyapellido"},
		{"name":"Comisionados", "placeholder":True, "searchable": False, "orderable": False},
		{"name":"solicitud_localidades", "m2m_foreign_field": "solicitud_localidades__localidad_nombre", "visible": True},
		{"name":"solicitud_fecha_desde"},
		{"name":"solicitud_fecha_hasta"},
		{"name":"solicitud_tareas", "max_length":100},
		{"name":"solicitud_vehiculo", "foreign_field":"solicitud_vehiculo__vehiculo_str", "choices":True, "autofilter":True},
		{"name":"solicitud_dia_inhabil", "choices":True, "autofilter":True},
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

		if obj.solicitud_provincia.provincia_nombre == "Chaco":				
			editarlink = f'<a href="/viaticos/crearsolicitud/{id}">{editlinkimg}</a>'
			if obj.solicitud_resolucion is not None:
				detallelink = f'<a href="{str(obj.solicitud_resolucion.instrumentolegalresoluciones.url)}">{pdflinkimg}</a>'
			else:
				detallelink = ""
			eliminarlink = f'<a href="/viaticos/eliminar/solicitud/{id}">{eliminarlinkimg}</a>'
			generarlink = f'<a href="/viaticos/creardocumento/solicitud/{id}">{generarlinkimg}</a>'
		else:
			editarlink = f'<a href="/viaticos/crearsolicitudexterior/{id}">{editlinkimg}</a>'
			if obj.solicitud_resolucion is not None:
				detallelink = f'<a href="{str(obj.solicitud_resolucion.instrumentolegalresoluciones.url)}">{pdflinkimg}</a>'
			else:
				detallelink = ""
			eliminarlink = f'<a href="/viaticos/eliminar/solicitudexterior/{id}">{eliminarlinkimg}</a>'
			generarlink = f'<a href="/viaticos/creardocumento/solicitudexterior/{id}">{generarlinkimg}</a>'

		if self.request.user.has_perm("secretariador.delete_solicitud"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}{generarlink}"
		elif self.request.user.has_perm("secretariador.change_solicitud"):
			row["edit"] = f"{editarlink}{detallelink}{generarlink}"
		else:
			row["edit"] = f"{detallelink}"

		# Get list of comisionados for this solicitud, joining them wih ";" for display
		comisionados = obj.comisionadosolicitud_set.all()
		row["Comisionados"] = "; ".join(c.comisionadosolicitud_nombre.comisionado_nombreyapellido for c in comisionados)
	
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