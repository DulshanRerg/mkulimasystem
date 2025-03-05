from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """
    A form for creating and updating a Product.
    This form includes fields for title, description, price, image, and location.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'location', 'category', 'quantity', 'sold', 'sold_at', 'buyer']
        labels = {
            'title': 'Product Name',
            'description': 'Description',
            'price': 'Price (Tsh)',
            'image': 'Image',
            'location': 'Location',
        }