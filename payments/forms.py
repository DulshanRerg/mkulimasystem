from django import forms

class PaymentForm(forms.Form):
    """
    Form for initiating a payment.
    """
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    currency = forms.CharField(max_length=10, initial='TZS')
    payer_email = forms.EmailField()
