from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """
    A form for creating and updating a Product.
    This form includes fields for title, description, price, image, and location.
    """
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'location']
        labels = {
            'title': 'Product Name',
            'description': 'Description',
            'price': 'Price (Tsh)',
            'image': 'Image',
            'location': 'Location',
        }