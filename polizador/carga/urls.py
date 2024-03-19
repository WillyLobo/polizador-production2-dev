from django.urls import path

from carga.views.certificadoviews import *
from carga.views.polizaviews import *
from carga.views.empresaviews import *
from carga.views.obraviews import *
from carga.views.regionviews import *
from carga.views.departamentoviews import *
from carga.views.localidadviews import *
from carga.views.municipioviews import *
from carga.views.receptorviews import *
from carga.views.areaviews import *
from carga.views.aseguradoraviews import *
from carga.views.programaviews import *
from carga.views.agenteviews import *
from carga.views.conjuntoviews import *
from carga.views.reportes import *
from carga.views.contratoviews import *
from carga.views.documentosdigitalesviews import *

app_name = "carga"

urlpatterns = [
]
empresa_patterns = [
	path("crear/empresa/", CrearEmpresa.as_view(), name="crear-empresa"),
	path("crear/empresa/<pk>", UpdateEmpresa.as_view(), name="update-empresa"),
	path("crear/empresa/obra/<pk>", EmpresaObra.as_view(), name="empresa-obra"),
    path("eliminar/empresa/<pk>", EliminarEmpresa.as_view(), name="eliminar-empresa")
]
certificado_patterns = [
	path("crear/certificado/", CrearCertificado.as_view(), name="crear-certificado"),
	path("crear/certificado/<pk>", UpdateCertificado.as_view(), name="update-certificado"),
	path("crear/certificado/detalle/<pk>", CertificadoView.as_view(), name="detalle-certificado"),
    path("eliminar/certificado/<pk>", EliminarCertificado.as_view(), name="eliminar-certificado")
]
obra_patterns = [
	path("crear/obra/", CrearObra.as_view(), name="crear-obra"),
	path("crear/obra/<pk>", UpdateObra.as_view(), name="update-obra"),
	path("crear/obra/estado/<pk>", EstadoObra.as_view(), name = "estado-obra"),
    path("eliminar/obra/<pk>", EliminarObra.as_view(), name="eliminar-obra"),
]
poliza_patterns = [
	path("crear/poliza/", CrearPoliza.as_view(), name="crear-poliza"),
	path("crear/poliza/<pk>", UpdatePoliza.as_view(), name="update-poliza"),
	path("crear/poliza/estado/<pk>", EstadoPoliza.as_view(), name="estado-poliza"),
    path("eliminar/poliza/<pk>", EliminarPoliza.as_view(), name="eliminar-poliza")
]
movimiento_patterns = [
	path("crear/poliza/movimiento/", CrearPolizaMovimiento.as_view(), name="crear-poliza-movimiento"),
	path("crear/poliza/movimiento/<pk>", UpdatePolizaMovimiento.as_view(), name="update-poliza-movimiento"),
	path("crear/poliza/movimiento/imprimir/<pk>", ImprimirPolizaMovimiento.as_view(), name="imprimir-poliza-movimiento"),
    path("eliminar/poliza/movimiento/<pk>", EliminarPolizaMovimiento.as_view(), name="eliminar-poliza-movimiento")
]
legacy_patterns = [
	path("legacy_imprimir/<pk>", ImprimirLegacyPoliza.as_view(), name="legacy-imprimir-poliza"),
	path("legacy_update/<pk>", UpdateLegacyPoliza.as_view(), name="legacy-update-poliza"),
]
region_patterns = [
	path("crear/region/", CrearRegion.as_view(), name="crear-region"),
	path("crear/region/<pk>", UpdateRegion.as_view(), name="update-region"),
	path("crear/region/obra/<pk>", RegionObra.as_view(), name="region-obra"),
    path("eliminar/region/<pk>", EliminarRegion.as_view(), name="eliminar-region")
]
departamento_patterns = [
	path("crear/departamento/", CrearDepartamento.as_view(), name="crear-departamento"),
	path("crear/departamento/<pk>", UpdateDepartamento.as_view(), name="update-departamento"),
	path("crear/departamento/obra/<pk>",DepartamentoObra.as_view(), name="departamento-obra"),
    path("eliminar/departamento/<pk>", EliminarDepartamento.as_view(), name="eliminar-departamento")
	]
localidad_patterns = [
	path("crear/localidad/", CrearLocalidad.as_view(), name="crear-localidad"),
	path("crear/localidad/<pk>", UpdateLocalidad.as_view(), name="update-localidad"),
	path("crear/localidad/obra/<pk>", LocalidadObra.as_view(), name="localidad-obra"),
    path("eliminar/localidad/<pk>", EliminarLocalidad.as_view(), name="eliminar-localidad")
]
municipio_patterns = [
	path("crear/municipio/", CrearMunicipio.as_view(), name="crear-municipio"),
	path("crear/municipio/<pk>", UpdateMunicipio.as_view(), name="update-municipio"),
	path("crear/municipio/obra/<pk>", MunicipioObra.as_view(), name="municipio-obra"),
    path("eliminar/municipio/<pk>", EliminarMunicipio.as_view(), name="eliminar-municipio")
]
receptor_patterns = [
	path("crear/receptor/", CrearReceptor.as_view(), name="crear-receptor"),
	path("crear/receptor/<pk>", UpdateReceptor.as_view(), name="update-receptor"),
    path("eliminar/receptor/<pk>", EliminarReceptor.as_view(), name="eliminar-receptor")
]
area_patterns = [
	path("crear/area/", CrearArea.as_view(), name="crear-area"),
	path("crear/area/<pk>", UpdateArea.as_view(), name="update-area")
]
aseguradora_patterns = [
	path("crear/aseguradora/", CrearAseguradora.as_view(), name="crear-aseguradora"),
	path("crear/aseguradora/<pk>", UpdateAseguradora.as_view(), name="update-aseguradora"),
    path("eliminar/aseguradora/<pk>", EliminarAseguradora.as_view(), name="eliminar-aseguradora")
]
programa_patterns = [
	path("crear/programa/", CrearPrograma.as_view(), name="crear-programa"),
	path("crear/programa/<pk>", UpdatePrograma.as_view(), name="update-programa"),
	path("crear/programa/obra/<pk>", ProgramaObra.as_view(), name="programa-obra"),
    path("eliminar/programa/<pk>", EliminarPrograma.as_view(), name="eliminar-programa")
]
agente_patterns = [
	path("crear/agente/", CrearAgente.as_view(), name="crear-agente"),
	path("crear/agente/<pk>", UpdateAgente.as_view(), name="update-agente"),
	path("crear/agente/obra/<pk>", AgenteObra.as_view(), name="agente-obra"),
    path("eliminar/agente/<pk>", EliminarAgente.as_view(), name="eliminar-agente")
]
conjunto_patterns = [
	path("crear/conjunto/", CrearConjunto.as_view(), name="crear-conjunto"),
	path("crear/conjunto/<pk>", UpdateConjunto.as_view(), name="update-conjunto"),
	path("crear/conjunto/obra/<pk>", ConjuntoObra.as_view(), name="conjunto-obra"),
    path("eliminar/conjunto/<pk>", EliminarConjunto.as_view(), name="eliminar-conjunto")
]
contrato_patterns = [
    path("crear/contrato/", CrearContrato.as_view(), name="crear-contrato"),
    path("crear/contrato/<pk>", UpdateContrato.as_view(), name="update-contrato"),
]
reporte_patterns = [
    path("reporte/crear-reporte-mes/", CrearReporteCertificadoPorMes.as_view(), name="crear-reporte-certificado"),
	path("reporte/ver-reporte-mes/", VerReporteCertificadoPorMes.as_view(), name="ver-reporte-certificado"),
    path("reporte/crear-reporte/", CrearReporteView.as_view(), name="crear-reporte"),
    path("reporte/ver-reporte/", VerReporteView.as_view(), name="ver-reporte"),
    path("reporte/lista-uvi/", CrearListaUvi.as_view(), name="crear-lista-uvi"),
]
documentos_digitales = [
    path("digitales/crear-contrato-digital/", CrearContratoDigital.as_view(), name="crear-contrato-digital"),
    path("digitales/crear-contrato-digital/<pk>", UpdateContratoDigital.as_view(), name="update-contrato-digital"),
    path("eliminar/digital/contrato/<pk>", EliminarContratoDigital.as_view(), name="eliminar-contrato-digital"),
    path("digitales/crear-resolucion-digital/", CrearResolucionDigital.as_view(), name="crear-resolucion-digital"),
    path("digitales/crear-resolucoin-digital/<pk>", UpdateResolucionDigital.as_view(), name="update-resolucion-digital"),
    path("eliminar/digital/resolucion/<pk>", EliminarResolucionDigital.as_view(), name="eliminar-resolucion-digital")
]
ajax = [
	# Obras
    path("listas/obras", PaginaListaObras, name="lista-obras"),
	path("ajax_datatable/obras/", ListaObrasView.as_view(), name="lista-obras-datatables"),
	# Certificados
	path("listas/certificados", PaginaListaCertificados, name="lista-certificados"),
	path("ajax_datatables/certificados/", ListaCertificadosView.as_view(), name="lista-certificados-datatables"),
	# Agentes
	path("listas/agentes", PaginaListaAgentes, name="lista-agentes"),
	path("ajax_datatables/agentes/", ListaAgentesView.as_view(), name="lista-agentes-datatables"),
	# Aseguradoras
	path("listas/aseguradoras", PaginaListaAseguradoras, name="lista-aseguradoras"),
	path("ajax_datatables/aseguradoras/", ListaAseguradorasView.as_view(), name="lista-aseguradoras-datatables"),
	# Conjuntos
	path("listas/conjuntos", PaginaListaConjuntos, name="lista-conjuntos"),
	path("ajax_datatables/conjuntos/", ListaConjuntosView.as_view(), name="lista-conjuntos-datatables"),
	# Empresas
	path("listas/empresas", PaginaListaEmpresas, name="lista-empresas"),
	path("ajax_datatables/empresas/", ListaEmpresasView.as_view(), name="lista-empresas-datatables"),
	# Departamentos
	path("listas/departamentos", PaginaListaDepartamentos, name="lista-departamentos"),
	path("ajax_datatables/departamentos/", ListaDepartamentosView.as_view(), name="lista-departamentos-datatables"),
	# Localidades
	path("listas/localidades", PaginaListaLocalidad, name="lista-localidades"),
	path("ajax_datatables/localidades/", ListaLocalidadesView.as_view(), name="lista-localidades-datatables"),
	# Municipios
	path("listas/municipios", PaginaListaMunicipio, name="lista-municipios"),
	path("ajax_datatables/municipios/", ListaMunicipiosView.as_view(), name="lista-municipios-datatables"),
	# Regiones
	path("listas/regiones", PaginaListaRegiones, name="lista-regiones"),
	path("ajax_datatables/regiones/", ListaRegionesView.as_view(), name="lista-regiones-datatables"),
	# Programa
	path("listas/programas", PaginaListaProgramas, name="lista-programas"),
	path("ajax_datatables/programas/", ListaProgramasView.as_view(), name="lista-programas-datatables"),
	# Polizas
	path("listas/polizas", PaginaListaPolizas, name="lista-polizas"),
	path("ajax_datatables/polizas", ListaPolizasView.as_view(), name="lista-polizas-datatables"),
	# Legacy Polizas
	path("listas/legacypolizas", PaginaListaLegacyPolizas, name="lista-legacy-polizas"),
	path("ajax_datatables/legacypolizas", ListaLegacyPolizasView.as_view(), name="lista-legacy-polizas-datatables"),
	# Obras Extendida
	path("listas/obrasextendida", PaginaListaObrasExtendida, name="lista-obras-extendida"),
	path("ajax_datatables/obrasextendida", ListaObrasExtendidaView.as_view(), name="lista-obras-extendida-datatables"),
]

urlpatterns += documentos_digitales
urlpatterns += reporte_patterns
urlpatterns += contrato_patterns
urlpatterns += ajax
urlpatterns += conjunto_patterns
urlpatterns += agente_patterns
urlpatterns += programa_patterns
urlpatterns += aseguradora_patterns
urlpatterns += area_patterns
urlpatterns += receptor_patterns
urlpatterns += municipio_patterns
urlpatterns += localidad_patterns
urlpatterns += departamento_patterns
urlpatterns += region_patterns
urlpatterns += empresa_patterns
urlpatterns += certificado_patterns
urlpatterns += poliza_patterns
urlpatterns += movimiento_patterns
urlpatterns += obra_patterns
urlpatterns += legacy_patterns
