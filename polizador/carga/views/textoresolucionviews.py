from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from carga.forms.textoresolucionforms import (
	BLOQUES_INICIALES,
	BloqueFormSet,
	BloqueTextoFormSet,
	CertificadoMuestraForm,
	TextoResolucionForm,
)
from carga.models import Certificado, TextoResolucionCertificado
from carga.resolucion_docx import ResolucionDocxError, build_resolucion_certificado, numerar_articulos
from carga.resolucion_texto import FILTROS_DOC, VARIABLES, TextoResolucionError, contexto_certificado, render_bloques
from core.mixins import DeleteRelatedObjectsMixin

PREFIJO_BLOQUES = "bloques"


def _previsualizar(bloques, certificado):
	"""Renderiza `bloques` contra `certificado` para el panel de vista previa.

	Devuelve `(bloques_renderizados, faltantes, error)`. Nunca lanza: el editor
	tiene que poder mostrar el problema al lado del texto, no un 500."""
	if certificado is None:
		return None, set(), None
	try:
		contexto = contexto_certificado(certificado)
		resueltos, faltantes = render_bloques(bloques, contexto)
	except TextoResolucionError as e:
		return None, set(), str(e)
	except Exception as e:  # noqa: BLE001 - datos incompletos del certificado de muestra
		return None, set(), f"No se pudo previsualizar con este certificado: {e}"
	return numerar_articulos(resueltos), faltantes, None


class TextoResolucionEditorMixin:
	"""GET/POST del editor de plantillas: form de alcance + formset de bloques +
	panel de vista previa contra un certificado de muestra.

	La vista previa se hace con un POST normal (`accion=previsualizar`) que
	re-renderiza la página. Es el mismo ida y vuelta que usa el resto del sistema,
	se testea con `self.client.post`, y evita estrenar htmx (que está cargado en
	base.html pero no lo usa ninguna plantilla todavía, así que no hay patrón de
	CSRF establecido)."""

	template_name = "textoresolucion/editar-texto-resolucion.html"
	form_class = TextoResolucionForm
	model = TextoResolucionCertificado
	success_url = reverse_lazy("carga:lista-textos-resolucion")
	view_type = None
	"""'create' o 'update', igual que FormsetViewMixin en core/mixins.py."""
	title = ""

	def bloques_iniciales(self):
		raise NotImplementedError

	def get(self, request, *args, **kwargs):
		self.object = self.get_object() if self.view_type == "update" else None
		formset = BloqueFormSet(prefix=PREFIJO_BLOQUES, initial=self.bloques_iniciales())
		muestra = CertificadoMuestraForm(initial={"certificado": request.GET.get("certificado") or None})
		return self.render_to_response(
			self.get_context_data(form=self.get_form(), formset=formset, muestra=muestra)
		)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object() if self.view_type == "update" else None
		form = self.get_form()
		formset = BloqueFormSet(request.POST, prefix=PREFIJO_BLOQUES)
		muestra = CertificadoMuestraForm(request.POST)

		# No usar "and": los dos tienen que validar siempre, para que la página
		# vuelva con todos los errores marcados y no de a uno.
		form_ok = form.is_valid()
		formset_ok = formset.is_valid()
		muestra.is_valid()

		if formset_ok and request.POST.get("accion") == "previsualizar":
			return self.render_to_response(
				self.get_context_data(
					form=form, formset=formset, muestra=muestra,
					bloques=formset.bloques_validos(),
					certificado=muestra.cleaned_data.get("certificado"),
				)
			)

		if form_ok and formset_ok:
			self.object = form.save(commit=False)
			self.object.textoresolucion_bloques = formset.bloques_validos()
			self.object.save()
			return HttpResponseRedirect(self.get_success_url())

		return self.render_to_response(self.get_context_data(form=form, formset=formset, muestra=muestra))

	def get_context_data(self, **kwargs):
		formset = kwargs.pop("formset", None)
		muestra = kwargs.pop("muestra", None)
		bloques = kwargs.pop("bloques", None)
		certificado = kwargs.pop("certificado", None)
		context = super().get_context_data(**kwargs)

		preview, faltantes, error = _previsualizar(bloques, certificado)
		context.update({
			"title": self.title,
			"formset": formset,
			"muestra": muestra,
			"variables": VARIABLES,
			"filtros_doc": FILTROS_DOC,
			"preview": preview,
			"preview_faltantes": sorted(faltantes),
			"preview_error": error,
			"certificado_muestra": certificado,
		})
		return context


@method_decorator(login_required, name="dispatch")
class CrearTextoResolucion(TextoResolucionEditorMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "carga.add_textoresolucioncertificado"
	view_type = "create"
	title = "Nuevo texto de resolución"

	def bloques_iniciales(self):
		# Arrancar de un esqueleto y no de una pantalla en blanco.
		return BLOQUES_INICIALES


@method_decorator(login_required, name="dispatch")
class UpdateTextoResolucion(TextoResolucionEditorMixin, PermissionRequiredMixin, generic.UpdateView):
	permission_required = "carga.change_textoresolucioncertificado"
	view_type = "update"
	title = "Editar texto de resolución"

	def bloques_iniciales(self):
		return self.object.textoresolucion_bloques or []


@method_decorator(login_required, name="dispatch")
class EliminarTextoResolucion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
	permission_required = "carga.delete_textoresolucioncertificado"

	model = TextoResolucionCertificado
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("carga:lista-textos-resolucion")


@method_decorator(login_required, name="dispatch")
class ListaTextosResolucion(PermissionRequiredMixin, generic.ListView):
	"""Listado simple: es un catálogo de unas pocas decenas de filas, no justifica
	el ida y vuelta de datatables que usan las listas grandes del sistema."""
	permission_required = "carga.view_textoresolucioncertificado"

	model = TextoResolucionCertificado
	template_name = "textoresolucion/lista-textos-resolucion.html"
	context_object_name = "textos"

	def get_queryset(self):
		return super().get_queryset().select_related("textoresolucion_programa")


# --------------------------------------------------------------------------- #
# Texto de la resolución de un Certificado concreto
# --------------------------------------------------------------------------- #

def _texto_certificado(certificado):
	"""Bloques a mostrar/emitir para `certificado`, junto con las variables que
	quedaron sin resolver.

	Si el certificado ya tiene un snapshot editado a mano se usa ese tal cual (ya
	está renderizado); si no, se resuelve la plantilla del alcance contra los datos
	actuales. Devuelve `(bloques, faltantes, plantilla, error)`; `plantilla` es None
	cuando no hay ningún texto base cargado para el alcance del certificado."""
	snapshot = certificado.certificado_texto_resolucion
	if snapshot and snapshot.get("bloques"):
		return snapshot["bloques"], set(), None, None

	plantilla = TextoResolucionCertificado.para_certificado(certificado)
	if plantilla is None:
		return None, set(), None, None

	try:
		contexto = contexto_certificado(certificado)
		bloques, faltantes = render_bloques(plantilla.textoresolucion_bloques, contexto)
	except TextoResolucionError as e:
		return None, set(), plantilla, str(e)
	return bloques, faltantes, plantilla, None


def _sin_plantilla(request, certificado):
	"""Pantalla de 'no hay texto base para este alcance', con el link para crearlo
	ya apuntando al certificado como muestra. No es un 404: el certificado existe,
	lo que falta es la plantilla."""
	return render(request, "textoresolucion/sin-texto-resolucion.html", {
		"certificado": certificado,
		"obra": certificado.certificado_obra,
	}, status=409)


@login_required
@permission_required("carga.change_certificado", raise_exception=True)
def editar_texto_resolucion_certificado(request, pk):
	"""Revisión del texto ya resuelto, antes de emitir el .docx.

	Espeja `revisar_texto_actuacion` de viáticos: lo que se guarda es el texto
	final, no la plantilla, y queda anotado de qué plantilla (y de qué versión de
	esa plantilla) salió."""
	certificado = get_object_or_404(Certificado, pk=pk)
	bloques, faltantes, plantilla, error = _texto_certificado(certificado)
	if bloques is None and plantilla is None:
		return _sin_plantilla(request, certificado)

	if request.method == "POST":
		formset = BloqueTextoFormSet(request.POST, prefix=PREFIJO_BLOQUES)
		if formset.is_valid():
			certificado.certificado_texto_resolucion = {
				"textoresolucion_id": plantilla.pk if plantilla else (certificado.certificado_texto_resolucion or {}).get("textoresolucion_id"),
				"textoresolucion_history_id": _history_id(plantilla),
				"bloques": formset.bloques(),
			}
			certificado.save(update_fields=["certificado_texto_resolucion"])
			if request.POST.get("accion") == "guardar":
				return HttpResponseRedirect(certificado.get_absolute_url())
			return HttpResponseRedirect(reverse("carga:resolucion-certificado-docx", kwargs={"pk": certificado.pk}))
	else:
		formset = BloqueTextoFormSet(prefix=PREFIJO_BLOQUES, initial=bloques or [])

	return render(request, "textoresolucion/revisar-texto-certificado.html", {
		"certificado": certificado,
		"obra": certificado.certificado_obra,
		"formset": formset,
		"faltantes": sorted(faltantes),
		"plantilla": plantilla,
		"error": error,
		"es_snapshot": bool(certificado.certificado_texto_resolucion),
	})


def _history_id(plantilla):
	"""Id de la fila histórica vigente de `plantilla`, para poder auditar después
	con qué versión del texto base se emitió una resolución."""
	if plantilla is None:
		return None
	ultima = plantilla.textoresolucion_history.order_by("-history_date").first()
	return ultima.history_id if ultima else None


@login_required
@permission_required("carga.view_certificado", raise_exception=True)
def resolucion_certificado_docx(request, pk):
	certificado = get_object_or_404(Certificado, pk=pk)
	bloques, faltantes, plantilla, error = _texto_certificado(certificado)
	if bloques is None and plantilla is None:
		return _sin_plantilla(request, certificado)
	if error:
		return HttpResponseServerError(error)
	if faltantes:
		# Una resolución se firma: emitirla con «falta: ...» adentro es peor que no
		# emitirla. Se manda a revisar el texto, donde se ve qué falta y dónde.
		messages.error(
			request,
			"No se puede generar la resolución: faltan datos ({}).".format(", ".join(sorted(faltantes))),
		)
		return redirect("carga:editar-texto-resolucion-certificado", pk=certificado.pk)

	try:
		salida = build_resolucion_certificado(bloques)
	except ResolucionDocxError as e:
		return HttpResponseServerError(str(e))

	nombre = f"resolucion-certificado-{certificado.certificado_expediente}.docx".replace("/", "-")
	respuesta = HttpResponse(
		salida.read(),
		content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
	)
	respuesta["Content-Disposition"] = f'attachment; filename="{nombre}"'
	return respuesta


@login_required
@permission_required("carga.change_certificado", raise_exception=True)
def restaurar_texto_resolucion_certificado(request, pk):
	"""Descarta el snapshot editado a mano y vuelve a resolver desde la plantilla."""
	certificado = get_object_or_404(Certificado, pk=pk)
	if request.method == "POST":
		Certificado.objects.filter(pk=certificado.pk).update(certificado_texto_resolucion=None)
		messages.success(request, "Se restauró el texto desde la plantilla.")
	return redirect("carga:editar-texto-resolucion-certificado", pk=certificado.pk)
