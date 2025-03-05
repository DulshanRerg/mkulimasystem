from django import forms
from .models import Product, Review

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

class ReviewForm(forms.ModelForm):
    """
    A form for creating and updating a Review.
    This form includes fields for rating and comment.
    """
    RATING_CHOICES = [(i, f"{i} ★") for i in range(1, 6)]
    COMMENT_CHOICES = [
        ("Very Poor", "Very Poor"),
        ("Poor", "Poor"),
        ("Satisfied", "Satisfied"),
        ("Good", "Good"),
        ("Best", "Best"),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    comment = forms.ChoiceField(choices=COMMENT_CHOICES, widget=forms.Select)
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Rating',
            'comment': 'Comment',
        }