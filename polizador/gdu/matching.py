import re

_SIN_DATOS_RE = re.compile(r"^\s*sin\s+datos\s*$", re.IGNORECASE)
_ESPACIOS_RE = re.compile(r"\s+")


def normalizar_expediente(texto):
    """Mayúsculas, espacios colapsados, sin bordes. 'SIN DATOS' (con variantes de
    espaciado/mayúsculas) y vacío -> None: son placeholders de dato faltante en
    catastro, no valen como clave de matching."""
    if not texto:
        return None
    texto = _ESPACIOS_RE.sub(" ", texto.strip()).upper()
    if not texto or _SIN_DATOS_RE.match(texto):
        return None
    return texto
