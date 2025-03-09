from django.db import models
from accounts.models import User
from products.models import Product
from django.conf import settings

class Transaction(models.Model):
    """
    Represents a payment transaction.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=0)  # Track which product was purchased
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='TZS')
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, success, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transaction_id} - {self.product.name} - {self.amount} {self.currency} - {self.user.username} - {self.status}'
