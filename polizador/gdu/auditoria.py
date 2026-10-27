"""
Auditoría del visor del lado del servidor. El visor heredado mandaba sus eventos desde el
navegador (POST público a /log, con el usuario que decía el cliente); acá los registra la
vista que atiende el pedido, con request.user. Las acciones conservan los nombres del
historial importado de audit.audit_logs (descargaPlano, printFeature, ...).
"""
from gdu.models import EventoVisor


def _ip(request):
    reenviada = request.META.get("HTTP_X_FORWARDED_FOR")
    return reenviada.split(",")[0].strip() if reenviada else request.META.get("REMOTE_ADDR")


def registrar_evento(request, accion, metadata=None):
    usuario = request.user if request.user.is_authenticated else None
    return EventoVisor.objects.create(
        usuario=usuario,
        username=usuario.get_username() if usuario else "",
        accion=accion,
        ip=_ip(request),
        metadata=metadata,
    )
