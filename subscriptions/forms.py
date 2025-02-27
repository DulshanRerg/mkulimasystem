from django import forms
from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    """
    Form for creating or updating a subscription.
    """
    class Meta:
        model = Subscription
        fields = ['plan_name']
        labels = {
            'plan_name': 'Plan Name',
        }