from django_select2 import forms as s2forms
from django.contrib.auth.mixins import LoginRequiredMixin

class representantetecnicoMultipleWidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "representantetecnico_nombre__icontains",
        "representantetecnico_apellido__icontains",
    ]
