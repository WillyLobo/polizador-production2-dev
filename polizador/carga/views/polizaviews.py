from ajax_datatable import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from carga.models import Poliza, Poliza_Movimiento, LegacyPoliza
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from carga.forms.polizaforms import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class EliminarPoliza(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.delete_poliza"

	model = Poliza
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-polizas")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearPoliza(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.add_poliza"

	model = Poliza
	template_name = "poliza/crear-poliza.html"
	form_class = PolizaForm
	success_url = reverse_lazy("carga:crear-poliza")

	title = "Crear Póliza"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.poliza_creador = self.request.user
		self.object.poliza_editor = self.request.user
		self.object.save()
		return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class UpdatePoliza(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.change_poliza"

	model = Poliza
	template_name = "poliza/update-poliza.html"
	form_class = PolizaForm
	success_url = reverse_lazy("carga:lista-polizas")

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.poliza_editor = self.request.user
		self.object.save()
		return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class CrearPolizaMovimiento(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.add_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "poliza/crear-movimiento-poliza.html"
	form_class = PolizaMovimientoForm

	title = "Crear Movimiento Póliza"

	def get_title(self):
		return self.title
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['poliza_id'] = self.request.session['poliza_id']
		context["title"] = self.get_title()
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.poliza_movimiento_editor = self.request.user
		self.object.save()
		return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class UpdatePolizaMovimiento(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.change_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "poliza/update-movimiento-poliza.html"
	form_class = PolizaMovimientoForm

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.poliza_movimiento_editor = self.request.user
		self.object.save()
		return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class EliminarPolizaMovimiento(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.delete_poliza_movimiento"

	model = Poliza_Movimiento
	template_name = "generic/confirm_delete.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

	
@method_decorator(login_required, name="dispatch")
class EstadoPoliza(generic.DetailView):
	login_url = "/"
	redirect_field_name = "login"
	model = Poliza
	template_name = "poliza/estado-poliza.html"

	# def get(self, request, *args, **kwargs):
	# 	poliza = request.session.get('poliza', 0)
	# 	request.session['num_visits'] = num_visits + 1
	# 	return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		self.object = self.get_object()
		poliza = models.Poliza.objects.get(id=self.object.id)
		poliza_id = str(poliza.id)
		self.request.session["poliza_id"] = poliza_id
		return context

@method_decorator(login_required, name="dispatch")
class ImprimirPolizaMovimiento(generic.DetailView):
	login_url = "/"
	redirect_field_name = "login"
	model = Poliza_Movimiento
	template_name = "poliza/imprimir-poliza.html"

@login_required
def PaginaListaPolizas(request):
	template_name = "Lista-polizas.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaPolizasView(AjaxDatatableView):
	model = Poliza
	title = "Pólizas"
	initial_order = [["id", "desc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":50},
		{"name": "id","title":"ID", "visible": True, "width":50, "searchable":False},
		{"name": "poliza_fecha"},
		{"name": "poliza_expediente"},
		{"name": "poliza_numero"},
		{"name": "poliza_concepto"},
		{"name": "poliza_recibo"},
		{"name": "poliza_aseguradora", "foreign_field":"poliza_aseguradora__aseguradora_nombre"},
		{"name": "poliza_tomador", "foreign_field":"poliza_tomador__empresa_nombre"},
		{"name": "poliza_obra", "title":"Obra", "foreign_field":"poliza_obra__obra_nombre"},
		{"name": "poliza_editor", "searchable":False, "orderable":False},
		]

	def customize_row(self, row, obj):
		id = str(obj.id)
		editarlink = f'<a href="/polizas/crear/poliza/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/polizas/crear/poliza/estado/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/polizas/eliminar/poliza/{id}">{eliminarlinkimg}</a>'
		if self.request.user.has_perm("carga.delete_poliza"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("carga.change_poliza"):
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

@method_decorator(login_required, name="dispatch")
class ImprimirLegacyPoliza(generic.DetailView):
	login_url = "/"
	redirect_field_name = "login"

	model 			= LegacyPoliza
	template_name 	= "poliza/legacy-imprimir-poliza.html"
	
@method_decorator(login_required, name="dispatch")
class UpdateLegacyPoliza(generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"

	model = LegacyPoliza
	template_name = "poliza/legacy-update-poliza.html"
	form_class = LegacyPolizaForm
	success_url = reverse_lazy("api:legacy_polizas")

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.legacy_poliza_editor = self.request.user
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())
	
@login_required
def PaginaListaLegacyPolizas(request):
	template_name = "Lista-legacypolizas.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaLegacyPolizasView(AjaxDatatableView):
	model = LegacyPoliza
	title = "Legacy Polizas"
	initial_order = [["id", "desc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{"name": "id","title":"ID", "visible": True, "width":50, "searchable":False},
		{"name": "legacy_poliza_fecha"},
		{"name": "legacy_poliza_expediente"},
		{"name": "legacy_poliza_numero"},
		{"name": "legacy_poliza_area", "foreign_field": "legacy_poliza_area__area_nombre"},
		{"name": "legacy_poliza_concepto"},
		{"name": "legacy_poliza_recibo"},
		{"name": "legacy_poliza_aseguradora", "foreign_field":"legacy_poliza_aseguradora__aseguradora_nombre"},
		{"name": "legacy_poliza_tomador", "foreign_field":"legacy_poliza_tomador__empresa_nombre"},
		{"name": "legacy_poliza_obra_nombre", "title":"Obra"},
		{"name": "legacy_poliza_editor", "searchable":False, "orderable":False},
		]

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