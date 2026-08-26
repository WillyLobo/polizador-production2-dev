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


def decimal_to_dms_parts(value):
    """Descompone grados decimales en (grados con signo, minutos, segundos)."""
    negative = value < 0
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
    if negative:
        deg = -deg
    return deg, minutes, seconds


def dms_parts_to_decimal(deg_raw, min_raw, sec_raw):
    try:
        deg = float(str(deg_raw).replace(",", "."))
        minutes = float(str(min_raw).replace(",", ".")) if min_raw not in (None, "") else 0.0
        seconds = float(str(sec_raw).replace(",", ".")) if sec_raw not in (None, "") else 0.0
    except ValueError:
        raise forms.ValidationError("Los grados, minutos y segundos deben ser numéricos.")
    if not (0 <= minutes < 60):
        raise forms.ValidationError("Los minutos deben estar entre 0 y 59.")
    if not (0 <= seconds < 60):
        raise forms.ValidationError("Los segundos deben estar entre 0 y 59.99.")
    negative = deg < 0 or str(deg_raw).strip().startswith("-")
    decimal = abs(deg) + minutes / 60 + seconds / 3600
    return -decimal if negative else decimal


class LatLngWidget(forms.MultiWidget):
    template_name = "widgets/latlng.html"

    def __init__(self, attrs=None):
        def field_attrs(placeholder):
            return {**(attrs or {}), "placeholder": placeholder, "type": "number", "step": "any"}

        widgets = [
            forms.NumberInput(attrs=field_attrs("Grados")),
            forms.NumberInput(attrs=field_attrs("Minutos")),
            forms.NumberInput(attrs=field_attrs("Segundos")),
            forms.NumberInput(attrs=field_attrs("Grados")),
            forms.NumberInput(attrs=field_attrs("Minutos")),
            forms.NumberInput(attrs=field_attrs("Segundos")),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value is None:
            return [None, None, None, None, None, None]
        lat_deg, lat_min, lat_sec = decimal_to_dms_parts(value.y)
        lng_deg, lng_min, lng_sec = decimal_to_dms_parts(value.x)
        return [lat_deg, lat_min, lat_sec, lng_deg, lng_min, lng_sec]


class LatLngField(forms.MultiValueField):
    widget = LatLngWidget

    def __init__(self, **kwargs):
        fields = tuple(forms.CharField(required=False) for _ in range(6))
        kwargs.setdefault("require_all_fields", False)
        super().__init__(fields=fields, **kwargs)

    def compress(self, data_list):
        if not data_list:
            return None
        lat_deg, lat_min, lat_sec, lng_deg, lng_min, lng_sec = data_list
        lat_parts = (lat_deg, lat_min, lat_sec)
        lng_parts = (lng_deg, lng_min, lng_sec)
        lat_empty = all(part in (None, "") for part in lat_parts)
        lng_empty = all(part in (None, "") for part in lng_parts)
        if lat_empty and lng_empty:
            return None
        if lat_deg in (None, "") or lng_deg in (None, ""):
            raise forms.ValidationError("Ingresá latitud y longitud.")
        lat = dms_parts_to_decimal(*lat_parts)
        lng = dms_parts_to_decimal(*lng_parts)
        if not (-90 <= lat <= 90):
            raise forms.ValidationError("La latitud debe estar entre -90° y 90°.")
        if not (-180 <= lng <= 180):
            raise forms.ValidationError("La longitud debe estar entre -180° y 180°.")
        return Point(lng, lat, srid=4326)
