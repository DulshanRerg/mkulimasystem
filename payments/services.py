import requests
from django.conf import settings

class PaymentGatewayService:
    """
    Handles API requests to your Python Payment Gateway.
    """
    BASE_URL = settings.PYTHON_GATEWAY_URL  # ✅ Your API Base URL

    @staticmethod
    def send_payment(account_number, amount, currency, external_id, provider, additional_properties=None):
        """
        Sends a payment request to your python-payment-gateway API.
        """
        payload = {
            "accountNumber": account_number,
            "amount": str(amount),
            "currency": currency,
            "externalId": external_id,
            "provider": provider,
            "additionalProperties": additional_properties or None,
        }

        headers = {
            "Content-Type": "application/json"
        }

        # ✅ Send request to your API (no authentication needed)
        response = requests.post(f"{PaymentGatewayService.BASE_URL}/mno-checkout", json=payload, headers=headers)

        return response.json()  # ✅ Return the response from your API
