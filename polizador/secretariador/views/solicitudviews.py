from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import Solicitud, InstrumentosLegalesDecretos
from carga.models import Provincia
from secretariador.forms.solicitudform import *
from carga.views.generics import get_deleted_objects
from pathlib import Path
from django.conf import settings
import jinja2
from docxtpl import DocxTemplate
from secretariador.forms.mixins import FormsetViewMixin

# Resolve relative to the project root:
BASE = Path(settings.BASE_DIR)
template_path_chaco = BASE / "secretariador/media/solicitud_template.docx"
template_path_exterior = BASE / "secretariador/media/solicitud_exterior.docx"

@login_required
@permission_required("secretariador.view_solicitud", raise_exception=True)
def solicitud_docx(request, pk):
	jinja_env = jinja2.Environment()
	jinja_env.trim_blocks = True
	jinja_env.lstrip_blocks = True

	actuacion = Solicitud.objects.get(pk=pk)
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
	
	def separate_items(items):
	    # Concatenate the items in the list into a string
		concatenated_items = ", ".join(items)
		
		# Replace the last comma with "y"
		last_comma_index = concatenated_items.rfind(",")
		if last_comma_index != -1:
			concatenated_items = concatenated_items[:last_comma_index] + " y" + concatenated_items[last_comma_index + 1:]
		
		return concatenated_items

	def generate_agente_list(agentes):
		lista_agentes = []
		final_text = {}
		for agente in agentes:
			chofer = ""
			colaborador = ""
			agente_denominacion = f"{agente.comisionadosolicitud_nombre.abreviatura} {agente.comisionadosolicitud_nombre.agente_nombres} {agente.comisionadosolicitud_nombre.agente_apellidos}"
			if agente.comisionadosolicitud_nombre.sexo.generoagente_nombre == "Masculino":
				text = "el"
			else:
				text = "la"
				
			if agente.comisionadosolicitud_colaborador:
				colaborador = " en carácter de colaborador"
			else:
				colaborador = ""
		
			if agente.comisionadosolicitud_chofer:
				if agente.comisionadosolicitud_nombre.sexo.generoagente_nombre == "Masculino":
					chofer = f"el {agente_denominacion}"
				else:
					chofer = f"la {agente_denominacion}"

			if len(agentes) > 1:
				traslado = "trasladar a los mencionados agentes"
			else:
				traslado = "trasladar al mencionado agente"
			
			dni = "{:,}".format(agente.comisionadosolicitud_nombre.dni).replace(",", "@").replace(".", ",").replace("@", ".")
			lista_agentes.append(f"{text} {agente_denominacion} - D.N.I.Nº{dni}{colaborador}")
		lista_agentes = separate_items(lista_agentes)

		final_text.update({
			"lista_agentes": lista_agentes,
			"traslado":traslado,
			"chofer":chofer,
		})
		return final_text

	def generate_localidad_list(localidades):
		lista_localidades = []
		final_text = ""
		if len(localidades) > 1:
			text_localidad = "las localidades de"
		else:
			text_localidad = "la localidad de"
		for localidad in localidades:
			lista_localidades.append(str(localidad.localidad_nombre))
		lista_localidades = separate_items(lista_localidades)
		
		final_text = f"{text_localidad} {lista_localidades}"
		return final_text

	def generate_fechas_list(fechas):
		lista_fechas = []
		final_text = ""
		if len(fechas) > 1:
			text_fechas = "los días"
		else:
			text_fechas = "el día"
		for fecha in fechas:
			lista_fechas.append(f"{fecha}")
		lista_fechas = separate_items(lista_fechas)

		final_text = f"{text_fechas} {lista_fechas}"
		return final_text

	def generate_agente_list_articulo(agentes):
		colaborador = ""
		
		final_text = []
		for agente in agentes:
			lista_agentes = []
			agente_cuit = f"{agente.comisionadosolicitud_nombre.abreviatura} {agente.comisionadosolicitud_nombre.agente_nombreyapellido} – CUIL Nº{agente.comisionadosolicitud_nombre.cuil}"
			cantidad_de_dias = f"{actuacion.solicitud_cantidad_de_dias.days} {' dias' if actuacion.solicitud_cantidad_de_dias.days > 1 else ' dia'}"
			comisionadosolicitud_combustible = "{:,.2f}".format(agente.comisionadosolicitud_combustible).replace(",", "@").replace(".", ",").replace("@", ".")
			comisionadosolicitud_pasaje = "{:,.2f}".format(agente.comisionadosolicitud_pasaje).replace(",", "@").replace(".", ",").replace("@", ".")
			comisionadosolicitud_gastos = "{:,.2f}".format(agente.comisionadosolicitud_gastos).replace(",", "@").replace(".", ",").replace("@", ".")
			valor_viatico_dia = "{:,.2f}".format(agente.valor_viatico_dia()).replace(",", "@").replace(".", ",").replace("@", ".")
			valor_viatico_total = "{:,.2f}".format(agente.viaticos_total()).replace(",", "@").replace(".", ",").replace("@", ".")

			subparrafo = f"(Viáticos: {cantidad_de_dias} a razón de ${valor_viatico_dia} diarios"
			if comisionadosolicitud_pasaje != "0,00":
				subparrafo += f" + Pasaje: ${comisionadosolicitud_pasaje}"
			if comisionadosolicitud_gastos != "0,00":
				subparrafo += f" + Gastos: ${comisionadosolicitud_gastos}"
			if comisionadosolicitud_combustible != "0,00":
				subparrafo += f" + Combustible: ${comisionadosolicitud_combustible}"
			subparrafo += f")."

			lista_agentes.append(agente_cuit)
			lista_agentes.append(valor_viatico_total)	
			lista_agentes.append(subparrafo)
			final_text.append(lista_agentes)
		return final_text

	lista_agentes       = generate_agente_list(agentes)
	lista_localidades   = generate_localidad_list(localidades)
	lista_fechas        = generate_fechas_list(fechas)
	lista_agentes_articulo = generate_agente_list_articulo(agentes)

	parrafo_uno     = f"Que por la misma se tramita autorización y anticipo de viáticos para {lista_agentes['lista_agentes']} de este Organismo, para trasladarse a {lista_localidades} {lista_fechas};"
	parrafo_dos     = f"Que dicha comisión, en el marco de las actividades del Organismo, tendrá como objetivo, {lista_agentes['traslado']}, a fin de {tareas} en {lista_localidades};"
	parrafo_tres_1  = f"Que el vehículo afectado será {vehiculo_modelo} – Dominio {vehiculo_patente}"
	parrafo_tres_2  = f", asegurado bajo póliza Nº{vehiculo_poliza} emitida por {vehiculo_poliza_aseguradora}," if vehiculo_poliza else ""
	parrafo_tres_3  = f" conducido por {lista_agentes['chofer']};"
	parrafo_tres    = parrafo_tres_1+parrafo_tres_2+parrafo_tres_3
	parrafo_cuatro  = f"Que, en consecuencia, deben anticiparse los fondos necesarios para hacer frente a los gastos a realizar, de acuerdo a lo dispuesto en los Decretos Nº1324/1978 y Nº{decreto_viaticos.instrumentolegaldecretos_numero}/{decreto_viaticos.instrumentolegaldecretos_ano};"
	parrafo_cinco   = f'Que el trámite se encuadra dentro de lo establecido en el Decreto Nº 1324/78 – "Régimen de Viáticos"; y que debido a la fecha a realizarse, incluye días inhábiles deben encuadrarse dentro de las excepciones en el Inciso A; IV Decreto Nº211/20;'

	articulo_uno            = f"Autorizar a los agentes, detallados a continuación, a trasladarse a {lista_localidades}, {lista_fechas} a fin de {tareas} y anticipar los importes que se consignan, conforme con el Visto y Considerando de la presente, debiendo rendir cuentas documentadas de sus inversiones, de acuerdo con las reglamentaciones vigentes."
	articulo_dos            = lista_agentes_articulo

	if actuacion.solicitud_provincia.provincia_nombre == "Chaco":
		doc = DocxTemplate(template_path_chaco)
		context = {
			"actuacion":actuacion,
			"parrafo_uno":parrafo_uno,
			"parrafo_dos":parrafo_dos,
			"parrafo_tres":parrafo_tres,
			"parrafo_cuatro":parrafo_cuatro,
			"parrafo_cinco":parrafo_cinco,
			"articulo_uno":articulo_uno,
			"articulo_dos":articulo_dos,
		}
	else:
		doc = DocxTemplate(template_path_exterior)
		context = {
			"actuacion":actuacion,
			"parrafo_uno":parrafo_uno,
			"parrafo_dos":parrafo_dos,
			"parrafo_tres":parrafo_tres,
			"parrafo_cuatro":parrafo_cuatro,
			"parrafo_cinco":parrafo_cinco,
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
class CrearSolicitud(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
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
class UpdateSolicitud(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
	permission_required = "secretariador.change_solicitud"
	formset_name = ComisionadoSolicitudFormset
	view_type = "update"

	model = Solicitud
	template_name = "solicitud/update-solicitud.html"
	form_class = SolicitudForm
	success_url = reverse_lazy("secretariador:lista-solicitudes")
	
@method_decorator(login_required, name="dispatch")
class EliminarSolicitud(PermissionRequiredMixin, generic.DeleteView):
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
