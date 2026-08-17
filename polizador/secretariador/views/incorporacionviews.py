import io

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import EncabezadoDocumento, Incorporacion, InstrumentosLegalesDecretos
from carga.models import Provincia
from secretariador.forms.incorporacionform import *
from core.mixins import DeleteRelatedObjectsMixin
from secretariador import docx_texto
from secretariador.docx_texto import separate_items
from secretariador.docx_builder import build_resolucion_docx
from secretariador.views.textoactuacionviews import revisar_texto_actuacion


def _calcular_texto_incorporacion(actuacion):
	"""Igual que en `solicitudviews`/`solicitud_exteriorviews` pero para la
	incorporación de agentes a una Solicitud ya resuelta."""
	numero_actuacion = actuacion.incorporacion_actuacion
	resolucion_solicitud = actuacion.incorporacion_solicitud.solicitud_resolucion
	agentes_incorporacion = actuacion.comisionadosolicitud_set.all().order_by("comisionadosolicitud_chofer")
	agentes_solicitud = actuacion.incorporacion_solicitud.comisionadosolicitud_set.all().order_by("comisionadosolicitud_chofer")
	localidades = actuacion.incorporacion_solicitud.solicitud_localidades.all()
	tareas = actuacion.incorporacion_solicitud.solicitud_tareas
	fechas = actuacion.incorporacion_solicitud.solicitud_fechas()
	decreto_viaticos = actuacion.incorporacion_solicitud.solicitud_decreto_viaticos.montoviaticodiario_decreto_reglamentario

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
			else:
				traslado = "trasladar al mencionado agente"

			dni = "{:,}".format(agente.persona.dni).replace(",", "@").replace(".", ",").replace("@", ".")
			lista_agentes.append(f"{text} {agente_denominacion} - D.N.I.Nº{dni}{colaborador}")
		lista_agentes = separate_items(lista_agentes)

		final_text.update({
			"lista_agentes": lista_agentes,
			"traslado":traslado,
			"chofer":chofer,
		})
		return final_text

	lista_agentes       = generate_agente_list(agentes_solicitud)
	lista_agentes_incorporacion = generate_agente_list(agentes_incorporacion)
	lista_localidades   = docx_texto.generate_localidad_list(localidades)
	lista_fechas        = docx_texto.generate_fechas_list(fechas)
	dias = actuacion.incorporacion_solicitud.solicitud_cantidad_de_dias.days
	articulo_dos        = docx_texto.generate_agente_list_articulo(agentes_incorporacion, dias)

	parrafo_uno		= f"Que por la {resolucion_solicitud}, se tramitó autorización y anticipo de viáticos para {lista_agentes['lista_agentes']} de este Organismo, a fin de {tareas}, en {lista_localidades} {lista_fechas};"
	parrafo_dos     = f"Que resulta necesario incorporar a la misma, a {lista_agentes_incorporacion['lista_agentes']} de este Organismo;"
	parrafo_tres  = f"Que, en consecuencia, deben anticiparse los fondos necesarios para hacer frente a los gastos a realizar, de acuerdo a lo dispuesto en los Decretos Nº1324/1978 y Nº{decreto_viaticos.instrumentolegaldecretos_numero}/{decreto_viaticos.instrumentolegaldecretos_ano};"
	parrafo_cuatro   = f"Que el trámite se encuadra dentro de lo establecido en el Decreto Nº 1324/78 – “Régimen de Viáticos”; y que debido a la fecha a realizarse, incluye días inhábiles deben encuadrarse dentro de las excepciones en el Inciso A; IV Decreto Nº211/20;"

	articulo_uno = f"Incorporar a los agentes, detallados a continuación, a trasladarse a {lista_localidades}, {lista_fechas} a fin de {tareas} y anticipar los importes que se consignan, conforme con el Visto y Considerando de la presente, debiendo rendir cuentas documentadas de sus inversiones, de acuerdo con las reglamentaciones vigentes."

	visto_texto = f"La {resolucion_solicitud} y la Actuación Electrónica Nº{numero_actuacion}; y "
	parrafos = [parrafo_uno, parrafo_dos, parrafo_tres, parrafo_cuatro]
	return visto_texto, parrafos, articulo_uno, articulo_dos


def _generar_incorporacion_docx(actuacion):
	texto = actuacion.incorporacion_texto_actuacion
	if texto:
		visto_texto, _parrafos_default, _articulo_uno_default, _articulo_dos_default = _calcular_texto_incorporacion(actuacion)
		parrafos = texto["parrafos"]
		articulo_uno = texto["articulo_uno"]
		articulo_dos_filas = texto["articulo_dos"]
	else:
		visto_texto, parrafos, articulo_uno, articulo_dos_filas = _calcular_texto_incorporacion(actuacion)

	encabezado = EncabezadoDocumento.vigente()
	with encabezado.encabezadodocumento_archivo.open("rb") as f:
		base_docx = io.BytesIO(f.read())

	return build_resolucion_docx(
		base_docx,
		visto_texto=visto_texto,
		parrafos=parrafos,
		incluir_ultimo_parrafo=actuacion.incorporacion_solicitud.solicitud_dia_inhabil,
		articulo_uno=articulo_uno,
		articulo_dos_filas=articulo_dos_filas,
		articulo_tres=docx_texto.ARTICULO_TRES,
		articulo_cuatro=docx_texto.ARTICULO_CUATRO,
		articulo_cinco=docx_texto.ARTICULO_CINCO,
		considerandos_fijos_finales=docx_texto.CONSIDERANDOS_FIJOS_FINALES,
	)


@login_required
@permission_required("secretariador.change_incorporacion", raise_exception=True)
def editar_texto_incorporacion(request, pk):
	actuacion = Incorporacion.objects.get(pk=pk)
	_visto_texto, parrafos_default, articulo_uno_default, articulo_dos_default = _calcular_texto_incorporacion(actuacion)
	return revisar_texto_actuacion(
		request,
		actuacion=actuacion,
		texto_field_name="incorporacion_texto_actuacion",
		generar_docx_url_name="secretariador:crear-documento-incorporacion",
		parrafos_default=parrafos_default,
		articulo_uno_default=articulo_uno_default,
		articulo_dos_default=articulo_dos_default,
		extra_context={"dia_inhabil": actuacion.incorporacion_solicitud.solicitud_dia_inhabil},
	)


@login_required
@permission_required("secretariador.view_incorporacion", raise_exception=True)
def incorporacion_docx(request, pk):
	actuacion = Incorporacion.objects.get(pk=pk)
	out = _generar_incorporacion_docx(actuacion)

	filename = actuacion.incorporacion_actuacion+".docx"
	response = HttpResponse(out.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
	response["Content-Disposition"] = f'filename="{filename}"'
	return response

@method_decorator(login_required, name="dispatch")
class CrearIncorporacion(PermissionRequiredMixin, generic.CreateView):
	permission_required = "secretariador.add_incorporacion"

	model = Incorporacion
	template_name = "incorporacion/crear-incorporacion.html"
	form_class = IncorporacionForm
	success_url = reverse_lazy("secretariador:crear-incorporacion")
	
	title = "Crear Incorporacion"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super(CrearIncorporacion, self).get_context_data(**kwargs)
		if self.request.POST:
			context['group_formset'] = ComisionadoIncorporacionFormset(self.request.POST, instance=self.object)
			# por que esta vergación tiene que estar acá para que los errores del formset se muestren correctamente?
			context.get('group_formset').errors
		else:
			context['group_formset'] = ComisionadoIncorporacionFormset(instance=self.object)

		return context

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoIncorporacionFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset = comisionadosformset))
	
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoIncorporacionFormset(self.request.POST, instance=self.object)
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
class UpdateIncorporacion(PermissionRequiredMixin, generic.UpdateView):
	permission_required = "secretariador.change_incorporacion"

	model = Incorporacion
	template_name = "incorporacion/update-incorporacion.html"
	form_class = IncorporacionForm
	success_url = reverse_lazy("secretariador:lista-incorporaciones")
	
	def get_context_data(self, **kwargs):
		context = super(UpdateIncorporacion, self).get_context_data(**kwargs)
		if self.request.POST:
			context['group_formset'] = ComisionadoIncorporacionFormset(self.request.POST, instance=self.object)
			# por que esta vergación tiene que estar acá para que los errores del formset se muestren correctamente?
			context.get('group_formset').errors
		else:
			context['group_formset'] = ComisionadoIncorporacionFormset(instance=self.object)

		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoIncorporacionFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset = comisionadosformset))
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		comisionadosformset = ComisionadoIncorporacionFormset(self.request.POST, instance=self.object)
		if form.is_valid() and comisionadosformset.is_valid():
			form.save()
			return self.form_valid(form, comisionadosformset)
		else:
			return self.form_invalid(form, comisionadosformset)
		
	def form_valid(self, form, comisionadosformset):
		formset = comisionadosformset.save(commit=False)
		for field in formset:
			field.comisionadosolicitud_incorporacion_foreign = self.object
			field.save()
		return redirect(reverse_lazy("secretariador:lista-incorporaciones"))
	
	def form_invalid(self, form, comisionadosformset):
		"""
		Renders the response based on the context data with the form and formset if the form is invalid.

		:param form: The form instance.
		:param comisionadosformset: The comisionados formset instance.
		:return: The response rendered based on the context data.
		"""
		return self.render_to_response(self.get_context_data(form=form, comisionadosformset=comisionadosformset))


@method_decorator(login_required, name="dispatch")
class EliminarIncorporacion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "secretariador.delete_incorporacion"

	model = Incorporacion
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-incorporaciones")

# @method_decorator(login_required, name="dispatch")
# class VerIncorporacion(generic.DetailView):
# 	login_url = "/"
# 	redirect_field_name = "login"
# 	model = Solicitud
# 	template_name = "solicitud/ver-incorporacion.incorporacion_solicitud.html"

@login_required
@permission_required("secretariador.view_incorporacion", raise_exception=True)
def PaginaListaIncorporaciones(request):
	template_name = "Lista-incorporaciones.html"

	return render(request, template_name, {})

