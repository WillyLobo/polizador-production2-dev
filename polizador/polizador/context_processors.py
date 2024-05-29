from carga import models
from django.db.models import Sum, F

def obra_por_programa(request):
    """
    Ver ésta cosa asquerosa... porque el context processor significa hacer el 
    pedido de programas por obra cada vez que hay un reload de pagina.
    """
    programa = models.Obra.objects.values_list("obra_programa", flat=True).distinct()
    lista_url_programa = ()
    for url in programa:
        obj = models.Programa.objects.get(pk=url).get_absolute_url()
        lista_url_programa += (obj,)
    return {
        "lista_url" : lista_url_programa
    }

def imglinks(request):
    return {
        "detalleimglink" : "<img class='img-small' src='/static/images/search.svg' title='Ver Detalle'/>",
        "editimglink" : "<img class='img-small' src='/static/images/pencil-square.svg' title='Editar' />",
        "pdfimglink" : "<img class='img-small' src='/static/images/filetype-pdf.svg' title='Descargar PDF' />",
        "eliminarimglink" : "<img class='img-small' src='/static/images/trash3.svg' title='Eliminar' />",
        "nofileimglink" : "<img class='img-small' src='/static/images/file-x.svg' title='' />",
        "imprimirimglink" : "<img class='img-small' src='/static/images/printer.svg' title='Imprimir' />",
        "agregarimglink" : "<img src='/static/images/clipboard-plus.svg' title='Agregar' width='30' heigth='30' />",
        }
