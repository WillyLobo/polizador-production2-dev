from django import forms
from fallout.models import CharFallout

class PlanillaFalloutForm(forms.ModelForm):
    class Meta:
        model = CharFallout
        fields = "__all__"
