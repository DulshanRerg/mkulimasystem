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
    first_name = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
    email = models.EmailField(unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default-pics.png')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Farmer-specific fields
    farm_size = models.CharField(max_length=50, blank=True, null=True)
    crops_grown = models.TextField(blank=True, null=True)
    # Buyer-specific fields
    favorite_crops = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    
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
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def get_avatar_url(self):
        if self.image:
            return self.image.url
        return "/static/media/profile_pics/default-pics.png"