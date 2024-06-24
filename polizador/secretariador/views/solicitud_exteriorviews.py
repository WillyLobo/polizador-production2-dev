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
from secretariador.forms.solicitud_exteriorform import *
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg, generarlinkimg
from carga.views.generics import get_deleted_objects
import jinja2


from docxtpl import DocxTemplate

def exterior_docx(request, pk):
	solicitud = Solicitud.objects.get(pk=pk)

	jinja_env = jinja2.Environment()
	jinja_env.trim_blocks = True
	jinja_env.lstrip_blocks = True
	# if solicitud.solicitud_solicitante.comisionado_cargo.organigrama_cargo == "":
	if solicitud.solicitud_provincia.provincia_nombre == "Chaco":
		doc = DocxTemplate("secretariador/media/solicitud_template.docx")
		context = {
		"solicitud":solicitud,
		"actuacion":solicitud.solicitud_actuacion,
		"agentes":solicitud.comisionadosolicitud_set.all(),
		"solicitante_cargo":solicitud.solicitud_solicitante.comisionado_cargo.organigrama_cargo,
		"localidades":solicitud.solicitud_localidades.all(),
		"fechas":solicitud.solicitud_fechas(),
		"tareas":solicitud.solicitud_tareas,
		"vehiculo":solicitud.solicitud_vehiculo,
		"vehiculo_modelo":solicitud.solicitud_vehiculo.vehiculo_modelo,
		"vehiculo_patente":solicitud.solicitud_vehiculo.vehiculo_patente,
		"decreto_viaticos":solicitud.solicitud_decreto_viaticos.montoviaticodiario_decreto_reglamentario,
		}
	else:
		doc = DocxTemplate("secretariador/media/solicitud_exterior.docx")
		context = {
		"solicitud":solicitud,
		"actuacion":solicitud.solicitud_actuacion,
		"solicitante_cargo":solicitud.solicitud_solicitante.comisionado_cargo.organigrama_cargo,
		"agentes":solicitud.comisionadosolicitud_set.all(),
		"fechas":solicitud.solicitud_fechas(),
		"tareas":solicitud.solicitud_tareas,
		"ciudad":solicitud.solicitud_ciudad,
		"decreto_viaticos":solicitud.solicitud_decreto_viaticos.montoviaticodiario_decreto_reglamentario,
		
		}

	filename = solicitud.solicitud_actuacion+".docx"
	response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
	response["Content-Disposition"] = f'filename="{filename}"'

	doc.render(context)
	doc.save(response)

	return response

@method_decorator(login_required, name="dispatch")
class CrearSolicitudExterior(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_solicitud"

	model = Solicitud
	template_name = "solicitudexterior/crear-solicitud-exterior.html"
	form_class = SolicitudExteriorForm
	initial={
		"solicitud_provincia":Provincia.objects.all().filter(provincia_nombre__icontains="Chaco").last(),
		"solicitud_decreto_viaticos":InstrumentosLegalesDecretos.objects.filter(instrumentolegaldecretos_tipo="P").filter(instrumentolegaldecretos_descripcion__icontains="Viáticos").latest()
		}
	success_url = reverse_lazy("secretariador:crear-solicitud-exterior")
	
	title = "Crear Solicitud Exterior"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super(CrearSolicitudExterior, self).get_context_data(**kwargs)

		context["comisionadosformset"] = ComisionadoSolicitudExteriorFormset(instance=self.object)
		return context

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoSolicitudExteriorFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset = comisionadosformset))
	
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoSolicitudExteriorFormset(self.request.POST, instance=self.object)
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
class UpdateSolicitudExterior(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_solicitud"

	model = Solicitud
	template_name = "solicitudexterior/update-solicitud-exterior.html"
	form_class = SolicitudExteriorForm
	success_url = reverse_lazy("secretariador:lista-solicitudes")
	
	def get_context_data(self, **kwargs):
		context = super(UpdateSolicitudExterior, self).get_context_data(**kwargs)

		context["comisionadosformset"] = ComisionadoSolicitudExteriorFormset(instance=self.object)
		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoSolicitudExteriorFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset = comisionadosformset))
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoSolicitudExteriorFormset(self.request.POST, instance=self.object)
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
class EliminarSolicitudExterior(PermissionRequiredMixin, generic.DeleteView):
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
	
# @method_decorator(login_required, name="dispatch")
# class VerSolicitud(generic.DetailView):
# 	login_url = "/"
# 	redirect_field_name = "login"
# 	model = Solicitud
# 	template_name = "solicitud/ver-solicitud.html"
