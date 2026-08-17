import io

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import EncabezadoDocumento, Solicitud, InstrumentosLegalesDecretos
from carga.models import Provincia
from secretariador.forms.solicitudform import *
from core.mixins import DeleteRelatedObjectsMixin, FormsetViewMixin, UserFormsetKwargsMixin
from secretariador import docx_texto
from secretariador.docx_texto import separate_items
from secretariador.docx_builder import build_resolucion_docx
from secretariador.views.textoactuacionviews import revisar_texto_actuacion


def _calcular_texto_solicitud(actuacion):
	"""Arma, a partir de los datos actuales de la Solicitud, el texto por
	default (VISTO/considerandos/artículos) que se ofrece como punto de
	partida en el formulario de edición y como fallback si la actuación
	todavía no tiene texto guardado en `solicitud_texto_actuacion`."""
	agentes = actuacion.comisionadosolicitud_set.all().order_by("comisionadosolicitud_chofer")
	localidades = actuacion.solicitud_localidades.all()
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
		chofer = ""
		if len(agentes) > 1:
			traslado = "trasladar a los mencionados agentes"
		else:
			traslado = "trasladar al mencionado agente"
		for agente in agentes:
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

			dni = "{:,}".format(agente.persona.dni).replace(",", "@").replace(".", ",").replace("@", ".")
			lista_agentes.append(f"{text} {agente_denominacion} - D.N.I.Nº{dni}{colaborador}")
		lista_agentes = separate_items(lista_agentes)

		final_text.update({
			"lista_agentes": lista_agentes,
			"traslado":traslado,
			"chofer":chofer,
		})
		return final_text

	lista_agentes       = generate_agente_list(agentes)
	lista_localidades   = docx_texto.generate_localidad_list(localidades)
	lista_fechas        = docx_texto.generate_fechas_list(fechas)
	articulo_dos        = docx_texto.generate_agente_list_articulo(agentes, actuacion.solicitud_cantidad_de_dias.days)

	parrafo_uno     = f"Que por la misma se tramita autorización y anticipo de viáticos para {lista_agentes['lista_agentes']} de este Organismo, para trasladarse a {lista_localidades} {lista_fechas};"
	parrafo_dos     = f"Que dicha comisión, en el marco de las actividades del Organismo, tendrá como objetivo, {lista_agentes['traslado']}, a fin de {tareas} en {lista_localidades};"
	parrafo_tres_1  = f"Que el vehículo afectado será {vehiculo_modelo} – Dominio {vehiculo_patente}"
	parrafo_tres_2  = f", asegurado bajo póliza Nº{vehiculo_poliza} emitida por {vehiculo_poliza_aseguradora}," if vehiculo_poliza else ""
	parrafo_tres_3  = f" conducido por {lista_agentes['chofer']};"
	parrafo_tres    = parrafo_tres_1+parrafo_tres_2+parrafo_tres_3
	parrafo_cuatro  = f"Que, en consecuencia, deben anticiparse los fondos necesarios para hacer frente a los gastos a realizar, de acuerdo a lo dispuesto en los Decretos Nº1324/1978 y Nº{decreto_viaticos.instrumentolegaldecretos_numero}/{decreto_viaticos.instrumentolegaldecretos_ano};"
	parrafo_cinco   = f'Que el trámite se encuadra dentro de lo establecido en el Decreto Nº 1324/78 – "Régimen de Viáticos"; y que debido a la fecha a realizarse, incluye días inhábiles deben encuadrarse dentro de las excepciones en el Inciso A; IV Decreto Nº211/20;'

	articulo_uno = f"Autorizar a los agentes, detallados a continuación, a trasladarse a {lista_localidades}, {lista_fechas} a fin de {tareas} y anticipar los importes que se consignan, conforme con el Visto y Considerando de la presente, debiendo rendir cuentas documentadas de sus inversiones, de acuerdo con las reglamentaciones vigentes."

	visto_texto = f"La Actuación Electrónica Nº{actuacion.solicitud_actuacion}; y "
	parrafos = [parrafo_uno, parrafo_dos, parrafo_tres, parrafo_cuatro, parrafo_cinco]
	return visto_texto, parrafos, articulo_uno, articulo_dos


def _generar_solicitud_docx(actuacion):
	texto = actuacion.solicitud_texto_actuacion
	if texto:
		visto_texto, _parrafos_default, _articulo_uno_default, _articulo_dos_default = _calcular_texto_solicitud(actuacion)
		parrafos = texto["parrafos"]
		articulo_uno = texto["articulo_uno"]
		articulo_dos_filas = texto["articulo_dos"]
	else:
		visto_texto, parrafos, articulo_uno, articulo_dos_filas = _calcular_texto_solicitud(actuacion)

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
def editar_texto_solicitud(request, pk):
	actuacion = Solicitud.objects.get(pk=pk)
	_visto_texto, parrafos_default, articulo_uno_default, articulo_dos_default = _calcular_texto_solicitud(actuacion)
	return revisar_texto_actuacion(
		request,
		actuacion=actuacion,
		texto_field_name="solicitud_texto_actuacion",
		generar_docx_url_name="secretariador:crear-documento-solicitud",
		parrafos_default=parrafos_default,
		articulo_uno_default=articulo_uno_default,
		articulo_dos_default=articulo_dos_default,
		extra_context={"dia_inhabil": actuacion.solicitud_dia_inhabil},
	)


@login_required
@permission_required("secretariador.view_solicitud", raise_exception=True)
def solicitud_docx(request, pk):
	actuacion = Solicitud.objects.get(pk=pk)
	out = _generar_solicitud_docx(actuacion)

	filename = actuacion.solicitud_actuacion+".docx"
	response = HttpResponse(out.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
	response["Content-Disposition"] = f'filename="{filename}"'
	return response

@method_decorator(login_required, name="dispatch")
class CrearSolicitud(PermissionRequiredMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.CreateView):
	permission_required = "secretariador.add_solicitud"
	formset_name = ComisionadoSolicitudFormset
	view_type = "create"

	model = Solicitud
	template_name = "solicitud/crear-solicitud.html"
	form_class = SolicitudForm
	success_url = reverse_lazy("secretariador:crear-solicitud")
	
	title = "Crear Solicitud"

	def get_title(self):
		return self.title
	
@method_decorator(login_required, name="dispatch")
class UpdateSolicitud(PermissionRequiredMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "secretariador.change_solicitud"
	formset_name = ComisionadoSolicitudFormset
	view_type = "update"

	model = Solicitud
	template_name = "solicitud/update-solicitud.html"
	form_class = SolicitudForm
	success_url = reverse_lazy("secretariador:lista-solicitudes")
	
@method_decorator(login_required, name="dispatch")
class EliminarSolicitud(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "secretariador.delete_solicitud"

	model = Solicitud
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-solicitudes")

@method_decorator(login_required, name="dispatch")
class VerSolicitud(PermissionRequiredMixin, generic.DetailView):
	permission_required = "secretariador.view_solicitud"

	model = Solicitud
	template_name = "solicitud/ver-solicitud.html"

@login_required
@permission_required("secretariador.view_solicitud", raise_exception=True)
def PaginaListaSolicitudes(request):
	template_name = "Lista-solicitudes.html"

	return render(request, template_name, {})
