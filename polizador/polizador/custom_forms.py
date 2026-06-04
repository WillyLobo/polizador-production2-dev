# widgets.py or forms.py
from django import forms
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
