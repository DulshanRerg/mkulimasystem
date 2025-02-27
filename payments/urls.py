from django.urls import path
from .views import PaymentInitiateView, PaymentCallbackView

app_name = 'payments'

urlpatterns = [
    path('initiate/', PaymentInitiateView.as_view(), name='initiate'),
    path('callback/', PaymentCallbackView.as_view(), name='callback'),
]
