from .enumerators import QueryCommand


class Query(object):
    TEST_BASE = 'https://sandbox.api.payulatam.com/reports-api/4.0/service.cgi'
    PROD_BASE = 'https://api.payulatam.com/reports-api/4.0/service.cgi'

    def __init__(self, client):
        self.client = client
        self.url = self.TEST_BASE if self.client.is_test else self.PROD_BASE

    def ping(self):
        payload = {
            'test': self.client.is_test,
            'language': self.client.language.value,
            'command': QueryCommand.PING.value,
            'merchant': {
                'apiLogin': self.client.api_login,
                'apiKey': self.client.api_key
            }
        }
        return self.client._post(self.url, json=payload)

    def get_order_by_identifier(self, order_id):
        payload = {
            "test": self.client.is_test,
            "language": self.client.language,
            "command": QueryCommand.ORDER_DETAIL.value,
            "merchant": {
                "apiLogin": self.client.api_login,
                "apiKey": self.client.api_key
            },
            "details": {
                "orderId": order_id
            }
        }
        return self.client._post(self.url, json=payload)

    def get_order_by_reference(self, reference_code):
        payload = {
            "test": self.client.is_test,
            "language": self.client.language,
            "command": QueryCommand.ORDER_DETAIL_REFERENCE_CODE.value,
            "merchant": {
                "apiLogin": self.client.api_login,
                "apiKey": self.client.api_key
            },
            "details": {
                "referenceCode": reference_code
            }
        }
        return self.client._post(self.url, json=payload)

    def get_transaction_response(self, transaction_id):
        payload = {
            "test": self.client.is_test,
            "language": self.client.language,
            "command": QueryCommand.TRANSACTION_RESPONSE_DETAIL.value,
            "merchant": {
                "apiLogin": self.client.api_login,
                "apiKey": self.client.api_key
            },
            "details": {
                "transactionId": transaction_id
            }
        }
        return self.client._post(self.url, json=payload)
