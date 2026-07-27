from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from personalizador.models import Categoria
from personalizador.forms.categoriaforms import *
from core.mixins import DeleteRelatedObjectsMixin, PopupCreateMixin

@method_decorator(login_required, name="dispatch")
class EliminarCategoria(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "personalizador.delete_categoria"

	model = Categoria
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("personalizador:lista-categorias")


@method_decorator(login_required, name="dispatch")
class CrearCategoria(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "personalizador.add_categoria"

	model = Categoria
	template_name = "categoria/crear-categoria.html"
	form_class = CategoriaForm
	success_url = reverse_lazy("personalizador:crear-categoria")
	popup_form_partial = "partials/categoria-form-partial.html"

	title = "Crear Categoría"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context


@method_decorator(login_required, name="dispatch")
class UpdateCategoria(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "personalizador.change_categoria"

	model = Categoria
	template_name = "categoria/update-categoria.html"
	form_class = CategoriaForm
	success_url = reverse_lazy("personalizador:lista-categorias")

@login_required
@permission_required('personalizador.view_categoria', raise_exception=True)
def PaginaListaCategorias(request):
	template_name = "Lista-categorias.html"

	return render(request, template_name, {})
