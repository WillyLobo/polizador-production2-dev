from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from personalizador.models import ComisionadoExterno
from secretariador.forms.comisionadoform import ComisionadoExternoForm
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

# @method_decorator(login_required, name="dispatch")
# class CertificadoView(generic.DetailView):
# 	login_url = "/"
# 	redirect_field_name = "login"
# 	model = Certificado
# 	template_name = "certificado/certificado.html"

@login_required
@permission_required("personalizador.view_agente", raise_exception=True)
def PaginaListaComisionados(request):
	template_name = "Lista-comisionados.html"

	return render(request, template_name, {})

@method_decorator(login_required, name="dispatch")
class CrearComisionadoExterno(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_comisionadoexterno"

	model = ComisionadoExterno
	template_name = "comisionado/crear-comisionado-externo.html"
	form_class = ComisionadoExternoForm
	success_url = reverse_lazy("secretariador:crear-comisionado-externo")
	popup_form_partial = "partials/comisionados-externo-form-partial.html"

	title = "Crear Comisionado Externo"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

@method_decorator(login_required, name="dispatch")
class UpdateComisionadoExterno(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_comisionadoexterno"

	model = ComisionadoExterno
	template_name = "comisionado/update-comisionado-externo.html"
	form_class = ComisionadoExternoForm
	success_url = reverse_lazy("secretariador:crear-comisionado-externo")

@method_decorator(login_required, name="dispatch")
class EliminarComisionadoExterno(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_comisionadoexterno"

	model = ComisionadoExterno
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-comisionados-externos")

@login_required
@permission_required("personalizador.view_comisionadoexterno", raise_exception=True)
def PaginaListaComisionadosExternos(request):
	template_name = "Lista-comisionados-externos.html"

	return render(request, template_name, {})

