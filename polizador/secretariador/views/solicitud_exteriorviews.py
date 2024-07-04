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
	jinja_env = jinja2.Environment()
	jinja_env.trim_blocks = True
	jinja_env.lstrip_blocks = True

	actuacion = Solicitud.objects.get(pk=pk)
	agentes = actuacion.comisionadosolicitud_set.all().order_by("comisionadosolicitud_chofer")
	tareas = actuacion.solicitud_tareas
	fechas = actuacion.solicitud_fechas()
	vehiculo = actuacion.solicitud_vehiculo
	decreto_viaticos = actuacion.solicitud_decreto_viaticos.montoviaticodiario_decreto_reglamentario
	
	def generate_agente_list(agentes):
		lista_agentes = []
		final_text = {}
		for index, agente in enumerate(agentes):
			chofer = ""
			colaborador = ""

			if index == len(agentes)-1 and len(agentes) > 1:
				if agente.comisionadosolicitud_nombre.comisionado_sexo == "M":
					text = "y el"
				else:
					text = "y la"
			else:
				if agente.comisionadosolicitud_nombre.comisionado_sexo == "M":
					text = "el"
				else:
					text = "la"
				if agente.comisionadosolicitud_colaborador:
					colaborador = ", en carácter de colaborador"
				else:
					colaborador = ""
			
			if agente.comisionadosolicitud_chofer:
				if agente.comisionadosolicitud_nombre.comisionado_sexo == "M":
					chofer = f"el {agente.comisionadosolicitud_nombre.comisionado_abreviatura} {agente.comisionadosolicitud_nombre.comisionado_nombreyapellido}"
				else:
					chofer = f"la {agente.comisionadosolicitud_nombre.comisionado_abreviatura} {agente.comisionadosolicitud_nombre.comisionado_nombreyapellido}"

			if len(agentes) > 1:
				traslado = "trasladar a los mencionados agentes"
			else:
				traslado = "trasladar al mencionado agente"
			
			dni = "{:,}".format(agente.comisionadosolicitud_nombre.comisionado_dni).replace(",", "@").replace(".", ",").replace("@", ".")
			lista_agentes.append(f"{text} {agente.comisionadosolicitud_nombre.comisionado_abreviatura} {agente.comisionadosolicitud_nombre.comisionado_nombreyapellido} - D.N.I.Nº{dni}{colaborador}")

		final_text.update({
			"lista_agentes": f"{', '.join(agente for agente in lista_agentes)}",
			"traslado":traslado,
			"chofer":chofer,
		})
		return final_text

		lista_localidades = []
		final_text = ""
		if len(localidades) > 1:
			text_localidad = "las localidades de"
		else:
			text_localidad = "la localidad de"
		for index, localidad in enumerate(localidades):
			if index == len(localidades)-1 and len(localidades) > 1:
				lista_localidades.append(f"y {localidad}")
			else:
				lista_localidades.append(f"{localidad}")
		final_text = f"{text_localidad} {', '.join(localidad for localidad in lista_localidades)}"
		return final_text

	def generate_fechas_list(fechas):
		lista_fechas = []
		final_text = ""
		if len(fechas) > 1:
			text_fechas = "los días"
		else:
			text_fechas = "el día"
		for index, fecha in enumerate(fechas):
			if index == len(fechas)-1 and len(fechas) > 1:
				lista_fechas.append(f"y {fecha}")
			else:
				lista_fechas.append(f"{fecha}")
		final_text = f"{text_fechas} {', '.join(fecha for fecha in lista_fechas)}"
		return final_text

	def generate_agente_list_articulo(agentes):
		colaborador = ""
		
		final_text = []
		for agente in agentes:
			lista_agentes = []
			agente_cuit = f"{agente.comisionadosolicitud_nombre.comisionado_abreviatura} {agente.comisionadosolicitud_nombre.comisionado_nombreyapellido} – CUIL Nº{agente.comisionadosolicitud_nombre.comisionado_cuit}"
			cantidad_de_dias = f"{actuacion.solicitud_cantidad_de_dias.days} {' dias' if actuacion.solicitud_cantidad_de_dias.days > 1 else 'dia'}"
			comisionadosolicitud_combustible = "{:,.2f}".format(agente.comisionadosolicitud_combustible).replace(",", "@").replace(".", ",").replace("@", ".")
			comisionadosolicitud_pasaje = "{:,.2f}".format(agente.comisionadosolicitud_pasaje).replace(",", "@").replace(".", ",").replace("@", ".")
			comisionadosolicitud_gastos = "{:,.2f}".format(agente.comisionadosolicitud_gastos).replace(",", "@").replace(".", ",").replace("@", ".")
			valor_viatico_dia = "{:,.2f}".format(agente.valor_viatico_dia()).replace(",", "@").replace(".", ",").replace("@", ".")
			valor_viatico_total = "{:,.2f}".format(agente.viaticos_total()).replace(",", "@").replace(".", ",").replace("@", ".")

			subparrafo = f"(Viáticos: {cantidad_de_dias} a razón de ${valor_viatico_dia} diarios"
			if comisionadosolicitud_pasaje != "0,00":
				subparrafo += f" + Pasaje: ${comisionadosolicitud_pasaje}"
			elif comisionadosolicitud_gastos != "0,00":
				subparrafo += f" + Gastos: ${comisionadosolicitud_gastos}"
			elif comisionadosolicitud_combustible != "0,00":
				subparrafo += f" + Combustible: ${comisionadosolicitud_combustible}"
			subparrafo += f")."

			lista_agentes.append(agente_cuit)
			lista_agentes.append(valor_viatico_total)	
			lista_agentes.append(subparrafo)
			final_text.append(lista_agentes)
		return final_text

	lista_agentes       = generate_agente_list(agentes)
	lista_fechas        = generate_fechas_list(fechas)
	lista_agentes_articulo = generate_agente_list_articulo(agentes)

	parrafo_uno     = f"Que por la misma se tramita autorización y anticipo de viáticos para {lista_agentes['lista_agentes']} de este Organismo, quienes se trasladaran a la provincia de {actuacion.solicitud_provincia} {lista_fechas}, con motivo de {tareas} en la ciudad de {actuacion.solicitud_ciudad};"
	if actuacion.solicitud_aereo:
		parrafo_dos     = f"Que, en la comisión de referencia el traslado se realizará de forma aérea;"
	else:
		parrafo_dos_1  = f"Que el vehículo afectado será {vehiculo.vehiculo_modelo} – Dominio {vehiculo.vehiculo_patente}"
		parrafo_dos_2  = f", asegurado bajo póliza Nº{ vehiculo.vehiculo_poliza} emitida por {vehiculo.vehiculo_poliza_aseguradora}," if vehiculo.vehiculo_poliza else ""
		parrafo_dos_3  = f" conducido por {lista_agentes['chofer']};"
		parrafo_dos    = parrafo_dos_1+parrafo_dos_2+parrafo_dos_3
	parrafo_tres	= f"Que, en consecuencia, deben anticiparse los fondos necesarios para hacer frente a los gastos a realizar, de acuerdo a lo dispuesto en los Decretos Nº1324/1978 y Nº{decreto_viaticos.instrumentolegaldecretos_numero}/{decreto_viaticos.instrumentolegaldecretos_ano});"
	parrafo_cuatro	= f"Que el trámite se encuadra dentro de lo establecido en el Decreto Nº 1324/78 – “Régimen de Viáticos”; y que debido a la fecha a realizarse, incluye días inhábiles deben encuadrarse dentro de las excepciones en el Inciso A; IV Decreto Nº211/20;"

	articulo_uno    = f"Autorizar a los agentes, detallados a continuación, a trasladarse a la ciudad de {actuacion.solicitud_ciudad}, provincia de {actuacion.solicitud_provincia}, con motivo de {tareas}, {lista_fechas} y anticipar los importes que se consignan, conforme con el Visto y Considerando de la presente, debiendo rendir cuentas documentadas de sus inversiones, de acuerdo con las reglamentaciones vigentes."
	articulo_dos    = lista_agentes_articulo

	if actuacion.solicitud_provincia.provincia_nombre == "Chaco":
		doc = DocxTemplate("secretariador/media/solicitud_template.docx")
		context = {
			"actuacion":actuacion,
			"parrafo_uno":parrafo_uno,
			"parrafo_dos":parrafo_dos,
			"parrafo_tres":parrafo_tres,
			"parrafo_cuatro":parrafo_cuatro,
			"articulo_uno":articulo_uno,
			"articulo_dos":articulo_dos,
		}
	else:
		doc = DocxTemplate("secretariador/media/solicitud_exterior.docx")
		context = {
			"actuacion":actuacion,
			"parrafo_uno":parrafo_uno,
			"parrafo_dos":parrafo_dos,
			"parrafo_tres":parrafo_tres,
			"parrafo_cuatro":parrafo_cuatro,
			"articulo_uno":articulo_uno,
			"articulo_dos":articulo_dos,
		}

	filename = actuacion.solicitud_actuacion+".docx"
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
