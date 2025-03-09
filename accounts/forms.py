from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','middle_name', 'last_name','role','username', 'email', 'password1', 'password2', 'profile_picture', 'phone_number', 'location']
        labels = {
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'last_name': 'Last Name',
            'role': 'Sign up as',
            'username': 'Username',
            'email': 'Email (optional)',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'profile_picture': 'Profile Picture',
            'phone_number': 'Phone Number',
            'location': 'Location',
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters and digits only.',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'e.g., dulshan0002'}),
        }

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'phone_number', 'location', 'bio']

    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', None)  # ✅ Extract user role
        super().__init__(*args, **kwargs)  # ✅ Initialize form without `user_role`

        #  Remove irrelevant fields based on user role
        # if user_role == 'farmer':
        #     self.fields.pop('favorite_crops', None)
        # elif user_role == 'buyer':
        #     self.fields.pop('farm_size', None)
        #     self.fields.pop('crops_grown', None)