from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from carga.models import Contrato
from carga.forms.contratoforms import *

@method_decorator(login_required, name="dispatch")
class CrearContrato(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.add_certificado"
	
	model = Contrato
	template_name = "contrato/crear-contrato.html"
	form_class = ContratoForm
	success_url = reverse_lazy("carga:crear-contrato")
	title = "Crear Contrato"

	def get_title(self):
		return self.title
	
	def get_context_data(self, **kwargs):
		context = super(CrearContrato, self).get_context_data(**kwargs)
		context["title"] = self.get_title()
		context["contratomonto_formset"] = ContratoFormset()
		return context
	
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		contratomonto_formset = ContratoFormset(self.request.POST)
		if form.is_valid() and contratomonto_formset.is_valid():
			return self.form_valid(form, contratomonto_formset)
		else:
			return self.form_invalid(form, contratomonto_formset)
	
	def form_valid(self, form, contratomonto_formset):
		self.object = form.save(commit=False)
		self.object.save()
		# Guardando Instancias
		contratomonto = contratomonto_formset.save(commit=False)
		for monto in contratomonto:
			monto.contratomonto_contrato = self.object
			monto.save()
		return redirect(reverse_lazy("carga:crear-contrato"))

	def form_invalid(self, form, contrato_formset):
		return self.render_to_response(self.get_context_data(form=form, contrato_formset=contrato_formset))

@method_decorator(login_required, name="dispatch")
class UpdateContrato(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.add_certificado"
	
	model = Contrato
	template_name = "contrato/update-contrato.html"
	form_class = ContratoForm
	success_url = reverse_lazy("carga:update-contrato")

	def get_context_data(self, **kwargs):
		context = super(UpdateContrato, self).get_context_data(**kwargs)

		context["contratomonto_formset"] = ContratoFormset(instance=self.object)
		return context
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		contratomonto_formset = ContratoFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, contratomonto_formset = contratomonto_formset))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		contratomonto_formset = ContratoFormset(self.request.POST, instance=self.object)
		if form.is_valid() and contratomonto_formset.is_valid():
			return self.form_valid(form, contratomonto_formset)
		else:
			return self.form_invalid(form, contratomonto_formset)
	
	def form_valid(self, form, contratomonto_formset):
		self.object = form.save(commit=False)
		self.object.save()
		# Guardando Instancias
		contratomonto = contratomonto_formset.save(commit=False)
		for monto in contratomonto:
			monto.contratomonto_contrato = self.object
			monto.save()
		return redirect(reverse_lazy("carga:crear-contrato"))

	def form_invalid(self, form, contrato_formset):
		return self.render_to_response(self.get_context_data(form=form, contrato_formset=contrato_formset))
	
# @method_decorator(login_required, name="dispatch")
# class UpdateCertificado(PermissionRequiredMixin, generic.UpdateView):
# 	login_url = "/"
# 	redirect_field_name = "login"
# 	permission_required = "carga.change_certificado"

# 	model = Certificado
# 	template_name = "certificado/update-certificado.html"
# 	form_class = CertificadoForm
# 	success_url = reverse_lazy("carga:lista-certificados")

# @method_decorator(login_required, name="dispatch")
# class CertificadoView(generic.DetailView):
# 	login_url = "/"
# 	redirect_field_name = "login"
# 	model = Certificado
# 	template_name = "certificado/certificado.html"

# @login_required
# def PaginaListaCertificados(request):
# 	template_name = "Lista-certificados.html"

# 	return render(request, template_name, {})

# @method_decorator(login_required, name="dispatch")
# class ListaCertificadosView(AjaxDatatableView):
# 	model = Certificado
# 	title = "Certificados"
# 	initial_order = [["id", "desc"], ]
# 	length_menu = [[50, 100, -1], [50, 100, "all"]]
# 	search_values_separator = "+"

# 	column_defs = [
# 		AjaxDatatableView.render_row_tools_column_def(),
# 		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":50},
# 		{"name": "id","title":"ID", "visible": True},
# 		{"name": "certificado_obra", "title":"Obra", "foreign_field":"certificado_obra__obra_nombre", "width":100},
# 		{"name": "certificado_empresa", "title":"Empresa", "foreign_field":"certificado_obra__obra_empresa__empresa_nombre","width":85},
# 		{"name": "certificado_expediente", "title":"Expediente", "width":95},
# 		{"name": "certificado_fecha"},
# 		{"name": "certificado_financiamiento", "title":"Financ."},
# 		{"name": "certificado_rubro_db", "title":"Rubro", "foreign_field":"certificado_rubro_db__certificadorubro_nombre"},
# 		{"name": "certificado_rubro_anticipo", "title":"Ant."},
# 		{"name": "certificado_rubro_obra", "title":"Obra"},
# 		{"name": "certificado_rubro_devanticipo", "title":"D.Ant."},
# 		{"name": "certificado_monto_cobrar", "title":"Monto $"},
# 		{"name": "certificado_monto_cobrar_uvi", "title":"Monto Uvi"},
# 		{"name": "certificado_mes_pct"},
# 	]

# 	def customize_row(self, row, obj):
# 		id = str(obj.id)
# 		obra = str(obj.certificado_obra.id)
# 		if self.request.user.has_perm("carga.change_certificado"):
# 			row["edit"] = '<a href="/polizas/crear/certificado/{id}"><img src="/static/edit.png" title="Editar" width="30" height="30" /></a> <a href="/polizas/crear/obra/estado/{obra}"><img src="/static/search.svg" title="Detalles" width="30" heigth="30" /></a>'.format(id=id, obra=obra)
# 		else:
# 			row["edit"] = '<a href="/polizas/crear/obra/estado/{obra}"><img src="/static/search.svg" title="Detalles" width="30" heigth="30" /></a>'.format(id=id, obra=obra)

# 		# Conversion de numeros con separador de miles "." y decimales ",2"
# 		locale.setlocale(locale.LC_ALL, "")
# 		row['certificado_monto_cobrar'] 	= locale.format_string("%.2f", obj.certificado_monto_cobrar, True)
# 		row['certificado_monto_cobrar_uvi'] = locale.format_string("%.2f", obj.certificado_monto_cobrar_uvi, True)

# 		return
	
# 	def render_row_details(self, pk, request=None):

#         # we do some optimization on the request
# 		relateds = []
# 		if not self.disable_queryset_optimization_only and not self.disable_queryset_optimization_select_related:
# 			relateds = [f.name for f in self.model._meta.get_fields() if f.many_to_one and f.concrete]

# 		prefetchs = []
# 		if not self.disable_queryset_optimization_only and not self.disable_queryset_optimization_prefetch_related:
# 			prefetchs = [f.name for f in self.model._meta.get_fields() if f.many_to_many and f.concrete]

# 		obj = self.model.objects.filter(pk=pk).select_related(*relateds).prefetch_related(*prefetchs).first()

# 		# Extract "extra_data" from request
# 		extra_data = {k: v for k, v in request.GET.items() if k not in ['action', 'pk', ]}

# 		# Search a custom template for rendering, if available
# 		try:
# 			template = loader.get_template(
#                 'ajax_datatable/%s/%s/%s' % (self.model._meta.app_label,
#                                              self.model._meta.model_name, self.render_row_details_template_name),
#             )

# 			html = template.render({
# 				'model': self.model,
# 				'model_admin': self.get_model_admin(),
# 				'object': obj,
# 				'extra_data': extra_data,
# 				}, request)

# 		# Failing that, display a simple table with field values
# 		except TemplateDoesNotExist:
# 			fields = [f.name for f in self.model._meta.get_fields() if f.concrete]
# 			html = '<table class="row-details">'
# 			for field in fields:
				
# 				if field in prefetchs:
# 					value = ', '.join([str(x) for x in eval(f'obj.{field}').all()])
# 				else:
# 					try:
# 						value = getattr(obj, field)
# 					except AttributeError:
# 						continue
# 				html += '<tr><td>%s</td><td>%s</td></tr>' % (field, value)
# 			html += '</table>'
# 		return html