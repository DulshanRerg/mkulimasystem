from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form for the Mkulima App.
    
    This form extends Django's UserCreationForm to incorporate the custom user model,
    including additional fields like email and role.
    """
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        # Include all necessary fields for user registration
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def save(self, commit=True):
        # Save the new user instance, ensuring that email and role are set properly
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
