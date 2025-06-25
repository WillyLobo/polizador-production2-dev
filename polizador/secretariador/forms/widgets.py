from django.forms.widgets import TextInput, DateTimeBaseInput
from django.utils import formats

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
