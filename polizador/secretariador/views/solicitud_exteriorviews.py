import io

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import EncabezadoDocumento, Solicitud, InstrumentosLegalesDecretos
from carga.models import Provincia
from secretariador.forms.solicitud_exteriorform import *
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg, generarlinkimg
from core.mixins import DeleteRelatedObjectsMixin
from secretariador import docx_texto
from secretariador.docx_texto import separate_items
from secretariador.docx_builder import build_resolucion_docx
from secretariador.views.textoactuacionviews import revisar_texto_actuacion


def _calcular_texto_exterior(actuacion):
	"""Igual que `solicitudviews._calcular_texto_solicitud` pero con la
	redacción usada para actuaciones de otras provincias (exterior)."""
	agentes = actuacion.comisionadosolicitud_set.all().order_by("comisionadosolicitud_chofer")
	tareas = actuacion.solicitud_tareas
	fechas = actuacion.solicitud_fechas()
	if actuacion.solicitud_vehiculo:
		vehiculo_modelo = actuacion.solicitud_vehiculo.vehiculo_modelo
		vehiculo_patente = actuacion.solicitud_vehiculo.vehiculo_patente
		vehiculo_poliza = actuacion.solicitud_vehiculo.vehiculo_poliza
		vehiculo_poliza_aseguradora = actuacion.solicitud_vehiculo.vehiculo_poliza_aseguradora
	else:
		vehiculo_modelo = "FALTA DESIGNAR VEHICULO!!"
		vehiculo_patente = "FALTA DESIGNAR VEHICULO!!"
		vehiculo_poliza = "FALTA DESIGNAR VEHICULO!!"
		vehiculo_poliza_aseguradora = "FALTA DESIGNAR VEHICULO!!"
	decreto_viaticos = actuacion.solicitud_decreto_viaticos.montoviaticodiario_decreto_reglamentario

	def generate_agente_list(agentes):
		lista_agentes = []
		final_text = {}
		for agente in agentes:
			chofer = ""
			colaborador = ""
			agente_denominacion = f"{agente.persona.abreviatura} {agente.persona.agente_nombres} {agente.persona.agente_apellidos}"
			if agente.persona.sexo.generoagente_nombre == "Masculino":
				text = "el"
			else:
				text = "la"

			if agente.comisionadosolicitud_colaborador:
				colaborador = " en carácter de colaborador"
			else:
				colaborador = ""

			if agente.comisionadosolicitud_chofer:
				if agente.persona.sexo.generoagente_nombre == "Masculino":
					chofer = f"el {agente_denominacion}"
				else:
					chofer = f"la {agente_denominacion}"

			if len(agentes) > 1:
				traslado = "trasladar a los mencionados agentes"
				traslado_parrafo_uno = "quienes se trasladarán"
				plural_agente_articulo_uno = "a los agentes, detallados"
			else:
				traslado = "trasladar al mencionado agente"
				traslado_parrafo_uno = "quien se trasladará"
				plural_agente_articulo_uno = "al agente, detallado"

			dni = "{:,}".format(agente.persona.dni).replace(",", "@").replace(".", ",").replace("@", ".")
			lista_agentes.append(f"{text} {agente_denominacion} - D.N.I.Nº{dni}{colaborador}")
		lista_agentes = separate_items(lista_agentes)

		final_text.update({
			"lista_agentes": lista_agentes,
			"traslado":traslado,
			"chofer":chofer,
			"traslado_parrafo_uno": traslado_parrafo_uno,
			"plural_agente_articulo_uno": plural_agente_articulo_uno
		})
		return final_text

	lista_agentes       = generate_agente_list(agentes)
	lista_fechas        = docx_texto.generate_fechas_list(fechas)
	articulo_dos        = docx_texto.generate_agente_list_articulo(agentes, actuacion.solicitud_cantidad_de_dias.days)

	parrafo_uno     = f"Que por la misma se tramita autorización y anticipo de viáticos para {lista_agentes['lista_agentes']} de este Organismo, {lista_agentes['traslado_parrafo_uno']} a la provincia de {actuacion.solicitud_provincia} {lista_fechas}, con motivo de {tareas} en la ciudad de {actuacion.solicitud_ciudad};"
	if actuacion.solicitud_aereo:
		parrafo_dos     = f"Que, en la comisión de referencia el traslado se realizará de forma aérea;"
	else:
		parrafo_dos_1  = f"Que el vehículo afectado será {vehiculo_modelo} – Dominio {vehiculo_patente}"
		parrafo_dos_2  = f", asegurado bajo póliza Nº{ vehiculo_poliza} emitida por {vehiculo_poliza_aseguradora}," if vehiculo_poliza else ""
		parrafo_dos_3  = f" conducido por {lista_agentes['chofer']};"
		parrafo_dos    = parrafo_dos_1+parrafo_dos_2+parrafo_dos_3
	parrafo_tres	= f"Que, en consecuencia, deben anticiparse los fondos necesarios para hacer frente a los gastos a realizar, de acuerdo a lo dispuesto en los Decretos Nº1324/1978 y Nº{decreto_viaticos.instrumentolegaldecretos_numero}/{decreto_viaticos.instrumentolegaldecretos_ano};"
	parrafo_cuatro	= f"Que el trámite se encuadra dentro de lo establecido en el Decreto Nº 1324/78 – “Régimen de Viáticos”; y que debido a la fecha a realizarse, incluye días inhábiles deben encuadrarse dentro de las excepciones en el Inciso A; IV Decreto Nº211/20;"

	articulo_uno = f"Autorizar {lista_agentes['plural_agente_articulo_uno']} a continuación, a trasladarse a la ciudad de {actuacion.solicitud_ciudad}, provincia de {actuacion.solicitud_provincia}, con motivo de {tareas}, {lista_fechas} y anticipar los importes que se consignan, conforme con el Visto y Considerando de la presente, debiendo rendir cuentas documentadas de sus inversiones, de acuerdo con las reglamentaciones vigentes."

	visto_texto = f"La Actuación Electrónica Nº{actuacion.solicitud_actuacion}; y "
	parrafos = [parrafo_uno, parrafo_dos, parrafo_tres, parrafo_cuatro]
	return visto_texto, parrafos, articulo_uno, articulo_dos


def _generar_exterior_docx(actuacion):
	texto = actuacion.solicitud_texto_actuacion
	if texto:
		visto_texto, _parrafos_default, _articulo_uno_default, _articulo_dos_default = _calcular_texto_exterior(actuacion)
		parrafos = texto["parrafos"]
		articulo_uno = texto["articulo_uno"]
		articulo_dos_filas = texto["articulo_dos"]
	else:
		visto_texto, parrafos, articulo_uno, articulo_dos_filas = _calcular_texto_exterior(actuacion)

	encabezado = EncabezadoDocumento.vigente()
	with encabezado.encabezadodocumento_archivo.open("rb") as f:
		base_docx = io.BytesIO(f.read())

	return build_resolucion_docx(
		base_docx,
		visto_texto=visto_texto,
		parrafos=parrafos,
		incluir_ultimo_parrafo=actuacion.solicitud_dia_inhabil,
		articulo_uno=articulo_uno,
		articulo_dos_filas=articulo_dos_filas,
		articulo_tres=docx_texto.ARTICULO_TRES,
		articulo_cuatro=docx_texto.ARTICULO_CUATRO,
		articulo_cinco=docx_texto.ARTICULO_CINCO,
		considerandos_fijos_finales=docx_texto.CONSIDERANDOS_FIJOS_FINALES,
	)


@login_required
@permission_required("secretariador.change_solicitud", raise_exception=True)
def editar_texto_solicitud_exterior(request, pk):
	actuacion = Solicitud.objects.get(pk=pk)
	_visto_texto, parrafos_default, articulo_uno_default, articulo_dos_default = _calcular_texto_exterior(actuacion)
	return revisar_texto_actuacion(
		request,
		actuacion=actuacion,
		texto_field_name="solicitud_texto_actuacion",
		generar_docx_url_name="secretariador:crear-documento-solicitud-exterior",
		parrafos_default=parrafos_default,
		articulo_uno_default=articulo_uno_default,
		articulo_dos_default=articulo_dos_default,
		extra_context={"dia_inhabil": actuacion.solicitud_dia_inhabil},
	)


@login_required
@permission_required("secretariador.view_solicitud", raise_exception=True)
def exterior_docx(request, pk):
	actuacion = Solicitud.objects.get(pk=pk)
	out = _generar_exterior_docx(actuacion)

	filename = actuacion.solicitud_actuacion+".docx"
	response = HttpResponse(out.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
	response["Content-Disposition"] = f'filename="{filename}"'
	return response

@method_decorator(login_required, name="dispatch")
class CrearSolicitudExterior(PermissionRequiredMixin, generic.CreateView):
	permission_required = "secretariador.add_solicitud"

	model = Solicitud
	template_name = "solicitudexterior/crear-solicitud-exterior.html"
	form_class = SolicitudExteriorForm
	success_url = reverse_lazy("secretariador:crear-solicitud-exterior")
	
	title = "Crear Solicitud Exterior"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super(CrearSolicitudExterior, self).get_context_data(**kwargs)

		if self.request.POST:
			context['group_formset'] = ComisionadoSolicitudExteriorFormset(self.request.POST, instance=self.object)
			# por que esta vergación tiene que estar acá para que los errores del formset se muestren correctamente?
			context.get('group_formset').errors
		else:
			context['group_formset'] = ComisionadoSolicitudExteriorFormset(instance=self.object)
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
	permission_required = "secretariador.change_solicitud"

	model = Solicitud
	template_name = "solicitudexterior/update-solicitud-exterior.html"
	form_class = SolicitudExteriorForm
	success_url = reverse_lazy("secretariador:lista-solicitudes")
	
	def get_context_data(self, **kwargs):
		context = super(type(self), self).get_context_data(**kwargs)
		if self.request.POST:
			context['group_formset'] = ComisionadoSolicitudExteriorFormset(self.request.POST, instance=self.object)
			# por que esta vergación tiene que estar acá para que los errores del formset se muestren correctamente?
			context.get('group_formset').errors
		else:
			context['group_formset'] = ComisionadoSolicitudExteriorFormset(instance=self.object)

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
class EliminarSolicitudExterior(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "secretariador.delete_solicitud"

	model = Solicitud
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-solicitudes")