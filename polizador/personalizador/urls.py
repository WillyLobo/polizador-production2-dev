from django.urls import path

from personalizador.views.generoagenteviews import *
from personalizador.views.tituloprofesionalviews import *
from personalizador.views.categoriaviews import *
from personalizador.views.denominacioncargoviews import *
from personalizador.views.apartadocargoviews import *
from personalizador.views.ceicviews import *
from personalizador.views.grupocargoviews import *
from personalizador.views.actividadespecificaviews import *
from personalizador.views.cargotipoviews import *
from personalizador.views.directorioviews import *
from personalizador.views.gerenciaviews import *
from personalizador.views.direccionviews import *
from personalizador.views.departamentoviews import *
from personalizador.views.oficinaviews import *
from personalizador.views.agenteviews import *
from personalizador.views.licenciapermisoviews import *
from personalizador.views.cortelicenciaviews import *
from personalizador.views.tipolicenciapermisoviews import *

app_name = "personalizador"

urlpatterns = [
]

generoagente_patterns = [
	path("crear/generoagente/", CrearGeneroAgente.as_view(), name="crear-generoagente"),
	path("crear/generoagente/<pk>", UpdateGeneroAgente.as_view(), name="update-generoagente"),
	path("eliminar/generoagente/<pk>", EliminarGeneroAgente.as_view(), name="eliminar-generoagente"),
]
tituloprofesional_patterns = [
	path("crear/tituloprofesional/", CrearTituloProfesional.as_view(), name="crear-tituloprofesional"),
	path("crear/tituloprofesional/<pk>", UpdateTituloProfesional.as_view(), name="update-tituloprofesional"),
	path("eliminar/tituloprofesional/<pk>", EliminarTituloProfesional.as_view(), name="eliminar-tituloprofesional"),
]
categoria_patterns = [
	path("crear/categoria/", CrearCategoria.as_view(), name="crear-categoria"),
	path("crear/categoria/<pk>", UpdateCategoria.as_view(), name="update-categoria"),
	path("eliminar/categoria/<pk>", EliminarCategoria.as_view(), name="eliminar-categoria"),
]
denominacioncargo_patterns = [
	path("crear/denominacioncargo/", CrearDenominacionCargo.as_view(), name="crear-denominacioncargo"),
	path("crear/denominacioncargo/<pk>", UpdateDenominacionCargo.as_view(), name="update-denominacioncargo"),
	path("eliminar/denominacioncargo/<pk>", EliminarDenominacionCargo.as_view(), name="eliminar-denominacioncargo"),
]
apartadocargo_patterns = [
	path("crear/apartadocargo/", CrearApartadoCargo.as_view(), name="crear-apartadocargo"),
	path("crear/apartadocargo/<pk>", UpdateApartadoCargo.as_view(), name="update-apartadocargo"),
	path("eliminar/apartadocargo/<pk>", EliminarApartadoCargo.as_view(), name="eliminar-apartadocargo"),
]
ceic_patterns = [
	path("crear/ceic/", CrearCEIC.as_view(), name="crear-ceic"),
	path("crear/ceic/<pk>", UpdateCEIC.as_view(), name="update-ceic"),
	path("eliminar/ceic/<pk>", EliminarCEIC.as_view(), name="eliminar-ceic"),
]
grupocargo_patterns = [
	path("crear/grupocargo/", CrearGrupoCargo.as_view(), name="crear-grupocargo"),
	path("crear/grupocargo/<pk>", UpdateGrupoCargo.as_view(), name="update-grupocargo"),
	path("eliminar/grupocargo/<pk>", EliminarGrupoCargo.as_view(), name="eliminar-grupocargo"),
]
actividadespecifica_patterns = [
	path("crear/actividadespecifica/", CrearActividadEspecifica.as_view(), name="crear-actividadespecifica"),
	path("crear/actividadespecifica/<pk>", UpdateActividadEspecifica.as_view(), name="update-actividadespecifica"),
	path("eliminar/actividadespecifica/<pk>", EliminarActividadEspecifica.as_view(), name="eliminar-actividadespecifica"),
]
cargotipo_patterns = [
	path("crear/cargotipo/", CrearCargoTipo.as_view(), name="crear-cargotipo"),
	path("crear/cargotipo/<pk>", UpdateCargoTipo.as_view(), name="update-cargotipo"),
	path("eliminar/cargotipo/<pk>", EliminarCargoTipo.as_view(), name="eliminar-cargotipo"),
]
directorio_patterns = [
	path("crear/directorio/", CrearDirectorio.as_view(), name="crear-directorio"),
	path("crear/directorio/<pk>", UpdateDirectorio.as_view(), name="update-directorio"),
	path("eliminar/directorio/<pk>", EliminarDirectorio.as_view(), name="eliminar-directorio"),
]
gerencia_patterns = [
	path("crear/gerencia/", CrearGerencia.as_view(), name="crear-gerencia"),
	path("crear/gerencia/<pk>", UpdateGerencia.as_view(), name="update-gerencia"),
	path("eliminar/gerencia/<pk>", EliminarGerencia.as_view(), name="eliminar-gerencia"),
]
direccion_patterns = [
	path("crear/direccion/", CrearDireccion.as_view(), name="crear-direccion"),
	path("crear/direccion/<pk>", UpdateDireccion.as_view(), name="update-direccion"),
	path("eliminar/direccion/<pk>", EliminarDireccion.as_view(), name="eliminar-direccion"),
]
departamento_patterns = [
	path("crear/departamento/", CrearDepartamento.as_view(), name="crear-departamento"),
	path("crear/departamento/<pk>", UpdateDepartamento.as_view(), name="update-departamento"),
	path("eliminar/departamento/<pk>", EliminarDepartamento.as_view(), name="eliminar-departamento"),
]
oficina_patterns = [
	path("crear/oficina/", CrearOficina.as_view(), name="crear-oficina"),
	path("crear/oficina/<pk>", UpdateOficina.as_view(), name="update-oficina"),
	path("eliminar/oficina/<pk>", EliminarOficina.as_view(), name="eliminar-oficina"),
]
agente_patterns = [
	path("crear/agente/", CrearAgente.as_view(), name="crear-agente"),
	path("crear/agente/<pk>", UpdateAgente.as_view(), name="update-agente"),
	path("eliminar/agente/<pk>", EliminarAgente.as_view(), name="eliminar-agente"),
	path("agente/ficha/<pk>", FichaAgente.as_view(), name="ficha-agente"),
]
licenciapermiso_patterns = [
	path("licencias/crear/", CrearLicenciaPermiso.as_view(), name="crear-licenciapermiso"),
	path("licencias/crear/<pk>", UpdateLicenciaPermiso.as_view(), name="update-licenciapermiso"),
	path("licencias/eliminar/<pk>", EliminarLicenciaPermiso.as_view(), name="eliminar-licenciapermiso"),
	path("licencias/ver/<pk>", VerLicenciaPermiso.as_view(), name="ver-licenciapermiso"),
	path("licencias/control/agente/<pk>", ControlLicenciasAgente, name="control-licencias-agente"),
]
cortelicencia_patterns = [
	path("licencias/<licenciapermiso_pk>/corte/crear/", CrearCorteLicencia.as_view(), name="crear-cortelicencia"),
	path("licencias/corte/<pk>", UpdateCorteLicencia.as_view(), name="update-cortelicencia"),
	path("licencias/corte/eliminar/<pk>", EliminarCorteLicencia.as_view(), name="eliminar-cortelicencia"),
]
tipolicenciapermiso_patterns = [
	path("crear/tipolicenciapermiso/", CrearTipoLicenciaPermiso.as_view(), name="crear-tipolicenciapermiso"),
	path("crear/tipolicenciapermiso/<pk>", UpdateTipoLicenciaPermiso.as_view(), name="update-tipolicenciapermiso"),
	path("eliminar/tipolicenciapermiso/<pk>", EliminarTipoLicenciaPermiso.as_view(), name="eliminar-tipolicenciapermiso"),
]

ajax = [
	path("listas/generoagentes", PaginaListaGeneroAgentes, name="lista-generoagentes"),
	path("listas/tituloprofesionales", PaginaListaTituloProfesionales, name="lista-tituloprofesionales"),
	path("listas/categorias", PaginaListaCategorias, name="lista-categorias"),
	path("listas/denominacioncargos", PaginaListaDenominacionCargos, name="lista-denominacioncargos"),
	path("listas/apartadocargos", PaginaListaApartadoCargos, name="lista-apartadocargos"),
	path("listas/ceics", PaginaListaCEICs, name="lista-ceics"),
	path("listas/grupocargos", PaginaListaGrupoCargos, name="lista-grupocargos"),
	path("listas/actividadespecificas", PaginaListaActividadEspecificas, name="lista-actividadespecificas"),
	path("listas/cargotipos", PaginaListaCargoTipos, name="lista-cargotipos"),
	path("listas/directorios", PaginaListaDirectorios, name="lista-directorios"),
	path("listas/gerencias", PaginaListaGerencias, name="lista-gerencias"),
	path("listas/direcciones", PaginaListaDirecciones, name="lista-direcciones"),
	path("listas/departamentos", PaginaListaDepartamentos, name="lista-departamentos"),
	path("listas/oficinas", PaginaListaOficinas, name="lista-oficinas"),
	path("listas/agentes", PaginaListaAgentes, name="lista-agentes"),
	path("listas/licenciapermisos", PaginaListaLicenciaPermisos, name="lista-licenciapermisos"),
	path("listas/tipolicenciapermisos", PaginaListaTipoLicenciaPermisos, name="lista-tipolicenciapermisos"),
]

urlpatterns += ajax
urlpatterns += generoagente_patterns
urlpatterns += tituloprofesional_patterns
urlpatterns += categoria_patterns
urlpatterns += denominacioncargo_patterns
urlpatterns += apartadocargo_patterns
urlpatterns += ceic_patterns
urlpatterns += grupocargo_patterns
urlpatterns += actividadespecifica_patterns
urlpatterns += cargotipo_patterns
urlpatterns += directorio_patterns
urlpatterns += gerencia_patterns
urlpatterns += direccion_patterns
urlpatterns += departamento_patterns
urlpatterns += oficina_patterns
urlpatterns += agente_patterns
urlpatterns += licenciapermiso_patterns
urlpatterns += cortelicencia_patterns
urlpatterns += tipolicenciapermiso_patterns
