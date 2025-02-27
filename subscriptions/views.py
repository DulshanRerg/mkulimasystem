from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm
from django.utils import timezone
from datetime import timedelta
from .models import Subscription

@login_required
def subscribe(request):
    """
    Allows a user to subscribe. Sets expiry 30 days from now.
    """
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.expiry_date = timezone.now() + timedelta(days=30)
            subscription.save()
            return redirect('subscriptions:status')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/subscription_form.html', {'form': form})

@login_required
def subscription_status(request):
    """
    Displays the user's current subscription status.
    """
    subscription = getattr(request.user, 'subscription', None)
    return render(request, 'subscriptions/subscription_status.html', {'subscription': subscription})
