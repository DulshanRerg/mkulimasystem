from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """
    list_display = ('name', 'price', 'location', 'farmer', 'created_at', 'updated_at', 'sold', 'sold_at', 'buyer', 'category', 'quantity')
    search_fields = ('name', 'description', 'location', 'farmer__username', 'category')
    list_filter = ('location', 'created_at')
    