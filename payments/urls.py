from django.urls import path
from .views import PaymentInitiateView, PaymentCallbackView, process_payment

app_name = 'payments'

urlpatterns = [
    path('<int:product_id>/', process_payment, name='process_payment'),
    path('initiate/', PaymentInitiateView.as_view(), name='initiate'),
    path('callback/', PaymentCallbackView.as_view(), name='callback'),
    # path('success/', PaymentCallbackView.as_view(), name='success'),
    # path('failure/', PaymentCallbackView.as_view(), name='failure'),
    # path('cancel/', PaymentCallbackView.as_view(), name='cancel'),
    # path('ipn/', PaymentCallbackView.as_view(), name='ipn'),
    # path('webhook/', PaymentCallbackView.as_view(), name='webhook'),
    # path('webhook/success/', PaymentCallbackView.as_view(), name='webhook_success'),
    # path('webhook/failure/', PaymentCallbackView.as_view(), name='webhook_failure'),
    # path('webhook/cancel/', PaymentCallbackView.as_view(), name='webhook_cancel'),
    # path('webhook/ipn/', PaymentCallbackView.as_view(), name='webhook_ipn'),
    # path('webhook/notify/', PaymentCallbackView.as_view(), name='webhook_notify'),
    # path('webhook/notify/success/', PaymentCallbackView.as_view(), name='webhook_notify_success'),
]
