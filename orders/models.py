from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('completed', 'Completed'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="farmer_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    external_id = models.CharField(max_length=128, unique=True)  # Unique transaction ID for payments
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.external_id} - {self.status}"
