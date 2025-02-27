from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Subscription(models.Model):
    """
    Represents a user subscription.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan_name = models.CharField(max_length=50)  # e.g., 'basic', 'premium'
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def is_active(self):
        """
        Returns True if the subscription is active.
        """
        return self.expiry_date > timezone.now()

    def __str__(self):
        return f'{self.user.username} - {self.plan_name}'
