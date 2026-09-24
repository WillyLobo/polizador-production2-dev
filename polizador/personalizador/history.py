from core.history import register
from personalizador.models import CorteLicencia, DevolucionHorasPermiso, LicenciaPermiso

register(LicenciaPermiso, children=[CorteLicencia, DevolucionHorasPermiso])
