class Tokenization(object):
    TEST_BASE = 'https://sandbox.api.payulatam.com/payments-api/4.0/service.cgi'
    PROD_BASE = 'https://api.payulatam.com/payments-api/4.0/service.cgi'

    def __init__(self, client):
        self.client = client
        self.url = self.TEST_BASE if self.client.is_test else self.PROD_BASE

    def create_single_token(self, *, payer_id, name, identification_number, payment_method, number, expiration_date):
        """
        Using this feature you can register a customer’s credit card data and get a token sequential number.

        Args:
            payer_id:
            name:
            identification_number:
            payment_method:
            number:
            expiration_date:

        Returns:

        """
        payload = {
            "language": self.client.language,
            "command": "CREATE_TOKEN",
            "merchant": {
                "apiLogin": self.client.api_login,
                "apiKey": self.client.api_key
            },
            "creditCardToken": {
                "payerId": payer_id,
                "name": name,
                "identificationNumber": identification_number,
                "paymentMethod": payment_method,
                "number": number,
                "expirationDate": expiration_date
            },
            "test": self.client.is_test
        }
        return self.client._post(self.url, json=payload)

    def create_multiple_tokens(self):
        """
        Using this feature you can register various customer’s credit card data and get token sequential numbers.

        For massive credit card tokenization you must create a file with CSV format with the following conditions:

        Each credit card register to be tokenized must contain data for the registration of a credit card,
        separated by commas in the following order: Payer ID, full name, credit card number, expiration date,
        franchise, and identification number.

        The file should have no header. The first line shows the first record.
        The file must be encoded under the UTF-8 standard.
        The file must not have more than 10,000 registers.

        Returns:

        """
        raise NotImplementedError

    def make_single_payment(self, *, reference_code, description, tx_value, currency, buyer, payer,
                            credit_card_token_id, payment_method, payment_country, device_session_id, ip_address,
                            cookie, user_agent, language=None, shipping_address=None, extra_parameters=None,
                            notify_url=None, security_code=None):
        """
        This feature allows you to make collections using a Token code that was previously created by our system,
        and which was used to store your customers’ credit cards data safely.

        Args:
            reference_code: The reference code of the order. It represents the identifier of the transaction
            in the shop’s system.
            Alphanumeric. Min: 1 Max: 255.

            description: The description of the order.
            Alphanumeric. Min: 1 Max: 255.

            tx_value: TX_VALUE, it is the total amount of the transaction. It can contain two decimal digits.
            For example 10000.00 and 10000.
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

            credit_card_token_id: Debit card’s data.
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
            Alphanumeric. Max: 1024.

            language: The language used in the emails that are sent to the buyer and seller.
            Alphanumeric. 2.

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

            security_code: CVV.

        Returns:

        """
        payload = {
            "language": self.client.language,
            "command": "SUBMIT_TRANSACTION",
            "merchant": {
                "apiKey": self.client.api_key,
                "apiLogin": self.client.api_login
            },
            "transaction": {
                "order": {
                    "accountId": self.client.account_id,
                    "referenceCode": reference_code,
                    "description": description,
                    "language": language or self.client.language,
                    "signature": self.client._get_signature(reference_code, tx_value, currency),
                    "notifyUrl": notify_url,
                    "additionalValues": {
                        "TX_VALUE": {
                            "value": tx_value,
                            "currency": currency
                        }
                    },
                    "buyer": buyer,
                    "shippingAddress": shipping_address
                },
                "payer": payer,
                "creditCardTokenId": credit_card_token_id,
                "extraParameters": extra_parameters,
                "type": "AUTHORIZATION_AND_CAPTURE",
                "paymentMethod": payment_method,
                "paymentCountry": payment_country,
                "deviceSessionId": device_session_id,
                "ipAddress": ip_address,
                "cookie": cookie,
                "userAgent": user_agent
            },
            "test": self.client.is_test
        }
        return self.client._post(self.url, json=payload)

    def make_multiple_payments(self):
        """
        This feature will allow you to make massive collections using the Token that were previously created by our
        system

        For this functionality you need to create a CSV file under the following conditions:

        Each transaction register to be processed must contain its processing data separated by commas in the
        following order: Account ID (identifier of the virtual PayU account), Token, security code,
        number of installments, sale Reference, sale description, buyer’s email, currency (ISO code),
        total (including tax), tax, base value of reimbursement, additional value, language (ISO code).

        The file should have no header. The first line shows the first record.
        The file must be encoded under the UTF-8 standard.
        The file must not have more than 10,000 records.

        Returns:

        """
        raise NotImplementedError

    def get_tokens(self, *, payer_id, credit_card_token_id, start_date, end_date):
        """
        With this functionality you can query previously the Credit Cards Token.

        Args:
            payer_id:
            credit_card_token_id:
            start_date:
            end_date:

        Returns:

        """
        payload = {
            "language": self.client.language,
            "command": "GET_TOKENS",
            "merchant": {
                "apiLogin": self.client.api_login,
                "apiKey": self.client.api_key
            },
            "creditCardTokenInformation": {
                "payerId": payer_id,
                "creditCardTokenId": credit_card_token_id,
                "startDate": start_date.strftime('%Y-%m-%dT%H:%M:%S'),
                "endDate": end_date.strftime('%Y-%m-%dT%H:%M:%S')
            },
            "test": self.client.is_test
        }
        return self.client._post(self.url, json=payload)

    def remove_token(self, *, payer_id, credit_card_token_id):
        """
        This feature allows you to delete a tokenized credit card register.

        Args:
            payer_id:
            credit_card_token_id:

        Returns:

        """
        payload = {
            "language": self.client.language,
            "command": "REMOVE_TOKEN",
            "merchant": {
                "apiLogin": self.client.api_login,
                "apiKey": self.client.api_key
            },
            "removeCreditCardToken": {
                "payerId": payer_id,
                "creditCardTokenId": credit_card_token_id
            },
            "test": self.client.is_test
        }
        return self.client._post(self.url, json=payload)
