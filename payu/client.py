import hashlib

import requests

from .payments import Payment
from .recurring_payments import Recurring
from .tokenization import Tokenization


class Client(object):

    def __init__(self, api_login, api_key, merchant_id, account_id, test=False, language='en'):
        self.api_login = api_login
        self.api_key = api_key
        self.merchant_id = merchant_id
        self.account_id = account_id
        self.test = test
        self.language = language

        self.payments = Payment(self)
        self.recurring = Recurring(self)
        self.tokenization = Tokenization(self)

    @property
    def is_test(self):
        return self.test

    def _get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, headers=None, **kwargs):
        _headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if headers:
            _headers.update(headers)
        return self._parse(requests.request(method, url, headers=_headers, **kwargs))

    def _parse(self, response):
        if 'Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        return r

    def _get_signature(self, reference_code, tx_value, currency):
        signature = '{}~{}~{}~{}~{}'.format(self.api_key, self.merchant_id, reference_code, tx_value, currency)
        return hashlib.md5(signature.encode('utf')).hexdigest()
