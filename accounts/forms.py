from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['role','username', 'email', 'password1', 'password2']
        labels = {
            'role': 'Sign up as',
            'username': 'Username',
            'email': 'Email (optional)',
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters and digits only.',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'e.g., dulshan0002'}),
        }
