from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import Incorporacion, InstrumentosLegalesDecretos
from carga.models import Provincia
from secretariador.forms.incorporacionform import *
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg, generarlinkimg
from carga.views.generics import get_deleted_objects
import jinja2


from docxtpl import DocxTemplate

def incorporacion_docx(request, pk):
	jinja_env = jinja2.Environment()
	jinja_env.trim_blocks = True
	jinja_env.lstrip_blocks = True

	actuacion = Incorporacion.objects.get(pk=pk)
	numero_actuacion = actuacion.incorporacion_actuacion
	resolucion_solicitud = actuacion.incorporacion_solicitud.solicitud_resolucion
	agentes_incorporacion = actuacion.comisionadosolicitud_set.all().order_by("comisionadosolicitud_chofer")
	agentes_solicitud = actuacion.incorporacion_solicitud.comisionadosolicitud_set.all().order_by("comisionadosolicitud_chofer")
	localidades = actuacion.incorporacion_solicitud.solicitud_localidades.all()
	tareas = actuacion.incorporacion_solicitud.solicitud_tareas
	fechas = actuacion.incorporacion_solicitud.solicitud_fechas()
	dia_inhabil = actuacion.incorporacion_solicitud.solicitud_dia_inhabil
	vehiculo = actuacion.incorporacion_solicitud.solicitud_vehiculo
	decreto_viaticos = actuacion.incorporacion_solicitud.solicitud_decreto_viaticos.montoviaticodiario_decreto_reglamentario
	
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
				colaborador = " en carácter de colaborador"
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
			cantidad_de_dias = f"{actuacion.incorporacion_solicitud.solicitud_cantidad_de_dias.days} {' dias' if actuacion.incorporacion_solicitud.solicitud_cantidad_de_dias.days > 1 else ' dia'}"
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

	lista_agentes       = generate_agente_list(agentes_solicitud)
	lista_agentes_incorporacion = generate_agente_list(agentes_incorporacion)
	lista_localidades   = generate_localidad_list(localidades)
	lista_fechas        = generate_fechas_list(fechas)
	lista_agentes_articulo = generate_agente_list_articulo(agentes_solicitud)
	lista_agentes_incorporacion_articulo = generate_agente_list_articulo(agentes_incorporacion)

	parrafo_uno		= f"Que por la {resolucion_solicitud}, se tramitó autorización y anticipo de viáticos para {lista_agentes['lista_agentes']} de este Organismo, a fin de {tareas}, en {lista_localidades} {lista_fechas};"
	parrafo_dos     = f"Que resulta necesario incorporar a la misma, a {lista_agentes_incorporacion['lista_agentes']} de este Organismo;"
	parrafo_tres  = f"Que, en consecuencia, deben anticiparse los fondos necesarios para hacer frente a los gastos a realizar, de acuerdo a lo dispuesto en los Decretos Nº1324/1978 y Nº{decreto_viaticos.instrumentolegaldecretos_numero}/{decreto_viaticos.instrumentolegaldecretos_ano};"
	parrafo_cuatro   = f"Que el trámite se encuadra dentro de lo establecido en el Decreto Nº 1324/78 – “Régimen de Viáticos”; y que debido a la fecha a realizarse, incluye días inhábiles deben encuadrarse dentro de las excepciones en el Inciso A; IV Decreto Nº211/20;"

	articulo_uno            = f"Incorporar a los agentes, detallados a continuación, a trasladarse a {lista_localidades}, {lista_fechas} a fin de {tareas} y anticipar los importes que se consignan, conforme con el Visto y Considerando de la presente, debiendo rendir cuentas documentadas de sus inversiones, de acuerdo con las reglamentaciones vigentes."
	articulo_dos            = lista_agentes_incorporacion_articulo

	doc = DocxTemplate("secretariador/media/solicitud_incorporacion.docx")
	context = {
		"actuacion":actuacion,
		"numero_actuacion":numero_actuacion,
		"dia_inhabil":dia_inhabil,
		"resolucion_solicitud":resolucion_solicitud,
		"parrafo_uno":parrafo_uno,
		"parrafo_dos":parrafo_dos,
		"parrafo_tres":parrafo_tres,
		"parrafo_cuatro":parrafo_cuatro,
		"articulo_uno":articulo_uno,
		"articulo_dos":articulo_dos,
	}

	filename = actuacion.incorporacion_actuacion+".docx"
	response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
	response["Content-Disposition"] = f'filename="{filename}"'
	doc.render(context)
	doc.save(response)
	return response

@method_decorator(login_required, name="dispatch")
class CrearIncorporacion(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_incorporacion"

	model = Incorporacion
	template_name = "incorporacion/crear-incorporacion.html"
	form_class = IncorporacionForm
	success_url = reverse_lazy("secretariador:crear-incorporacion")
	
	title = "Crear Incorporacion"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super(CrearIncorporacion, self).get_context_data(**kwargs)
		if self.request.POST:
			context['group_formset'] = ComisionadoIncorporacionFormset(self.request.POST, instance=self.object)
			# por que esta vergación tiene que estar acá para que los errores del formset se muestren correctamente?
			context.get('group_formset').errors
		else:
			context['group_formset'] = ComisionadoIncorporacionFormset(instance=self.object)

		return context

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoIncorporacionFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset = comisionadosformset))
	
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoIncorporacionFormset(self.request.POST, instance=self.object)
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
class UpdateIncorporacion(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_incorporacion"

	model = Incorporacion
	template_name = "incorporacion/update-incorporacion.html"
	form_class = IncorporacionForm
	success_url = reverse_lazy("secretariador:lista-incorporaciones")
	
	def get_context_data(self, **kwargs):
		context = super(UpdateIncorporacion, self).get_context_data(**kwargs)
		if self.request.POST:
			context['group_formset'] = ComisionadoIncorporacionFormset(self.request.POST, instance=self.object)
			# por que esta vergación tiene que estar acá para que los errores del formset se muestren correctamente?
			context.get('group_formset').errors
		else:
			context['group_formset'] = ComisionadoIncorporacionFormset(instance=self.object)

		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoIncorporacionFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset = comisionadosformset))
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoIncorporacionFormset(self.request.POST, instance=self.object)
		if form.is_valid() and comisionadosformset.is_valid():
			form.save()
			return self.form_valid(form, comisionadosformset)
		else:
			return self.form_invalid(form, comisionadosformset)
		
	def form_valid(self, form, comisionadosformset):
		formset = comisionadosformset.save(commit=False)
		for field in formset:
			field.comisionadosolicitud_incorporacion_foreign = self.object
			field.save()
		return redirect(reverse_lazy("secretariador:lista-incorporaciones"))
	
	def form_invalid(self, form, comisionadosformset):
		"""
		Renders the response based on the context data with the form and formset if the form is invalid.

		:param form: The form instance.
		:param comisionadosformset: The comisionados formset instance.
		:return: The response rendered based on the context data.
		"""
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset=comisionadosformset))


@method_decorator(login_required, name="dispatch")
class EliminarIncorporacion(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_incorporacion"

	model = Incorporacion
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-incorporaciones")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context
	
# @method_decorator(login_required, name="dispatch")
# class VerIncorporacion(generic.DetailView):
# 	login_url = "/"
# 	redirect_field_name = "login"
# 	model = Solicitud
# 	template_name = "solicitud/ver-incorporacion.incorporacion_solicitud.html"

@login_required
def PaginaListaIncorporaciones(request):
	template_name = "Lista-incorporaciones.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaIncorporacionesView(AjaxDatatableView):
	model = Incorporacion
	title = "Incorporaciones"
	initial_order = [["incorporacion_actuacion_ano", "desc"], ["incorporacion_actuacion_numero", "desc"]]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":81},
		{"name": "id","title":"ID", "visible": False},
		{"name":"incorporacion_actuacion_ano"},
		{"name":"incorporacion_actuacion_numero"},
		{"name":"incorporacion_solicitud", "foreign_field":"incorporacion_solicitud__solicitud_actuacion"},
		{"name":"incorporacion_solicitante", "foreign_field":"incorporacion_solicitante__comisionado_nombreyapellido"},
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
				
		editarlink = f'<a href="/viaticos/crearincorporacion/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/viaticos/crearincorporacion/ver/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/incorporacion/{id}">{eliminarlinkimg}</a>'
		generarlink = f'<a href="/viaticos/creardocumento/incorporacion/{id}">{generarlinkimg}</a>'
		
		if self.request.user.has_perm("secretariador.delete_incorporacion"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}{generarlink}"
		elif self.request.user.has_perm("secretariador.change_incorporacion"):
			row["edit"] = f"{editarlink}{detallelink}{generarlink}"
		else:
			row["edit"] = f"{detallelink}"

		# # Get list of comisionados for this solicitud, joining them wih ";" for display
		# if obj.get_comisionados():
		# 	row["Comisionados"] = "; ".join(c for c in obj.get_comisionados())

		# return
	
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