import hashlib
import logging

import requests

from payu.enumerators import Language
from payu.payments import Payment
from payu.queries import Query
from payu.recurring import Recurring
from payu.tokenization import Tokenization

fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)


class Client(object):
    TEST_BASE = 'https://sandbox.api.payulatam.com'
    PROD_BASE = 'https://api.payulatam.com'

    def __init__(self, api_login, api_key, merchant_id, account_id, language=Language.ENGLISH,
                 payments_api_version='4.0', recurring_api_version='4.9', reports_api_version='4.0', sandbox=False,
                 test=False, debug=False):
        self.api_login = api_login
        self.api_key = api_key
        self.merchant_id = merchant_id
        self.account_id = account_id

        if not isinstance(language, Language):
            language = Language(language)
        self.language = language

        self.payments_api_version = payments_api_version
        self.recurring_api_version = recurring_api_version
        self.reports_api_version = reports_api_version
        self.sandbox = sandbox
        self.test = test
        self.debug = debug

        self.url = self.TEST_BASE if self.is_sandbox else self.PROD_BASE

        self.payments = Payment(self)
        self.recurring = Recurring(self)
        self.tokenization = Tokenization(self)
        self.queries = Query(self)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @property
    def is_sandbox(self):
        return self.sandbox

    @property
    def is_test(self):
        return self.test

    @property
    def is_debug(self):
        return self.debug

    def _get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, headers=None, **kwargs):
        """
        Normally the connection guarantees response times of 3 seconds on average,
        if there is an abnormal situation, the maximum response time is 1 minute.
        It is highly recommended that you set “timeouts” when you connect with PayU.

        Args:
            method:
            url:
            headers:
            **kwargs:

        Returns:

        """
        _headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if headers:
            _headers.update(headers)

        if self.is_debug:
            self.logger.debug('{} {} {} {}'.format(method, url, headers, kwargs))
        return self._parse(requests.request(method, url, headers=_headers, timeout=60, **kwargs))

    def _parse(self, response):
        if 'Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            if self.is_debug:
                fmt = 'The response with status code ({}) is not JSON deserializable. Response: {}'
                self.logger.warning(fmt.format(response.status_code, response.text))

            r = response.text
        return r

    def _get_signature(self, reference_code, tx_value, currency):
        signature = '{}~{}~{}~{}~{}'.format(self.api_key, self.merchant_id, reference_code, tx_value, currency)
        return hashlib.md5(signature.encode('utf')).hexdigest()
