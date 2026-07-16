from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from personalizador.models import Agente
from secretariador.forms.comisionadoform import ComisionadoForm
from core.mixins import DeleteRelatedObjectsMixin

@method_decorator(login_required, name="dispatch")
class CrearComisionado(PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_agente"

	model = Agente
	template_name = "comisionado/crear-comisionado.html"
	form_class = ComisionadoForm
	success_url = reverse_lazy("secretariador:crear-comisionado")

	title = "Crear Comisionado"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context

@method_decorator(login_required, name="dispatch")
class UpdateComisionado(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_agente"

	model = Agente
	template_name = "comisionado/update-comisionado.html"
	form_class = ComisionadoForm
	success_url = reverse_lazy("secretariador:crear-comisionado")

@method_decorator(login_required, name="dispatch")
class EliminarComisionado(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_agente"

	model = Agente
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-comisionados")

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

