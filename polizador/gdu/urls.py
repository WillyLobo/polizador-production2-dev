from django.urls import path

from gdu.views import api3450, audit, csv_export, encuesta, print_pdf, smb, uf, visor

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
]
