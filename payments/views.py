from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .services import AzamPayService
from .models import Transaction
import uuid

class PaymentInitiateView(View):
    """
    Initiates a payment via AzamPay.
    """
    def get(self, request):
        form = PaymentForm()
        return render(request, 'payments/payment_form.html', {'form': form})

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            currency = form.cleaned_data['currency']
            payer_email = form.cleaned_data['payer_email']
            external_id = str(uuid.uuid4())
            callback_url = request.build_absolute_uri(reverse('payments:callback'))

            azampay = AzamPayService()
            payment_response = azampay.initiate_payment(amount, currency, external_id, payer_email, callback_url)

            Transaction.objects.create(
                user=request.user,
                amount=amount,
                currency=currency,
                transaction_id=external_id,
                status=payment_response.get('status', 'pending')
            )

            if payment_response.get('status') == 'success':
                return redirect(payment_response.get('paymentUrl'))
            else:
                return render(request, 'payments/payment_failure.html', {'error': payment_response.get('error')})
        return render(request, 'payments/payment_form.html', {'form': form})

class PaymentCallbackView(View):
    """
    Handles the callback from AzamPay after a payment.
    """
    def get(self, request):
        # Process the callback data here and update the transaction status as needed.
        return render(request, 'payments/payment_success.html')
