from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Aseguradora
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from carga.forms.aseguradoraforms import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class EliminarAseguradora(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.delete_aseguradora"

	model = Aseguradora
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-aseguradoras")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context


@method_decorator(login_required, name="dispatch")
class CrearAseguradora(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.add_aseguradora"

	model = Aseguradora
	template_name = "aseguradora/crear-aseguradora.html"
	form_class = AseguradoraForm
	success_url = reverse_lazy("carga:crear-aseguradora")

	title = "Crear Aseguradora"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateAseguradora(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.change_aseguradora"

	model = Aseguradora
	template_name = "aseguradora/update-aseguradora.html"
	form_class = AseguradoraForm
	success_url = reverse_lazy("carga:lista-aseguradoras")

@login_required
def PaginaListaAseguradoras(request):
	template_name = "Lista-aseguradoras.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaAseguradorasView(AjaxDatatableView):
	model = Aseguradora
	title = "Aseguradoras"
	initial_order = [["aseguradora_nombre", "asc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False, "width":81},
		{"name": "aseguradora_nombre", "className":"align-left", "title":"Aseguradora"},
		{"name": "id","title":"ID", "visible": False},
		]

	def customize_row(self, row, obj):
		id = str(obj.id)
		editarlink = f'<a href="/polizas/crear/aseguradora/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="#">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/polizas/eliminar/aseguradora/{id}">{eliminarlinkimg}</a>'
		if self.request.user.has_perm("carga.delete_aseguradora"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("carga.change_aseguradora"):
			row["edit"] = f"{editarlink}{detallelink}"
		else:
			# Armar template EstadoAseguradora!!
			row["edit"] = f"{detallelink}"
		return
	