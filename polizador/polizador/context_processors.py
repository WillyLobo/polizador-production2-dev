from carga import models
from django.db.models import Sum, F

def user_groups_processor(request):
    """ Crea un contexto con los grupos del usuario para ser usado en los templates permitiendo verificar permisos por grupo."""
    groups = []
    user = request.user
    if user.is_authenticated:
        groups = list(user.groups.values_list('name',flat = True))
    return {'groups': groups}

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
