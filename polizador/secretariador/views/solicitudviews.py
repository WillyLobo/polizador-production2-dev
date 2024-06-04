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
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg, generarlinkimg
from carga.views.generics import get_deleted_objects
import jinja2


from docxtpl import DocxTemplate

def render_docx(request, pk):
	jinja_env = jinja2.Environment()
	jinja_env.trim_blocks = True
	jinja_env.lstrip_blocks = True
	doc = DocxTemplate("secretariador/media/solicitud_template.docx")
	solicitud = Solicitud.objects.get(pk=pk)
	context = {
	"solicitud":solicitud,
	"actuacion":solicitud.solicitud_actuacion,
	"agentes":solicitud.comisionadosolicitud_set.all(),
	"localidades":solicitud.solicitud_localidades.all(),
	"fechas":solicitud.solicitud_fechas(),
	"tareas":solicitud.solicitud_tareas,
	"vehiculo":solicitud.solicitud_vehiculo,
	"vehiculo_modelo":solicitud.solicitud_vehiculo.vehiculo_modelo,
	"vehiculo_patente":solicitud.solicitud_vehiculo.vehiculo_patente,
	"decreto_viaticos":solicitud.solicitud_decreto_viaticos.montoviaticodiario_decreto_reglamentario,
	}

	filename = solicitud.solicitud_actuacion+".docx"
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
	initial_order = [["solicitud_actuacion", "desc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":81},
		{"name": "id","title":"ID", "visible": False},
		{"name":"solicitud_actuacion"},
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
				
		editarlink = f'<a href="/viaticos/crearsolicitud/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/viaticos/crearsolicitud/ver/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/viaticos/eliminar/solicitud/{id}">{eliminarlinkimg}</a>'
		generarlink = f'<a href="/viaticos/creardocumento/{id}">{generarlinkimg}</a>'
		
		if self.request.user.has_perm("secretariador.delete_solicitud"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}{generarlink}"
		elif self.request.user.has_perm("secretariador.change_solicitud"):
			row["edit"] = f"{editarlink}{detallelink}{generarlink}"
		else:
			row["edit"] = f"{detallelink}"

		# Get list of comisionados for this solicitud, joining them wih ";" for display
		if obj.get_comisionados():
			row["Comisionados"] = "; ".join(c for c in obj.get_comisionados())

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