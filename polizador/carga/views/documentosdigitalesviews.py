from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from carga.models import ContratosDigitales, ResolucionesDigitales
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from carga.forms.documentosdigitalesforms import *
from carga.views.generics import get_deleted_objects
import locale


@method_decorator(login_required, name="dispatch")
class CrearContratoDigital(PermissionRequiredMixin, generic.CreateView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "carga.add_certificado"

    model = ContratosDigitales
    template_name = "digitales/crear-contratodigital.html"
    form_class = ContratoDigitalForm
    success_url = reverse_lazy("carga:crear-contrato-digital")

    title = "Cargar Contrato Digital"

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contratodigital_creador = self.request.user
        self.object.contratodigital_editor = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UpdateContratoDigital(PermissionRequiredMixin, generic.UpdateView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "carga.change_certificado"

    model = ContratosDigitales
    template_name = "digitales/update-contratodigital.html"
    form_class = ContratoDigitalForm
    success_url = reverse_lazy("carga:crear-contrato-digital")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contratodigital_editor = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EliminarContratoDigital(PermissionRequiredMixin, generic.DeleteView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "carga.delete_certificado"

    model = ContratosDigitales
    template_name = "generic/confirm_delete.html"
    success_url = reverse_lazy("carga:lista-obras")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([
                                                                        self.object])
        context["deletable_objects"] = deletable_objects
        context["model_count"] = dict(model_count).items()
        context["protected"] = protected
        return context

@method_decorator(login_required, name="dispatch")
class CrearResolucionDigital(PermissionRequiredMixin, generic.CreateView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "carga.add_certificado"

    model = ResolucionesDigitales
    template_name = "digitales/crear-resoluciondigital.html"
    form_class = ResolucionDigitalForm
    success_url = reverse_lazy("carga:crear-resolucion-digital")

    title = "Cargar Resolución Digital"

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.resoluciondigital_creador = self.request.user
        self.object.resoluciondigital_editor = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UpdateResolucionDigital(PermissionRequiredMixin, generic.UpdateView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "carga.add_certificado"

    model = ResolucionesDigitales
    template_name = "digitales/update-resoluciondigital.html"
    form_class = ResolucionDigitalForm
    success_url = reverse_lazy("carga:crear-resolucion-digital")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.resoluciondigital_editor = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EliminarResolucionDigital(PermissionRequiredMixin, generic.DeleteView):
    login_url = "/"
    redirect_field_name = "login"
    permission_required = "carga.delete_certificado"

    model = ResolucionesDigitales
    template_name = "generic/confirm_delete.html"
    success_url = reverse_lazy("carga:lista-obras")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([
                                                                        self.object])
        context["deletable_objects"] = deletable_objects
        context["model_count"] = dict(model_count).items()
        context["protected"] = protected
        return context

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
# 		{"name": "certificado_financiamiento", "title":"Financ.", "searchable":False},
# 		{"name": "certificado_rubro_db", "title":"Rubro", "foreign_field":"certificado_rubro_db__certificadorubro_nombre", "searchable":False},
# 		{"name": "certificado_rubro_anticipo", "title":"Ant.", "searchable":False},
# 		{"name": "certificado_rubro_obra", "title":"Obra", "searchable":False},
# 		{"name": "certificado_rubro_devanticipo", "title":"D.Ant.", "searchable":False},
# 		{"name": "certificado_monto_cobrar", "title":"Monto $", "searchable":False},
# 		{"name": "certificado_monto_cobrar_uvi", "title":"Monto Uvi", "searchable":False},
# 		{"name": "certificado_mes_pct", "searchable":False},
# 	]

# 	def customize_row(self, row, obj):
# 		id = str(obj.id)
# 		obra = str(obj.certificado_obra.id)

# 		editarlink = f'<a href="/polizas/crear/certificado/{id}">{editlinkimg}</a>'
# 		detallelink = f'<a href="/polizas/crear/obra/estado/{obra}">{detallelinkimg}</a>'
# 		eliminarlink = f'<a href="/polizas/eliminar/certificado/{id}">{eliminarlinkimg}</a>'

# 		if self.request.user.has_perm("carga.delete_certificado"):
# 			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
# 		elif self.request.user.has_perm("carga.change_certificado"):
# 			row["edit"] = f"{editarlink}{detallelink}"
# 		else:
# 			row["edit"] = f"{detallelink}"

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
