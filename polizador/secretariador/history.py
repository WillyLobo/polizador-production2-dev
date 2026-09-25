from core.history import register
from secretariador.models import ComisionadoSolicitud, Incorporacion, Solicitud

register(Solicitud, children=[ComisionadoSolicitud, Incorporacion])
register(Incorporacion, children=[ComisionadoSolicitud])
