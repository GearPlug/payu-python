# payu-python

payu-python is an API wrapper for Payu written in Python. Currently only works for supported credit cards in the supported countries in Latam.

Supported countries:
* Argentina
* Brazil
* Chile
* Colombia
* Mexico
* Panama
* Peru
* Chile

Read `Utils` section to find out how to get the supported credit cards for a country.
Read `TODO` section to find out what's missing in this library.


## Installing
```
pip install payu-python
```

## Usage

### Client instantiation in sandbox mode (test)
```
TEST_API_LOGIN = 'pRRXKOl8ikMmt9u'
TEST_API_KEY = '4Vj8eK4rloUd272L48hsrarnUA'
TEST_MERCHANT_ID = 508029
TEST_ACCOUNT_ID = 512321

client = Client(TEST_API_LOGIN, TEST_API_KEY, TEST_MERCHANT_ID, TEST_ACCOUNT_ID, test=True, language='en', debug=True)
```

### Example data for sandbox mode
```
BUYER_EXAMPLE = {
    "merchantBuyerId": "1",
    "fullName": "Miguel Ferrer",
    "emailAddress": "mferrer@gearplug.io",
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

PAYER_EXAMPLE = {
    "merchantPayerId": "1",
    "fullName": "Miguel Ferrer",
    "emailAddress": "mferrer@gearplug.io",
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

CREDIT_CARD_EXAMPLE = {
    "number": "4097440000000004",
    "securityCode": "321",
    "expirationDate": "2022/12",
    "name": "APPROVED"
}

EXTRA_EXAMPLE = {
    "INSTALLMENTS_NUMBER": 1
}
```

### Payments Module

#### Ping service
```
r = client.payments.ping()
```

#### Get payments method
```
r = client.payments.get_payments_methods()
```

#### Make a payment (AUTHORIZATION AND CAPTURE)
```
r = client.payments.make_payment(reference_code='TestPayU01', description='Test Payment', tx_value=1000, tx_tax=0, 
                                 tx_tax_return_base=0, currency='COP', buyer=BUYER_EXAMPLE, payer=PAYER_EXAMPLE, 
                                 credit_card=CREDIT_CARD_EXAMPLE, payment_method='VISA', payment_country='CO', 
                                 device_session_id='vghs6tvkcle931686k1900o6e1', 
                                 ip_address='127.0.0.1', cookie='pt1t38347bs6jc9ruv2ecpv7o2', 
                                 user_agent='Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0', 
                                 extra_parameters=EXTRA_EXAMPLE,
                                 notify_url='https://ed60769e.ngrok.io/payu/notification/')
```

#### Make authorization (ONLY AUTHORIZATION)
```
r = client.payments.make_authorization(reference_code='TestPayU02', description='Test Payment', tx_value=1000, tx_tax=0, 
                                       tx_tax_return_base=0, currency='COP', buyer=BUYER_EXAMPLE, payer=PAYER_EXAMPLE, 
                                       credit_card=CREDIT_CARD_EXAMPLE, payment_method='VISA', payment_country='CO', 
                                       device_session_id='vghs6tvkcle931686k1900o6e1', 
                                       ip_address='127.0.0.1', cookie='pt1t38347bs6jc9ruv2ecpv7o2', 
                                       user_agent='Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0', 
                                       extra_parameters=EXTRA_EXAMPLE,
                                       notify_url='https://ed60769e.ngrok.io/payu/notification/')
```

#### Make capture (ONLY CAPTURE)
```
r = client.payments.make_capture(order_id='844928300', parent_transaction_id='4d7f240d-084a-426f-aa27-42c3b2a2b265')
```

#### Refund a payment
```
r = client.payments.refund_payment(order_id='844928300', parent_transaction_id='4d7f240d-084a-426f-aa27-42c3b2a2b265',
                                   reason='Client asked for refund.')
```

### Tokenization Module

#### Create a single token
```
r = client.tokenization.create_single_token(payer_id='1', name='Miguel Ferrer', identification_number='555555', 
                                            payment_method='VISA', number='4111111111111111', expiration_date='2022/01')
```

#### Make a payment
```
r = client.tokenization.make_payment(reference_code='TestPayU03', description='Test Payment', tx_value=1000, 
                                     currency='COP', buyer=BUYER_EXAMPLE, payer=PAYER_EXAMPLE, payment_method='VISA', 
                                     payment_country='CO', device_session_id='vghs6tvkcle931686k1900o6e1', 
                                     ip_address='127.0.0.1', cookie='pt1t38347bs6jc9ruv2ecpv7o2',
                                     user_agent='Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0',
                                     credit_card_token_id='b01877c3-b044-455a-99f5-82aed33795e9')
```

#### Make authorization (ONLY AUTHORIZATION)
```
r = client.tokenization.make_authorization(reference_code='TestPayU03', description='Test Payment', tx_value=1000, 
                                           currency='COP', buyer=BUYER_EXAMPLE, payer=PAYER_EXAMPLE, payment_method='VISA', 
                                           payment_country='CO', device_session_id='vghs6tvkcle931686k1900o6e1', 
                                           ip_address='127.0.0.1', cookie='pt1t38347bs6jc9ruv2ecpv7o2',
                                           user_agent='Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0',
                                           credit_card_token_id='b01877c3-b044-455a-99f5-82aed33795e9')
```

#### Make capture (ONLY CAPTURE)
```
r = client.tokenization.make_capture(order_id='844928300', parent_transaction_id='4d7f240d-084a-426f-aa27-42c3b2a2b265')
```

#### Get tokens for a payer (for the last year)
```
import datetime

r = client.tokenization.get_tokens(payer_id='1', credit_card_token_id='b65c63e9-ec0c-49ac-a67d-1414c3dc3ccc', 
                                   start_date=datetime.datetime.now().replace(year=2017), 
                                   end_date=datetime.datetime.now()))
```

#### Remove a token
```
r = client.tokenization.remove_token(payer_id='1', credit_card_token_id='d70889d2-0f82-482d-a2ed-3c0a2813d57c')
```

### Recurring Payments Module

#### Create a plan
```
r = client.recurring.create_plan(plan_code='PLAN_CODE', description='Test Plan', interval='MONTH', interval_count=1,
                                 max_payments_allowed=12, payment_attempts_delay=1, plan_value=1000, plan_tax=0,
                                 plan_tax_return_base=0, currency='COP')
```

#### Get plan
```
r = client.recurring.get_plan('PLAN_CODE')
```

#### Remove a plan
```
r = client.recurring.delete_plan('PLAN_CODE')
```

#### Create a customer
```
r = client.recurring.create_customer(full_name='Miguel Ferrer', email='mferrer@gearplug.io')
```

#### Get customer
```
r = client.recurring.get_customer('CUSTOMER_ID')
```

#### Delete a customer
```
r = client.recurring.delete_customer('CUSTOMER_ID')
```

#### Create a credit card
```
r = client.recurring.create_credit_card(customer_id='CUSTOMER_ID', name'Miguel Ferrer', document='555555', 
                                        number='4111111111111111', exp_month='01', exp_year='2022', type='VISA', 
                                        address='calle 93 125544 Bogota')
```

#### Get credit card
```
r = client.recurring.get_credit_card('CREDIT_CARD_ID')
```

#### Delete a credit card
```
r = client.recurring.delete_credit_card(customer_id='CUSTOMER_ID', credit_card_id='CREDIT_CARD_ID')
```

#### Create a subscription
```
r = client.recurring.create_subscription(customer_id='CUSTOMER_ID', credit_card_token='CREDIT_CARD_ID', 
                                         plan_code='PLAN_CODE')
```

#### Get subscription
```
r = client.recurring.get_subscription('SUBSCRIPTION_ID')
```

#### Update a subscription
```
r = client.recurring.update_subscription(subscription_id='SUBSCRIPTION_ID', credit_card_token='CREDIT_CARD_TOKEN')
```

#### Delete a subscription
```
r = client.recurring.delete_subscription('SUBSCRIPTION_ID')
```

#### Create an additional charge
```
r = client.recurring.create_additional_charge(subscription_id='SUBSCRIPTION_ID', description='TEST CHARGE', 
                                              plan_value=1000, plan_tax=0, plan_tax_return_base=0,
                                              currency='COP')
```

#### Get additional charge
```
r = client.recurring.get_additional_charge('RECURRING_BILLING_ID')
```

#### Update an additional charge
```
r = client.recurring.update_additional_charge(recurring_billing_id='RECURRING_BILLING_ID', description='TEST CHARGE', 
                                              plan_value=1000, plan_tax=0, plan_tax_return_base=0, currency='COP')
```

#### Delete an additional charge
```
r = client.recurring.delete_additional_charge('RECURRING_BILLING_ID')
```

#### Get recurring bill
```
import datetime

r = client.recurring.get_recurring_bill(customer_id='CUSTOMER_ID', 
                                        date_begin=datetime.datetime.now().replace(year=2017), 
                                        date_final=datetime.datetime.now())
```

### Queries Module

#### Get order by identifier
```
r = client.queries.get_order_by_identifier('ORDER_ID')
```

#### Get order by reference code
```
r = client.queries.get_order_by_reference('REFERENCE_CODE')
```

#### Get order by transaction
```
r = client.queries.get_transaction_response('TRANSACTION_ID')
```

## Utils

#### Get supported credit cards for payments in a country
```
from payu.utils import get_available_franchise_for_payment
from payu.enumerators import Country, TransactionType

r = get_available_franchise_for_payment(Country.COLOMBIA, TransactionType.AUTHORIZATION)
r = get_available_franchise_for_payment(Country.COLOMBIA, TransactionType.AUTHORIZATION_AND_CAPTURE)
```

#### Get supported credit cards for tokenization in a country
```
from payu.utils import get_available_franchise_for_tokenization
from payu.enumerators import Country, TransactionType

r = get_available_franchise_for_tokenization(Country.COLOMBIA, TransactionType.AUTHORIZATION)
r = get_available_franchise_for_tokenization(Country.COLOMBIA, TransactionType.AUTHORIZATION_AND_CAPTURE)
```

#### Check if tokenized payment needs credit card CVV
```
from payu.utils import has_franchise_cvv_tokenization
from payu.enumerators import Country, Franchise, TransactionType

r = get_available_franchise_for_tokenization(Franchise.VISA, Country.COLOMBIA, TransactionType.AUTHORIZATION_AND_CAPTURE)
```

## TODO

### Payments
* cancel_payment()
* Support for cash / bank payment methods
* Support for bank transfer methods

### Tokenization
* create_multiple_tokens()
* make_multiple_payments()

### Recurring Payments
* update_plan()
* update_customer()
* update_credit_card()

## Contributing
We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.

#### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/GearPlug/payu-python/issues).

#### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/GearPlug/payu-python )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
