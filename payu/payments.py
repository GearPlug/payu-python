from .enumerators import Country, Currency, Franchise, PaymentCommand, TransactionType
from .exceptions import CVVRequiredError
from .utils import get_available_franchise_for_payment


class Payment(object):
    TEST_BASE = 'https://sandbox.api.payulatam.com/payments-api/4.9/service.cgi'
    PROD_BASE = 'https://api.payulatam.com/payments-api/4.9/service.cgi'

    def __init__(self, client):
        self.client = client
        self.url = self.TEST_BASE if self.client.is_test else self.PROD_BASE

    def ping(self):
        payload = {
            'test': self.client.is_test,
            'language': self.client.language.value,
            'command': PaymentCommand.PING.value,
            'merchant': {
                'apiLogin': self.client.api_login,
                'apiKey': self.client.api_key
            }
        }
        return self.client._post(self.url, json=payload)

    def get_payments_methods(self):
        payload = {
            'test': self.client.is_test,
            'language': self.client.language.value,
            'command': PaymentCommand.GET_PAYMENT_METHODS.value,
            'merchant': {
                'apiLogin': self.client.api_login,
                'apiKey': self.client.api_key
            }
        }
        return self.client._post(self.url, json=payload)

    def make_payment(self, *, reference_code, description, tx_value, tx_tax, tx_tax_return_base, currency, buyer,
                     payer, credit_card, payment_method, payment_country, device_session_id, ip_address, cookie,
                     user_agent, language=None, shipping_address=None, extra_parameters=None, notify_url=None,
                     transaction_type=TransactionType.AUTHORIZATION_AND_CAPTURE):
        """
        Authorization: used to verify if a credit card is active, if it has funds, etc.
        The transaction is not complete until a transaction capture is sent (only available for accounts in Brazil).

        Capture: terminates a previously authorized transaction.
        This is when the account makes a debit to the card (only available for accounts in Brazil).

        Authorization and capture: this is the most used type of transaction.
        This option sends the transaction amount to authorization and if it is approved immediately capture is performed.

        Args:
            reference_code: The reference code of the order. It represents the identifier of the transaction
            in the shop’s system.
            Alphanumeric. Min: 1 Max: 255.

            description: The description of the order.
            Alphanumeric. Min: 1 Max: 255.

            tx_value: TX_VALUE, it is the total amount of the transaction. It can contain two decimal digits.
            For example 10000.00 and 10000.
            Alphanumeric. 64.

            tx_tax: TX_TAX, it is the value of the VAT (Value Added Tax only valid for Colombia) of the transaction,
            if no VAT is sent, the system will apply 19% automatically. It can contain two decimal digits.
            Example 19000.00. In case you have no VAT you should fill out 0.
            Alphanumeric. 64.

            tx_tax_return_base: TX_TAX_RETURN_BASE, it is the base value on which VAT (only valid for Colombia)
            is calculated. If you do not have VAT should be sent to 0.
            Alphanumeric. 64.

            currency: The ISO currency code associated with the amount.
            http://developers.payulatam.com/en/api/variables_table.html
            Alphanumeric. 3.

            buyer: Buyer’s shipping address.
            Example.
            {
                "merchantBuyerId": "1",
                "fullName": "First name and second buyer  name",
                "emailAddress": "buyer_test@test.com",
                "contactPhone": "7563126",
                "dniNumber": "5415668464654",
                "shippingAddress": {
                    "street1": "calle 100",
                    "street2": "5555487",
                    "city": "Medellin",
                    "state": "Antioquia",
                    "country": "CO",
                    "postalCode": "000000",
                    "phone": "7563126"
                }
            }

            payer: Payer’s data.
            Example.
            {
                "merchantPayerId": "1",
                "fullName": "First name and second payer name",
                "emailAddress": "payer_test@test.com",
                "contactPhone": "7563126",
                "dniNumber": "5415668464654",
                "billingAddress": {
                    "street1": "calle 93",
                    "street2": "125544",
                    "city": "Bogota",
                    "state": "Bogota DC",
                    "country": "CO",
                    "postalCode": "000000",
                    "phone": "7563126"
                }
            }

            credit_card: Debit card’s data.
            Example.
            {
                "number": "4097440000000004",
                "securityCode": "321",
                "expirationDate": "2022/12",
                "name": "APPROVED"
            }

            payment_method: Payment method.
            Alphanumeric. 32.

            payment_country: Payment countries.
            http://developers.payulatam.com/en/api/variables_table.html

            device_session_id: The session identifier of the device where the transaction was performed from.
            Alphanumeric. Max: 255.

            ip_address: The IP address of the device where the transaction was performed from.
            Alphanumeric. Max: 39.

            cookie: The cookie stored on the device where the transaction was performed from.
            Alphanumeric. Max: 255.

            user_agent: The user agent of the browser from which the transaction was performed.
            Alphanumeric. Max: 1024

            language: The language used in the emails that are sent to the buyer and seller.
            Alphanumeric. 2

            shipping_address: The shipping address.
            Example.
            {
                "street1": "calle 100",
                "street2": "5555487",
                "city": "Medellin",
                "state": "Antioquia",
                "country": "CO",
                "postalCode": "0000000",
                "phone": "7563126"
            }

            extra_parameters: Additional parameters or data associated with a transaction. These parameters may vary
            according to the payment means or shop’s preferences.
            Example.
            {
                "INSTALLMENTS_NUMBER": 1
            }

            notify_url: The URL notification or order confirmation.
            Alphanumeric. Max: 2048.

            transaction_type:

        Returns:

        """
        if not isinstance(payment_country, Country):
            payment_country = Country(payment_country)

        if not isinstance(transaction_type, TransactionType):
            transaction_type = TransactionType(transaction_type)

        if not isinstance(payment_method, Franchise):
            payment_method = Franchise(payment_method)

        if not isinstance(currency, Currency):
            currency = Currency(currency)

        franchises = get_available_franchise_for_payment(payment_country, transaction_type)
        if not franchises or payment_method not in franchises:
            fmt = 'The credit card franchise {} with transaction type {} is not available for {}.'
            raise CVVRequiredError(fmt.format(payment_method.value, transaction_type.value, payment_country.name))

        payload = {
            "language": self.client.language.value,
            "command": PaymentCommand.SUBMIT_TRANSACTION.value,
            "merchant": {
                "apiKey": self.client.api_key,
                "apiLogin": self.client.api_login
            },
            "transaction": {
                "order": {
                    "accountId": self.client.account_id,
                    "referenceCode": reference_code,
                    "description": description,
                    "language": language or self.client.language.value,
                    "signature": self.client._get_signature(reference_code, tx_value, currency.value),
                    "notifyUrl": notify_url,
                    "additionalValues": {
                        "TX_VALUE": {
                            "value": tx_value,
                            "currency": currency.value
                        },
                        "TX_TAX": {
                            "value": tx_tax,
                            "currency": currency.value
                        },
                        "TX_TAX_RETURN_BASE": {
                            "value": tx_tax_return_base,
                            "currency": currency.value
                        }
                    },
                    "buyer": buyer,
                    "shippingAddress": shipping_address
                },
                "payer": payer,
                "creditCard": credit_card,
                "extraParameters": extra_parameters,
                "type": transaction_type.value,
                "paymentMethod": payment_method.value,
                "paymentCountry": payment_country.value,
                "deviceSessionId": device_session_id,
                "ipAddress": ip_address,
                "cookie": cookie,
                "userAgent": user_agent
            },
            "test": self.client.is_test
        }
        return self.client._post(self.url, json=payload)

    def make_authorization(self, **kwargs):
        kwargs['transaction_type'] = TransactionType.AUTHORIZATION
        return self.make_payment(**kwargs)

    def make_capture(self, *, order_id, parent_transaction_id):
        payload = {
            "language": self.client.language.value,
            "command": PaymentCommand.SUBMIT_TRANSACTION.value,
            "merchant": {
                "apiLogin": self.client.api_login,
                "apiKey": self.client.api_key
            },
            "transaction": {
                "order": {
                    "id": order_id
                },
                "type": TransactionType.CAPTURE.value,
                "parentTransactionId": parent_transaction_id
            },
            "test": self.client.is_test
        }
        return self.client._post(self.url, json=payload)

    def cancel_payment(self):
        """
        Cancellation: used to reverse a previously authorized transaction (only available for accounts in Brazil).

        Returns:

        """
        raise NotImplementedError

    def refund_payment(self, *, order_id, parent_transaction_id, reason):
        payload = {
            "language": self.client.language.value,
            "command": PaymentCommand.SUBMIT_TRANSACTION.value,
            "merchant": {
                "apiLogin": self.client.api_login,
                "apiKey": self.client.api_key
            },
            "transaction": {
                "order": {
                    "id": order_id
                },
                "type": TransactionType.REFUND.value,
                "parentTransactionId": parent_transaction_id,
                "reason": reason
            },
            "test": self.client.is_test
        }
        return self.client._post(self.url, json=payload)
