from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """
    list_display = ('title', 'price', 'location', 'user', 'created_at')
    search_fields = ('title', 'description', 'location')
    list_filter = ('location', 'created_at')
    