from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse

from secretariador.forms.textoactuacionform import ArticuloDosFormSet, ArticuloUnoForm, ParrafoFormSet
from secretariador.models import EncabezadoDocumento

TEMPLATE_NAME = "solicitud/editar-texto-actuacion.html"


def texto_actuacion_guardado(actuacion, texto_field_name):
	return getattr(actuacion, texto_field_name)


def _articulo_dos_inicial(articulo_dos_default, texto_guardado):
	"""Filas a mostrar en el formset: siempre una por cada agente
	comisionado actual (`articulo_dos_default`); si hay texto guardado para
	ese agente se usa el guardado, si no el recién calculado."""
	guardadas_por_agente = {}
	if texto_guardado:
		guardadas_por_agente = {fila["comisionado_id"]: fila for fila in texto_guardado.get("articulo_dos", [])}
	filas = []
	for fila in articulo_dos_default:
		filas.append(guardadas_por_agente.get(fila["comisionado_id"], fila))
	return filas


def revisar_texto_actuacion(request, *, actuacion, texto_field_name, generar_docx_url_name,
							 parrafos_default, articulo_uno_default, articulo_dos_default,
							 extra_context=None):
	"""
	Vista GET/POST compartida por los tres flujos (solicitud, solicitud
	exterior, incorporación) para revisar/editar el texto de considerandos
	y artículos antes de generar el .docx.

	`parrafos_default`/`articulo_uno_default`/`articulo_dos_default` son el
	texto recién calculado con las reglas de negocio de cada flujo (mismas
	que se usaban antes para armar directamente el .docx). Si la actuación
	ya tiene texto guardado en `texto_field_name`, se usa ese como valor
	inicial del formulario en lugar del recién calculado.
	"""
	if EncabezadoDocumento.vigente() is None:
		return HttpResponseServerError(
			"No hay ningún documento base cargado. Subí uno desde "
			"\"Actualizar Encabezado\" antes de generar resoluciones."
		)

	texto_guardado = texto_actuacion_guardado(actuacion, texto_field_name)

	if request.method == "POST":
		parrafo_formset = ParrafoFormSet(request.POST, prefix="parrafos")
		articulo_uno_form = ArticuloUnoForm(request.POST, prefix="articulo_uno")
		articulo_dos_formset = ArticuloDosFormSet(request.POST, prefix="articulo_dos")

		if parrafo_formset.is_valid() and articulo_uno_form.is_valid() and articulo_dos_formset.is_valid():
			payload = {
				"parrafos": [form.cleaned_data["texto"] for form in parrafo_formset],
				"articulo_uno": articulo_uno_form.cleaned_data["articulo_uno"],
				"articulo_dos": [
					{
						"comisionado_id": form.cleaned_data["comisionado_id"],
						"nombre_cuil": form.cleaned_data["nombre_cuil"],
						"monto": form.cleaned_data["monto"],
						"subparrafo": form.cleaned_data["subparrafo"],
					}
					for form in articulo_dos_formset
				],
			}
			setattr(actuacion, texto_field_name, payload)
			actuacion.save(update_fields=[texto_field_name])
			if request.POST.get("accion") == "guardar":
				return redirect(actuacion.get_absolute_url())
			return redirect(reverse(generar_docx_url_name, kwargs={"pk": actuacion.pk}))
	else:
		parrafo_formset = ParrafoFormSet(
			prefix="parrafos",
			initial=[{"texto": texto} for texto in (texto_guardado["parrafos"] if texto_guardado else parrafos_default)],
		)
		articulo_uno_form = ArticuloUnoForm(
			prefix="articulo_uno",
			initial={"articulo_uno": texto_guardado["articulo_uno"] if texto_guardado else articulo_uno_default},
		)
		articulo_dos_formset = ArticuloDosFormSet(
			prefix="articulo_dos",
			initial=_articulo_dos_inicial(articulo_dos_default, texto_guardado),
		)

	context = {
		"actuacion": actuacion,
		"parrafo_formset": parrafo_formset,
		"articulo_uno_form": articulo_uno_form,
		"articulo_dos_formset": articulo_dos_formset,
	}
	context.update(extra_context or {})
	return render(request, TEMPLATE_NAME, context)
