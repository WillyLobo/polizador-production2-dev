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
from carga.views.conjuntoviews import *
from carga.views.reportes import *
from carga.views.contratoviews import *
from carga.views.contratotramopagoviews import *
from carga.views.documentosdigitalesviews import *
from carga.views.plandetrabajosviews import *
from carga.views.plandetrabajosrubroviews import *
from carga.views.fojademedicionviews import *
from carga.views.plandetrabajosetapaviews import *
from carga.views.ayudaviews import *
from carga.views.representantetecnicoviews import *

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
	path("crear/certificado/generar-desde-foja/<pk>", GenerarCertificadosDesdeFoja.as_view(), name="generar-certificados-foja"),
	path("crear/certificado/anticipo/", CrearCertificadoAnticipo.as_view(), name="crear-certificado-anticipo"),
	path("crear/certificado/hecho-consumado/", CrearCertificadoHechoConsumado.as_view(), name="crear-certificado-hechoconsumado"),
	path("crear/certificado/nuevo/", NuevoCertificadoMenu.as_view(), name="nuevo-certificado-menu"),
	path("crear/certificado/<pk>", UpdateCertificado.as_view(), name="update-certificado"),
	path("crear/certificado/detalle/<pk>", DetalleCertificado.as_view(), name="detalle-certificado"),
	path("crear/certificado/detalle/<pk>/imprimir", ImprimirCertificado.as_view(), name="imprimir-certificado"),
    path("eliminar/certificado/<pk>", EliminarCertificado.as_view(), name="eliminar-certificado")
]
obra_patterns = [
	path("crear/obra/", CrearObra.as_view(), name="crear-obra"),
	path("crear/obra/<pk>", UpdateObra.as_view(), name="update-obra"),
	path("crear/obra/estado/<pk>", EstadoObra.as_view(), name = "estado-obra"),
	path("crear/obra/planes-anteriores/<pk>", PlanesAnterioresObra.as_view(), name="planes-anteriores-obra"),
	path("crear/obra/contratos-anteriores/<pk>", ContratosAnterioresObra.as_view(), name="contratos-anteriores-obra"),
    path("eliminar/obra/<pk>", EliminarObra.as_view(), name="eliminar-obra"),
]
poliza_patterns = [
	path("crear/poliza/", CrearPoliza.as_view(), name="crear-poliza"),
	path("crear/poliza/<pk>", UpdatePoliza.as_view(), name="update-poliza"),
	path("crear/poliza/estado/<pk>", EstadoPoliza.as_view(), name="estado-poliza"),
    path("eliminar/poliza/<pk>", EliminarPoliza.as_view(), name="eliminar-poliza")
]
movimiento_patterns = [
	path("crear/poliza/movimiento/imprimir/<pk>", ImprimirPolizaMovimiento.as_view(), name="imprimir-poliza-movimiento"),
    path("eliminar/poliza/movimiento/<pk>", EliminarPolizaMovimiento.as_view(), name="eliminar-poliza-movimiento")
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
representantetecnico_patterns = [
	path("crear/representantetecnico/", CrearRepresentanteTecnico.as_view(), name="crear-representantetecnico"),
	path("crear/representantetecnico/<pk>", UpdateRepresentanteTecnico.as_view(), name="update-representantetecnico"),
	path("crear/representantetecnico/obra/<pk>", RepresentanteTecnicoObra.as_view(), name="representantetecnico-obra"),
    path("eliminar/representantetecnico/<pk>", EliminarRepresentanteTecnico.as_view(), name="eliminar-representantetecnico")
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
conjunto_patterns = [
	path("crear/conjunto/", CrearConjunto.as_view(), name="crear-conjunto"),
	path("crear/conjunto/<pk>", UpdateConjunto.as_view(), name="update-conjunto"),
	path("crear/conjunto/obra/<pk>", ConjuntoObra.as_view(), name="conjunto-obra"),
    path("eliminar/conjunto/<pk>", EliminarConjunto.as_view(), name="eliminar-conjunto")
]
contrato_patterns = [
    path("crear/contrato/", CrearContrato.as_view(), name="crear-contrato"),
    path("crear/contrato/<pk>", UpdateContrato.as_view(), name="update-contrato"),
    path("crear/contrato/<pk>/tramos/", GestionarTramosContrato.as_view(), name="gestionar-tramos-contrato"),
]
plandetrabajos_patterns = [
    path("crear/plandetrabajos/", CrearPlanDeTrabajos.as_view(), name="crear-plandetrabajos"),
    path("crear/plandetrabajos/<pk>", UpdatePlanDeTrabajos.as_view(), name="update-plandetrabajos"),
]
plandetrabajosrubro_patterns = [
    path("crear/plandetrabajosrubro/", CrearPlanDeTrabajosRubro.as_view(), name="crear-plandetrabajosrubro"),
    path("crear/plandetrabajosrubro/<pk>", UpdatePlanDeTrabajosRubro.as_view(), name="update-plandetrabajosrubro"),
]
fojademedicion_patterns = [
    path("crear/foja-medicion/", CrearFojaDeMedicion.as_view(), name="crear-fojademedicion"),
    path("crear/foja-medicion/<pk>", UpdateFojaDeMedicion.as_view(), name="update-fojademedicion"),
    path("foja-medicion/<pk>/detalle/", DetalleFojaDeMedicion.as_view(), name="detalle-fojademedicion"),
    path("foja-medicion/<pk>/imprimir/", ImprimirFojaDeMedicion.as_view(), name="imprimir-fojademedicion"),
]
plandetrabajosetapa_patterns = [
    path("crear/plandetrabajosetapa/<int:pk>/", PlanDeTrabajosEtapaMatriz.as_view(), name="plandetrabajosetapa-matriz"),
]
ayuda_patterns = [
    path("ayuda/plan-de-trabajos-fojas/", ManualObraPlanFojaView.as_view(), name="ayuda-plan-fojas"),
    path("ayuda/certificados/", ManualCertificadosView.as_view(), name="ayuda-certificados"),
]
reporte_patterns = [
    path("reporte/crear-reporte-mes/", ReporteCertificadoPorMesView.as_view(), name="crear-reporte-certificado"),
    path("reporte/crear-reporte-obra/", CrearReporteObraView.as_view(), name="crear-reporte-obra"),
    path("reporte/lista-uvi/", CrearListaUvi.as_view(), name="crear-lista-uvi"),
    path("reporte/refresh_uvi", refresh_uvi_from_bcra, name="refresh-uvi-from-bcra"),
]
documentos_digitales = [
    path("digitales/crear-contrato-digital/", CrearContratoDigital.as_view(), name="crear-contrato-digital"),
    path("digitales/crear-contrato-digital/<pk>", UpdateContratoDigital.as_view(), name="update-contrato-digital"),
    path("eliminar/digital/contrato/<pk>", EliminarContratoDigital.as_view(), name="eliminar-contrato-digital"),
    path("digitales/crear-resolucion-digital/", CrearResolucionDigital.as_view(), name="crear-resolucion-digital"),
    path("digitales/crear-resolucion-digital/<pk>", UpdateResolucionDigital.as_view(), name="update-resolucion-digital"),
    path("eliminar/digital/resolucion/<pk>", EliminarResolucionDigital.as_view(), name="eliminar-resolucion-digital")
]
ajax = [
	# Obras
    path("listas/obras", PaginaListaObras, name="lista-obras"),
	# Certificados
	path("listas/certificados", PaginaListaCertificados, name="lista-certificados"),
	# Aseguradoras
	path("listas/aseguradoras", PaginaListaAseguradoras, name="lista-aseguradoras"),
	# Conjuntos
	path("listas/conjuntos", PaginaListaConjuntos, name="lista-conjuntos"),
	# Empresas
	path("listas/empresas", PaginaListaEmpresas, name="lista-empresas"),
	# Departamentos
	path("listas/departamentos", PaginaListaDepartamentos, name="lista-departamentos"),
	# Representantes Técnicos
	path("listas/representantetecnicos", PaginaListaRepresentantesTecnicos, name="lista-representantetecnicos"),
	# Localidades
	path("listas/localidades", PaginaListaLocalidad, name="lista-localidades"),
	# Municipios
	path("listas/municipios", PaginaListaMunicipio, name="lista-municipios"),
	# Regiones
	path("listas/regiones", PaginaListaRegiones, name="lista-regiones"),
	# Programa
	path("listas/programas", PaginaListaProgramas, name="lista-programas"),
	# Polizas
	path("listas/polizas", PaginaListaPolizas, name="lista-polizas"),
	# Legacy Polizas
	# path("listas/legacypolizas", PaginaListaLegacyPolizas, name="lista-legacy-polizas"),
	# path("ajax_datatables/legacypolizas", ListaLegacyPolizasView.as_view(), name="lista-legacy-polizas-datatables"),
	# Obras Extendida
	path("listas/obrasextendida", PaginaListaObrasExtendida, name="lista-obras-extendida"),
]

urlpatterns += documentos_digitales
urlpatterns += reporte_patterns
urlpatterns += contrato_patterns
urlpatterns += plandetrabajos_patterns
urlpatterns += plandetrabajosrubro_patterns
urlpatterns += fojademedicion_patterns
urlpatterns += plandetrabajosetapa_patterns
urlpatterns += ayuda_patterns
urlpatterns += ajax
urlpatterns += conjunto_patterns
urlpatterns += programa_patterns
urlpatterns += aseguradora_patterns
urlpatterns += area_patterns
urlpatterns += representantetecnico_patterns
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