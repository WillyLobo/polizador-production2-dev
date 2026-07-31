from django.urls import path

from gdu.views import api3450, audit, csv_export, encuesta, listados, print_pdf, smb, uf, vincular_obra, visor

app_name = "gdu"

urlpatterns = [
    path("relevamientos/", encuesta.relevamientos_list, name="relevamientos_list"),
    path("relevamientos/<int:relevamiento_id>/viviendas/", encuesta.relevamiento_viviendas, name="relevamiento_viviendas"),
    path("relevamientos/<int:relevamiento_id>/viviendas/<int:vivienda_id>/encuesta/", encuesta.encuesta_form, name="encuesta_form"),

    path("log/", audit.post_log, name="post_log"),
    path("planos/", smb.plano, name="plano"),
    path("csv/", csv_export.exportar_csv, name="exportar_csv"),
    path("3450/", api3450.consultar_3450, name="consultar_3450"),
    path("print/", print_pdf.imprimir, name="imprimir"),
    path("uf/<int:uf_id>/nro-adjudicatario/", uf.actualizar_nro_adjudicatario, name="actualizar_nro_adjudicatario"),

    path("mapa/", visor.mapa, name="mapa"),
    path("mapa/viviendas.geojson", visor.geojson_viviendas, name="geojson_viviendas"),
    path("mapa/barrios.geojson", visor.geojson_barrios, name="geojson_barrios"),

    path("contrataciones/<int:contratacion_id>/vincular-obra/", vincular_obra.vincular_obra, name="vincular_obra"),

    path("listas/actuaciones/", listados.lista_actuaciones, name="lista_actuaciones"),
    path("listas/contrataciones/", listados.lista_contrataciones, name="lista_contrataciones"),
    path("listas/contrataciones-sin-obra/", listados.lista_contrataciones_sin_obra, name="lista_contrataciones_sin_obra"),
    path("listas/intervenciones/", listados.lista_intervenciones, name="lista_intervenciones"),
    path("listas/programas/", listados.lista_programas, name="lista_programas"),
    path("listas/barrios/", listados.lista_barrios, name="lista_barrios"),
    path("listas/parcelas/", listados.lista_parcelas, name="lista_parcelas"),
    path("listas/ufs/", listados.lista_ufs, name="lista_ufs"),
    path("listas/localidades/", listados.lista_localidades, name="lista_localidades"),
    path("listas/expropiaciones/", listados.lista_expropiaciones, name="lista_expropiaciones"),
    path("listas/planos-mensura/", listados.lista_planos_mensura, name="lista_planos_mensura"),
    path("listas/adjudicaciones-beneficiario/", listados.lista_adjudicaciones_beneficiario, name="lista_adjudicaciones_beneficiario"),
    path("listas/resoluciones-costos/", listados.lista_resoluciones_costos, name="lista_resoluciones_costos"),
    path("listas/tipos-contratacion/", listados.lista_tipos_contratacion, name="lista_tipos_contratacion"),
    path("listas/tipos-estado/", listados.lista_tipos_estado, name="lista_tipos_estado"),
    path("listas/tipos-intervencion/", listados.lista_tipos_intervencion, name="lista_tipos_intervencion"),
    path("listas/tipos-uf/", listados.lista_tipos_uf, name="lista_tipos_uf"),
    path("listas/destinos-parcela/", listados.lista_destinos_parcela, name="lista_destinos_parcela"),
    path("listas/estados-gestion-expropiacion/", listados.lista_estados_gestion_expropiacion, name="lista_estados_gestion_expropiacion"),
    path("listas/adjudicatarios-3450/", listados.lista_adjudicatarios_3450, name="lista_adjudicatarios_3450"),
]
