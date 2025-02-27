import requests
from django.conf import settings

class AzamPayService:
    """
    Handles integration with the AzamPay API.
    """
    def __init__(self):
        self.base_url = settings.AZAMPAY_BASE_URL
        self.client_id = settings.AZAMPAY_CLIENT_ID
        self.client_secret = settings.AZAMPAY_CLIENT_SECRET

    def get_access_token(self):
        response = requests.post(f'{self.base_url}/auth/token', data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        data = response.json()
        return data.get('access_token')

    def initiate_payment(self, amount, currency, external_id, payer_email, callback_url):
        access_token = self.get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        payload = {
            'amount': amount,
            'currency': currency,
            'externalId': external_id,
            'payerEmail': payer_email,
            'callbackUrl': callback_url,
        }
        response = requests.post(f'{self.base_url}/payment/initiate', json=payload, headers=headers)
        return response.json()
