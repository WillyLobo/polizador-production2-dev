from django.urls import path

from django.views.generic import TemplateView
from secretariador.views.ajaxviews import get_agentes
from secretariador.views.solicitudviews import *
from secretariador.views.solicitud_exteriorviews import *
from secretariador.views.comisionadoviews import *
from secretariador.views.instrumentolegalviews import *
from secretariador.views.vehiculoviews import *
from secretariador.views.montoviaticodiarioviews import *
from secretariador.views.incorporacionviews import *
from secretariador.views.reportesviews import *
from secretariador.views.delete_inlines import *
from secretariador.views.redirects import *
from secretariador.views.encabezadoviews import *

app_name = "secretariador"

urlpatterns = [
]
redirects = [
    path("redirect_decreto/", redirect_decretos, name="redirect-decreto"),
    path("redirect_solicitudes/", redirect_solicitudes, name="redirect-solicitud"),
    path("redirect_resoluciones/", redirect_resoluciones, name="redirect-resoluciones"),
]
instrumento_legal_decreto_patterns = [
	path("creardecreto/", CrearInstrumentoLegalDecreto.as_view(), name="crear-decreto"),
    path("creardecreto/<pk>", UpdateInstrumentoLegalDecreto.as_view(), name="update-decreto"),
    path("eliminar/decreto/<pk>", EliminarInstrumentoLegalDecreto.as_view(), name="eliminar-decreto"),
]
instrumento_legal_memorandum_patterns = [
	path("crearmemorandum/", CrearInstrumentoLegalMemorandum.as_view(), name="crear-memorandum"),
    path("crearmemorandum/<pk>", UpdateInstrumentoLegalMemorandum.as_view(), name="update-memorandum"),
    path("eliminar/memorandum/<pk>", EliminarInstrumentoLegalMemorandum.as_view(), name="eliminar-memorandum"),
]
monto_viatico_diario_patterns = [
    path("crearmontoviaticodiario/", CrearMontoViaticoDiario.as_view(), name="crear-montoviaticodiario"),
    path("crearmontoviaticodiario/<pk>", UpdateMontoViaticoDiario.as_view(), name="update-montoviaticodiario"),
    path("eliminar/montoviaticodiario/<pk>", EliminarMontoViaticoDiario.as_view(), name="eliminar-montoviaticodiario"),
]
instrumento_legal_resolucion_patterns = [
	path("crearresolucionpresidencia/", CrearInstrumentoLegalResolucionPresidencia.as_view(), name="crear-resolucion-presidencia"),
    path("crearresolucionpresidencia/<pk>", UpdateInstrumentoLegalResolucionPresidencia.as_view(), name="update-resolucion-presidencia"),
    path("eliminar/resolucionpresidencia/<pk>", EliminarInstrumentoLegalResolucionPresidencia.as_view(), name="eliminar-resolucion-presidencia"),
	path("crearresoluciondirectorio/", CrearInstrumentoLegalResolucionDirectorio.as_view(), name="crear-resolucion-directorio"),
    path("crearresoluciondirectorio/<pk>", UpdateInstrumentoLegalResolucionDirectorio.as_view(), name="update-resolucion-directorio"),
    path("eliminar/resoluciondirectorio/<pk>", EliminarInstrumentoLegalResolucionDirectorio.as_view(), name="eliminar-resolucion-directorio"),
]
solicitud_patterns = [
	path("crearsolicitud/", CrearSolicitud.as_view(), name="crear-solicitud"),
	path("crearsolicitud/<pk>", UpdateSolicitud.as_view(), name="update-solicitud"),
	path("crearsolicitud/ver/<pk>", VerSolicitud.as_view(), name="ver-solicitud"),
    path("eliminar/solicitud/<pk>", EliminarSolicitud.as_view(), name="eliminar-solicitud"),
    path('delete-comisionadosolicitud/<int:pk>/', delete_comisionadosolicitud, name='delete-comisionado-solicitud'),
]
solicitud_exterior_patterns = [
	path("crearsolicitudexterior/", CrearSolicitudExterior.as_view(), name="crear-solicitud-exterior"),
	path("crearsolicitudexterior/<pk>", UpdateSolicitudExterior.as_view(), name="update-solicitud-exterior"),
	# path("crearsolicitudexterior/ver/<pk>", VerSolicitud.as_view(), name="ver-solicitud"),
    path("eliminar/solicitudexterior/<pk>", EliminarSolicitudExterior.as_view(), name="eliminar-solicitud-exterior"),
]
vehiculo_patterns = [
    path("crearvehiculo/", CrearVehiculo.as_view(), name="crear-vehiculo"),
    path("crearvehiculo/<pk>", UpdateVehiculo.as_view(), name="update-vehiculo"),
    path("eliminar/vehiculo/<pk>", EliminarVehiculo.as_view(), name="eliminar-vehiculo"),
]
docx_patterns = [
    path("creardocumento/solicitud/<pk>", solicitud_docx, name="crear-documento-solicitud"),
    path("creardocumento/solicitudexterior/<pk>", exterior_docx, name="crear-documento-solicitud-exterior"),
    path("creardocumento/incorporacion/<pk>", incorporacion_docx, name="crear-documento-incorporacion"),
]
encabezado_patterns = [
    path("actualizar-encabezado/", ActualizarEncabezado.as_view(), name="actualizar-encabezado"),
]
comisionado_patterns = [
    path("crearcomisionado/", CrearComisionado.as_view(), name="crear-comisionado"),
    path("crearcomisionado/<pk>", UpdateComisionado.as_view(), name="update-comisionado"),
    path("eliminar/comisionado/<pk>", EliminarComisionado.as_view(), name="eliminar-comisionado"),
]
incorporacion_patterns = [
    path("crearincorporacion/", CrearIncorporacion.as_view(), name="crear-incorporacion"),
    path("crearincorporacion/<pk>", UpdateIncorporacion.as_view(), name="update-incorporacion"),
    path("eliminar/incorporacion/<pk>", EliminarIncorporacion.as_view(), name="eliminar-incorporacion"),
    path('delete-incorporacion-comisionadosolicitud/<int:pk>/', delete_incorporacion_comisionadosolicitud, name='delete-incorporacion-comisionado-solicitud'),
]
reportes_patterns = [
    path("reportes/viaticos-agente/", CrearReporteViaticosPorAgente.as_view(), name="crear-reporte-viaticos-por-agente"),
    path("reportes/viaticos-agente-individual/", CrearReporteViaticosPorAgenteIndividual.as_view(), name="crear-reporte-viaticos-por-agente-individual"),
    path("reportes/calendario-semanal/", CalendarioSemanal.as_view(), name="calendario-semanal"),
    path("reportes/calendario-anual/", CalendarioAnual.as_view(), name="calendario-anual"),
    path("reportes/viaticos-area/", CrearReporteViaticosporArea.as_view(), name="crear-reporte-viaticos-por-area"),
    path("reportes/ausencias/", CrearReporteAusenciasPorAgente.as_view(), name="crear-reporte-ausencias-por-agente"),
    path("reportes/duplicados/", CrearReporteComisionesDuplicadas.as_view(), name="crear-reporte-duplicados"),
    path("pdf_merge/", PDFMergeTemplateView.as_view(), name="pdf-merge"),
]
# documentos_digitales = [
#     path("digitales/crear-contrato-digital/", CrearContratoDigital.as_view(), name="crear-contrato-digital"),
#     path("digitales/crear-contrato-digital/<pk>", UpdateContratoDigital.as_view(), name="update-contrato-digital"),
#     path("eliminar/digital/contrato/<pk>", EliminarContratoDigital.as_view(), name="eliminar-contrato-digital"),
#     path("digitales/crear-resolucion-digital/", CrearResolucionDigital.as_view(), name="crear-resolucion-digital"),
#     path("digitales/crear-resolucoin-digital/<pk>", UpdateResolucionDigital.as_view(), name="update-resolucion-digital"),
#     path("eliminar/digital/resolucion/<pk>", EliminarResolucionDigital.as_view(), name="eliminar-resolucion-digital")
# ]

ajax = [
	# Solicitudes
	path("listas/solicitudes", PaginaListaSolicitudes, name="lista-solicitudes"),
    # Comisionados
	path("listas/comisionados", PaginaListaComisionados, name="lista-comisionados"),
    # Memorandum
    path("listas/memorandum", PaginaListaInstrumentosLegalesMemorandum, name="lista-memorandum"),
    # Decretos
    path("listas/decretos", PaginaListaInstrumentosLegalesDecretos, name="lista-decretos"),
    # Resoluciones
    path("listas/resoluciones", PaginaListaInstrumentosLegalesResoluciones, name="lista-resoluciones"),
    # Vehiculos
    path("listas/vehiculos", PaginaListaVehiculos, name="lista-vehiculos"),
    # Incorporaciones
    path("listas/incorporaciones", PaginaListaIncorporaciones, name="lista-incorporaciones"),
    # Agente Query
    path("ajax/get_agentes/", get_agentes, name="get-agentes"),
]
template_views = [
    
]

urlpatterns += redirects
urlpatterns += ajax
urlpatterns += template_views
urlpatterns += instrumento_legal_memorandum_patterns
urlpatterns += instrumento_legal_decreto_patterns
urlpatterns += monto_viatico_diario_patterns
urlpatterns += instrumento_legal_resolucion_patterns
urlpatterns += solicitud_patterns
urlpatterns += solicitud_exterior_patterns
urlpatterns += comisionado_patterns
urlpatterns += incorporacion_patterns
urlpatterns += vehiculo_patterns
urlpatterns += reportes_patterns
urlpatterns += docx_patterns
urlpatterns += encabezado_patterns
