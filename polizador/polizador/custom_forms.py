# widgets.py or forms.py
import re
from django import forms
from django.contrib.gis.geos import Point
from django.forms.widgets import DateTimeBaseInput
from django.utils import formats


class CustomCheckboxInput(forms.CheckboxInput):
    template_name = 'widgets/custom_checkbox.html'

class DateHTMLWidget(DateTimeBaseInput):
    supports_microseconds = False
    template_name = "django/forms/widgets/date.html"

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs)
        self.format = format or None

    def format_value(self, value):
        return formats.localize_input(
            value, formats.get_format("%Y-%m-%d")
        )

# Acepta grados/minutos/segundos, ej: 27°20'48.41"S, o directamente decimal: -27.3468
DMS_RE = re.compile(
    r"""^\s*
    (?P<deg>-?\d+(?:\.\d+)?)\s*(?:°|d)?\s*
    (?:
        (?P<min>\d+(?:\.\d+)?)\s*(?:'|′|m)?\s*
        (?:
            (?P<sec>\d+(?:\.\d+)?)\s*(?:"|″|s)?\s*
        )?
    )?
    (?P<hem>[NSEWO])?\s*$""",
    re.VERBOSE | re.IGNORECASE,
)


def parse_dms(value):
    """Convierte una coordenada en formato grados/minutos/segundos (o decimal) a grados decimales."""
    if value in (None, ""):
        return None
    match = DMS_RE.match(str(value))
    if not match:
        raise forms.ValidationError(
            "Formato de coordenada inválido. Usá grados/minutos/segundos, ej: 27°20'48.41\"S"
        )
    deg = float(match.group("deg"))
    negative = deg < 0
    minutes = float(match.group("min") or 0)
    seconds = float(match.group("sec") or 0)
    decimal = abs(deg) + minutes / 60 + seconds / 3600
    hem = (match.group("hem") or "").upper()
    if hem in ("S", "W", "O") or (not hem and negative):
        decimal = -decimal
    return decimal


def decimal_to_dms(value, hemispheres):
    positive, negative = hemispheres
    hem = positive if value >= 0 else negative
    value = abs(value)
    deg = int(value)
    minutes_full = (value - deg) * 60
    minutes = int(minutes_full)
    seconds = round((minutes_full - minutes) * 60, 2)
    if seconds >= 60:
        seconds -= 60
        minutes += 1
    if minutes >= 60:
        minutes -= 60
        deg += 1
    return f"""{deg}°{minutes}'{seconds:.2f}"{hem}"""


class LatLngWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs={**(attrs or {}), "placeholder": """Ejemplo: 27°20'48.41"S"""}),
            forms.TextInput(attrs={**(attrs or {}), "placeholder": """Ejemplo: 59°3'0.00"O"""}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value is None:
            return [None, None]
        return [
            decimal_to_dms(value.y, ("N", "S")),
            decimal_to_dms(value.x, ("E", "O")),
        ]

class LatLngField(forms.MultiValueField):
    widget = LatLngWidget

    def __init__(self, **kwargs):
        fields = (
            forms.CharField(required=False),
            forms.CharField(required=False),
        )
        kwargs.setdefault("require_all_fields", False)
        super().__init__(fields=fields, **kwargs)

    def compress(self, data_list):
        if not data_list:
            return None
        lat_raw, lng_raw = data_list
        if not lat_raw and not lng_raw:
            return None
        if not lat_raw or not lng_raw:
            raise forms.ValidationError("Ingresá latitud y longitud.")
        lat = parse_dms(lat_raw)
        lng = parse_dms(lng_raw)
        if not (-90 <= lat <= 90):
            raise forms.ValidationError("La latitud debe estar entre -90° y 90°.")
        if not (-180 <= lng <= 180):
            raise forms.ValidationError("La longitud debe estar entre -180° y 180°.")
        return Point(lng, lat, srid=4326)
