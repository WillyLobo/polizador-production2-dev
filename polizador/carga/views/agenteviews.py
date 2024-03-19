from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from carga.models import Agente
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from carga.forms.agenteforms import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class EliminarAgente(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.delete_agente"

	model = Agente
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-agentes")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context
	

@method_decorator(login_required, name="dispatch")
class CrearAgente(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.add_agente"

	model = Agente
	template_name = "agente/crear-agente.html"
	form_class = AgenteForm
	success_url = reverse_lazy("carga:crear-agente")
	
	title = "Crear Agente"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateAgente(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.change_agente"

	model = Agente
	template_name = "agente/update-agente.html"
	form_class = AgenteForm
	success_url = reverse_lazy("carga:lista-agentes")

@method_decorator(login_required, name="dispatch")
class AgenteObra(generic.DetailView):
	login_url = "/"
	redirect_field_name = "login"

	model = Agente
	template_name = "agente/agente-obra.html"

@login_required
def PaginaListaAgentes(request):
	template_name = "Lista-agentes.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class ListaAgentesView(AjaxDatatableView):
	model = Agente
	title = "Agentes"
	initial_order = [["id", "asc"], ]
	length_menu = [[50, 100, -1], [50, 100, "all"]]
	search_values_separator = "+"

	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{'name': 'edit', 'title': '', 'placeholder': True, 'searchable': False, 'orderable': False},
		{"name": "agente_nombre"},
		{"name": "agente_apellido"},
		{"name": "agente_dni"},
		# {"name": "agente_telefono"},
		# {"name": "agente_email"},
		{"name": "agente_profesion"},
		{"name": "agente_matricula"},
		{"name": "id","title":"ID", "visible": True},
		]

	def customize_row(self, row, obj):
		id = str(obj.id)
		editarlink = f'<a href="/polizas/crear/agente/{id}">{editlinkimg}</a>'
		detallelink = f'<a href="/polizas/crear/agente/obra/{id}">{detallelinkimg}</a>'
		eliminarlink = f'<a href="/polizas/eliminar/agente/{id}">{eliminarlinkimg}</a>'
		if self.request.user.has_perm("carga.delete_agente"):
			row["edit"] = f"{editarlink}{detallelink}{eliminarlink}"
		elif self.request.user.has_perm("carga.change_agente"):
			row["edit"] = f"{editarlink}{detallelink}"
		else:
			row["edit"] = f"{detallelink}"
		return
	