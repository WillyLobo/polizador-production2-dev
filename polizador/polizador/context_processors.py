from carga import models
from django.conf import settings
from django.db.models import Sum, F

def debug_mode(request):
    return {"DEBUG": settings.DEBUG}

def user_groups_processor(request):
    """ Crea un contexto con los grupos del usuario para ser usado en los templates permitiendo verificar permisos por grupo."""
    groups = []
    user = request.user
    if user.is_authenticated:
        groups = list(user.groups.values_list('name',flat = True))
    return {'groups': groups}

def imglinks(request):
    return {
        "detalleimglink" : "<i class='bi bi-search' title='Ver Detalle'></i>",
        "editimglink" : "<i class='bi bi-pencil-square' title='Editar'></i>",
        "pdfimglink" : "<i class='bi bi-filetype-pdf' title='Descargar PDF'></i>",
        "eliminarimglink" : "<i class='bi bi-trash3' title='Eliminar'></i>",
        "nofileimglink" : "<i class='bi bi-file-x' title=''></i>",
        "imprimirimglink" : "<i class='bi bi-printer' title='Imprimir'></i>",
        "agregarimglink" : "<i class='bi bi-clipboard-plus' title='Agregar'></i>",
        }
