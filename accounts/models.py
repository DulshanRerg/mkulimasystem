from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class User(AbstractUser):
    """
    Custom User model for the Mkulima App.
    
    Attributes:
        role (str): The role of the user, with choices defined in ROLE_CHOICES.
            - 'farmer': For users who can post crop listings.
            - 'buyer': For users who browse and interact with crop listings.
            - 'admin': For users with administrative privileges.
    """
    FARMER = 'farmer'
    BUYER = 'buyer'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (FARMER, 'Farmer'),
        (BUYER, 'Buyer'),
        (ADMIN, 'Admin'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Username must be alphanumeric.',
            code='invalid_username'
        )]
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
    email = models.EmailField(unique=True, blank=True, null=True)

    def is_farmer(self):
        """Return True if the user is a farmer."""
        return self.role == self.FARMER

    def is_buyer(self):
        """Return True if the user is a buyer."""
        return self.role == self.BUYER

    def is_admin(self):
        """Return True if the user is an admin."""
        return self.role == self.ADMIN

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def get_avatar_url(self):
        if self.image:
            return self.image.url
        return "/static/images/user-placeholder.png"