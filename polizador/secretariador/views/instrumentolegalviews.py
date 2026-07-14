from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import InstrumentosLegalesMemorandum, InstrumentosLegalesDecretos, InstrumentosLegalesResoluciones
from secretariador.forms.instrumentoslegalesform import *
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class CrearInstrumentoLegalMemorandum(PermissionRequiredMixin, generic.CreateView):
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
	permission_required = "secretariador.add_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "instrumentoslegales/crear-instrumento-legal-resolucion-directorio.html"
	form_class = InstrumentosLegalesResolucionesDirectorioForm
	success_url = reverse_lazy("secretariador:crear-resolucion-directorio")
	
	title = "Crear Resolución(Directorio)"

	def get_title(self):
		return self.title

@method_decorator(login_required, name="dispatch")
class UpdateInstrumentoLegalMemorandum(PermissionRequiredMixin, generic.UpdateView):
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
	
@method_decorator(login_required, name="dispatch")
class UpdateInstrumentoLegalResolucionDirectorio(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "secretariador.change_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "instrumentoslegales/update-instrumento-legal-resolucion-directorio.html"
	form_class = InstrumentosLegalesResolucionesDirectorioForm
	success_url = reverse_lazy("secretariador:lista-resoluciones")

	def get_context_data(self,*args, **kwargs):
		context = super(type(self), self).get_context_data(*args,**kwargs)
		objetoanterior = self.model.objects.filter(pk=self.object.id - 1)
		objetosiguiente = self.model.objects.filter(pk=self.object.id + 1)
		
		context['idanteriorobjeto'] = objetoanterior.first() if objetoanterior.exists() else None
		context['idsiguienteobjeto'] = objetosiguiente.first() if objetosiguiente.exists() else None
		
		return context

@method_decorator(login_required, name="dispatch")
class EliminarInstrumentoLegalMemorandum(PermissionRequiredMixin, generic.DeleteView):
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
	permission_required = "secretariador.delete_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-resoluciones")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

@method_decorator(login_required, name="dispatch")
class EliminarInstrumentoLegalResolucionDirectorio(PermissionRequiredMixin, generic.DeleteView):
	permission_required = "secretariador.delete_instrumentoslegalesresoluciones"

	model = InstrumentosLegalesResoluciones
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-resoluciones")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context

@login_required
@permission_required("secretariador.view_instrumentoslegalesmemorandum", raise_exception=True)
def PaginaListaInstrumentosLegalesMemorandum(request):
	template_name = "Lista-memorandum.html"

	return render(request, template_name, {})

@login_required
@permission_required("secretariador.view_instrumentoslegalesdecretos", raise_exception=True)
def PaginaListaInstrumentosLegalesDecretos(request):
	template_name = "Lista-decretos.html"

	return render(request, template_name, {})

@login_required
@permission_required("secretariador.view_instrumentoslegalesresoluciones", raise_exception=True)
def PaginaListaInstrumentosLegalesResoluciones(request):
	template_name = "Lista-resoluciones.html"

	return render(request, template_name, {})
