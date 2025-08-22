from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import InstrumentosLegalesMemorandum, InstrumentosLegalesDecretos, InstrumentosLegalesResoluciones, InstrumentosLegalesResolucionesDirectorio
from secretariador.forms.instrumentoslegalesform import *
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg, pdflinkimg
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class CrearInstrumentoLegalMemorandum(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_instrumentoslegalesmemorandum"

	model = InstrumentosLegalesMemorandum
	template_name = "instrumentoslegales/crear-instrumento-legal-memorandum.html"
	form_class = InstrumentosLegalesMemorandumForm
	success_url = reverse_lazy("secretariador:crear-memorandum")
	
	title = "Crear Memorandum"

	def get_title(self):
		return self.title
	
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
class CrearInstrumentoLegalResolucionPresidencia(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "instrumentoslegales/crear-instrumento-legal-resolucion-presidencia.html"
	form_class = InstrumentosLegalesResolucionesPresidenciaForm
	success_url = reverse_lazy("secretariador:crear-resolucion-presidencia")
	
	title = "Crear Resolución"

	def get_title(self):
		return self.title
	
@method_decorator(login_required, name="dispatch")
class CrearInstrumentoLegalResolucionDirectorio(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResolucionesDirectorio
	template_name = "instrumentoslegales/crear-instrumento-legal-resolucion-directorio.html"
	form_class = InstrumentosLegalesResolucionesDirectorioForm
	success_url = reverse_lazy("secretariador:crear-resolucion-directorio")
	
	title = "Crear Resolución(Directorio)"

	def get_title(self):
		return self.title

@method_decorator(login_required, name="dispatch")
class UpdateInstrumentoLegalMemorandum(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_instrumentoslegalesmemorandum"

	model = InstrumentosLegalesMemorandum
	template_name = "instrumentoslegales/update-instrumento-legal-memorandum.html"
	form_class = InstrumentosLegalesMemorandumForm
	success_url = reverse_lazy("secretariador:lista-memorandum")

	def get_context_data(self,*args, **kwargs):
		context = super(type(self), self).get_context_data(*args,**kwargs)
		objetoanterior = self.model.objects.filter(pk=self.object.id - 1)
		objetosiguiente = self.model.objects.filter(pk=self.object.id + 1)
		
		context['idanteriorobjeto'] = objetoanterior.first() if objetoanterior.exists() else None
		context['idsiguienteobjeto'] = objetosiguiente.first() if objetosiguiente.exists() else None
		
		return context

@method_decorator(login_required, name="dispatch")
class UpdateInstrumentoLegalDecreto(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_instrumentoslegalesdecretos"

	model = InstrumentosLegalesDecretos
	template_name = "instrumentoslegales/update-instrumento-legal-decreto.html"
	form_class = InstrumentosLegalesDecretosForm
	success_url = reverse_lazy("secretariador:lista-decretos")

	def get_context_data(self,*args, **kwargs):
		context = super(type(self), self).get_context_data(*args,**kwargs)
		objetoanterior = self.model.objects.filter(pk=self.object.id - 1)
		objetosiguiente = self.model.objects.filter(pk=self.object.id + 1)
		
		context['idanteriorobjeto'] = objetoanterior.first() if objetoanterior.exists() else None
		context['idsiguienteobjeto'] = objetosiguiente.first() if objetosiguiente.exists() else None
		
		return context

@method_decorator(login_required, name="dispatch")
class UpdateInstrumentoLegalResolucionPresidencia(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "instrumentoslegales/update-instrumento-legal-resolucion-presidencia.html"
	form_class = InstrumentosLegalesResolucionesPresidenciaForm
	success_url = reverse_lazy("secretariador:lista-resoluciones")

	def get_context_data(self,*args, **kwargs):
		context = super(type(self), self).get_context_data(*args,**kwargs)
		objetoanterior = self.model.objects.filter(pk=self.object.id - 1)
		objetosiguiente = self.model.objects.filter(pk=self.object.id + 1)
		
		context['idanteriorobjeto'] = objetoanterior.first() if objetoanterior.exists() else None
		context['idsiguienteobjeto'] = objetosiguiente.first() if objetosiguiente.exists() else None
		
		return context
	
class UpdateInstrumentoLegalResolucionDirectorio(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResolucionesDirectorio
	template_name = "instrumentoslegales/update-instrumento-legal-resolucion-directorio.html"
	form_class = InstrumentosLegalesResolucionesDirectorioForm
	success_url = reverse_lazy("secretariador:lista-resoluciones-directorio")
	
	def get_context_data(self,*args, **kwargs):
		context = super(type(self), self).get_context_data(*args,**kwargs)
		objetoanterior = self.model.objects.filter(pk=self.object.id - 1)
		objetosiguiente = self.model.objects.filter(pk=self.object.id + 1)
		
		context['idanteriorobjeto'] = objetoanterior.first() if objetoanterior.exists() else None
		context['idsiguienteobjeto'] = objetosiguiente.first() if objetosiguiente.exists() else None
		
		return context

@method_decorator(login_required, name="dispatch")
class EliminarInstrumentoLegalMemorandum(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_instrumentoslegalesmemorandum"

	model = InstrumentosLegalesMemorandum
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-memorandum")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

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
class EliminarInstrumentoLegalResolucionPresidencia(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-resoluciones-presidencia")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

@method_decorator(login_required, name="dispatch")
class EliminarInstrumentoLegalResolucionDirectorio(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResolucionesDirectorio
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-resoluciones-directorio")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

@login_required
def PaginaListaInstrumentosLegalesMemorandum(request):
	template_name = "Lista-memorandum.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaListaInstrumentosLegalesMemorandumView(AjaxDatatableView):
	model = InstrumentosLegalesMemorandum
	title = "Instrumentos Legales(Memorandum)"
	initial_order = [["instrumentolegalmemorandum_ano", "desc"], ["instrumentolegalmemorandum_numero", "desc"] ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":65},
		{"name": "id","title":"ID", "visible": False},
		{"name":"instrumentolegalmemorandum_tipo", "className": "align-left"},
		{"name":"instrumentolegalmemorandum_numero", "className": "align-left"},
		{"name":"instrumentolegalmemorandum_ano", "className": "align-left "},
		{"name":"instrumentolegalmemorandum_fecha_aprobacion", "className": "align-left "},
		{"name":"instrumentolegalmemorandum_descripcion", "className": "align-right"},
		{"name":"instrumentolegalmemorandum_document", "className":"align-right", "max_length":200, "orderable": False},
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
				
		editarlink = f'<a href="/viaticos/crearmemorandum/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/viaticos/crearmemorandum/ver/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/memorandum/{id}">{eliminarlinkimg}</a>'

		if self.request.user.has_perm("secretariador.delete_instrumentoslegalesmemorandum"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("secretariador.change_instrumentoslegalesmemorandum"):
			row["edit"] = f"{editarlink}{detallelink}"
		else:
			row["edit"] = f"{detallelink}"

		# # Conversion de numeros con separador de miles "." y decimales ",2"
		# locale.setlocale(locale.LC_ALL, "")
		# row['certificado_monto_cobrar'] 	= locale.format_string("%.2f", obj.certificado_monto_cobrar, True)
		# row['certificado_monto_cobrar_uvi'] = locale.format_string("%.2f", obj.certificado_monto_cobrar_uvi, True)

		return

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
				
		editarlink = f'<a href="{obj.get_absolute_url()}">{editlinkimg}</a>'
		detallelink = f'<a href="/viaticos/creardecreto/ver/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/decreto/{id}">{eliminarlinkimg}</a>'

		if self.request.user.has_perm("secretariador.delete_instrumentoslegalesdecretos"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("secretariador.change_instrumentoslegalesdecretos"):
			row["edit"] = f"{editarlink}{detallelink}"
		else:
			row["edit"] = f"{detallelink}"

		# # Conversion de numeros con separador de miles "." y decimales ",2"
		# locale.setlocale(locale.LC_ALL, "")
		# row['certificado_monto_cobrar'] 	= locale.format_string("%.2f", obj.certificado_monto_cobrar, True)
		# row['certificado_monto_cobrar_uvi'] = locale.format_string("%.2f", obj.certificado_monto_cobrar_uvi, True)

		return
	
@login_required
def PaginaListaInstrumentosLegalesResoluciones(request):
	template_name = "Lista-resoluciones.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaListaInstrumentosLegalesResolucionesView(AjaxDatatableView):
	model = InstrumentosLegalesResoluciones
	title = "Instrumentos Legales(Resoluciones Presidencia)"
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
		{"name":"instrumentolegalresoluciones_descripcion", "className":"align-right", "max_length":200},
		{"name":"instrumentolegalresoluciones_document", "className":"align-right", "max_length":200, "orderable": False},
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
				
		if obj.instrumentolegalresoluciones_tipo == "P":
			editarlink = f'<a href="/viaticos/crearresolucionpresidencia/{id}">{editlinkimg}</a>'
		elif obj.instrumentolegalresoluciones_tipo == "D":
			editarlink = f'<a href="/viaticos/crearresoluciondirectorio/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/viaticos/crearresolucion/ver/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/resolucionpresidencia/{id}">{eliminarlinkimg}</a>'
		
		if self.request.user.has_perm("secretariador.delete_instrumentoslegalesresoluciones"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("secretariador.change_instrumentoslegalesresoluciones"):
			row["edit"] = f"{editarlink}{detallelink}"
		else:
			row["edit"] = f"{detallelink}"

		# # Conversion de numeros con separador de miles "." y decimales ",2"
		# locale.setlocale(locale.LC_ALL, "")
		# row['certificado_monto_cobrar'] 	= locale.format_string("%.2f", obj.certificado_monto_cobrar, True)
		# row['certificado_monto_cobrar_uvi'] = locale.format_string("%.2f", obj.certificado_monto_cobrar_uvi, True)

		return

@login_required
def PaginaListaInstrumentosLegalesResolucionesDirectorio(request):
	template_name = "Lista-resoluciones-directorio.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaListaInstrumentosLegalesResolucionesDirectorioView(AjaxDatatableView):
	model = InstrumentosLegalesResolucionesDirectorio
	title = "Instrumentos Legales(Resoluciones Directorio)"
	initial_order = [["instrumentolegalresolucionesdirectorio_ano", "desc"], ["instrumentolegalresolucionesdirectorio_numero", "desc"] ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":65},
		{"name": "id","title":"ID", "visible": False},
		{"name":"instrumentolegalresolucionesdirectorio_tipo", "className":"align-left"},
		{"name":"instrumentolegalresolucionesdirectorio_numero", "className":"align-left"},
		{"name":"instrumentolegalresolucionesdirectorio_acta", "className":"align-left"},
		{"name":"instrumentolegalresolucionesdirectorio_ano", "className":"align-left "},
		{"name":"instrumentolegalresolucionesdirectorio_fecha_aprobacion", "className":"align-left "},
		{"name":"instrumentolegalresolucionesdirectorio_descripcion", "className":"align-right", "max_length":200},
		{"name":"instrumentolegalresolucionesdirectorio_document", "className":"align-right", "max_length":200, "orderable": False},
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
				
		editarlink = f'<a href="/viaticos/crearresoluciondirectorio/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/viaticos/crearresoluciondirectorio/ver/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/resoluciondirectorio/{id}">{eliminarlinkimg}</a>'
		
		if self.request.user.has_perm("secretariador.delete_instrumentoslegalesresoluciones"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("secretariador.change_instrumentoslegalesresoluciones"):
			row["edit"] = f"{editarlink}{detallelink}"
		else:
			row["edit"] = f"{detallelink}"

		# # Conversion de numeros con separador de miles "." y decimales ",2"
		# locale.setlocale(locale.LC_ALL, "")
		# row['certificado_monto_cobrar'] 	= locale.format_string("%.2f", obj.certificado_monto_cobrar, True)
		# row['certificado_monto_cobrar_uvi'] = locale.format_string("%.2f", obj.certificado_monto_cobrar_uvi, True)

		return