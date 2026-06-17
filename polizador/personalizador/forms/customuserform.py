from django import forms
from allauth.account.forms import SignupForm
from personalizador.models import CustomUser

class CustomUserForm(SignupForm, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

        first_name = forms.CharField(max_length=150, label='Nombre')
        last_name = forms.CharField(max_length=150, label='Apellido')

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        self.first_name = self.cleaned_data['first_name']
        self.last_name = self.cleaned_data['last_name']
        user = super().save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
