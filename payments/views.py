from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from products.models import Product, Review
from .forms import PaymentForm
from .services import PaymentGatewayService
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

            azampay = PaymentGatewayService()
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
    Handles the callback from AzamPay and updates payment status.
    """
    def get(self, request):
        transaction_id = request.GET.get('transaction_id')
        status = request.GET.get('status')  # Expected values: "success", "failed", "pending"

        #  Find the transaction and update its status
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        transaction.status = status
        transaction.save()

        # Mark the review as paid if payment is successful
        if status == "success":
            transaction.product.review.paid = True
            transaction.product.review.save()
            return render(request, 'payments/payment_success.html')

        return render(request, 'payments/payment_failure.html', {'error': "Payment failed."})

@login_required
def process_payment(request, pk):
    """
    Processes the payment after the buyer submits a rating.
    """
    product = get_object_or_404(Product, pk=pk)
    user_review = get_object_or_404(Review, user=request.user, product=product)

    # Ensure user has already rated before proceeding with payment
    if not user_review:
        return redirect('products:product_detail', pk=pk)

    if request.method == "POST":
        amount = product.price  # Payment amount is the product price
        currency = "TZS"  # Assuming Tanzanian Shillings
        payer_email = request.user.email
        external_id = str(uuid.uuid4())  # Unique transaction ID
        callback_url = request.build_absolute_uri(reverse('payments:callback'))

        #  Initiate payment via AzamPay
        azampay = PaymentGatewayService()
        payment_response = azampay.initiate_payment(amount, currency, external_id, payer_email, callback_url)

        #  Store transaction details in the database
        transaction = Transaction.objects.create(
            user=request.user,
            product=product,
            amount=amount,
            currency=currency,
            transaction_id=external_id,
            status=payment_response.get('status', 'pending')
        )

        # Redirect to payment gateway if successful
        if payment_response.get('status') == 'success':
            return redirect(payment_response.get('paymentUrl'))
        else:
            return render(request, 'payments/payment_failure.html', {'error': payment_response.get('error')})

    return render(request, 'payments/payment_form.html', {'product': product})

