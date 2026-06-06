# secretariador/adapters.py
from allauth.account.adapter import DefaultAccountAdapter

class InactiveSignupAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new user instance and forces their status to inactive.
        """
        # Call the base implementation to populate standard fields
        user = super().save_user(request, user, form, commit=False)
        
        # Explicitly set the user to inactive
        user.is_active = False
        
        if commit:
            user.save()
        return user