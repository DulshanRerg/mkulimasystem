from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from django.urls import reverse

class Product(models.Model):
    """
    Model representing a crop/product listing.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    location = models.CharField(max_length=255)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=255, default='Other')
    quantity = models.IntegerField( default=1)
    sold = models.BooleanField(default=False)
    sold_at = models.DateTimeField(blank=True, null=True, default=None)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases', blank=True, null=True)
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Buyer
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    has_paid = models.BooleanField(default=False)  # Track Payment Statu

    def __str__(self):
        return f"{self.user.username} - {self.rating}⭐ for {self.product.name}"
