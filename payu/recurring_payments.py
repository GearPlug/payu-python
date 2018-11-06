import base64


class Recurring(object):
    TEST_BASE = 'https://sandbox.api.payulatam.com/payments-api/rest/v4.3/'
    PROD_BASE = 'https://api.payulatam.com/payments-api/rest/v4.3/'

    def __init__(self, client):
        self.client = client
        self.url = self.TEST_BASE if self.client.is_test else self.PROD_BASE

    def create_plan(self, *, plan_code, description, interval, interval_count, max_payments_allowed,
                    payment_attempts_delay, plan_value, plan_tax, plan_tax_return_base, currency,
                    max_payment_attempts=None, max_pending_payments=None, trial_days=None):
        """
        Creating a new plan for subscriptions associated with the merchant.

        Args:

            plan_code:
            Unique code assigned by the merchant to the plan in order to identify it.

            Alphanumeric. Min: 1 Max: 255

            description:
            Plan description.

            Alphanumeric. Min: 1 Max: 255

            interval:
            Interval that defines how often the suscription payment is performed.
            The possible values are: DAY, WEEK, MONTH y YEAR.

            Alphanumeric. Min: 3 Max: 5

            interval_count:
            Interval count that defines how often the suscription payment is performed.

            Numeric.

            max_payments_allowed:
            Total amount of payments for the suscription.

            Numeric.

            payment_attempts_delay:
            Total amount of waiting days between the payment attempts of the suscription.

            Numeric.

            plan_value:
            total value of the plan.

            Alphanumeric. Min: 1 Max: 255

            plan_tax:
            tax value associated to the value of the plan.

            Alphanumeric. Min: 1 Max: 255

            plan_tax_return_base:
            tax return base value associated to the value of the plan.

            Alphanumeric. Min: 1 Max: 255

            currency:
            The ISO currency code associated with the amount.
            http://developers.payulatam.com/en/api/variables_table.html

            max_payment_attempts:
            Total amount of payment attempts performed when a suscription payment is declined.

            Numeric. Max: 3

            max_pending_payments:
            Total amount of pending payments that a suscription can have before it is cancelled.

            Numeric

            trial_days:
            Total amount of trial days of the suscription.

            Numeric

        Returns:

        """
        payload = {
            "accountId": self.client.account_id,
            "planCode": plan_code,
            "description": description,
            "interval": interval,
            "intervalCount": interval_count,
            "maxPaymentsAllowed": max_payments_allowed,
            "paymentAttemptsDelay": payment_attempts_delay,
            "additionalValues": [
                {
                    "name": "PLAN_VALUE",
                    "value": plan_value,
                    "currency": currency
                },
                {
                    "name": "PLAN_TAX",
                    "value": plan_tax,
                    "currency": currency
                },
                {
                    "name": "PLAN_TAX_RETURN_BASE",
                    "value": plan_tax_return_base,
                    "currency": currency
                }
            ],
            "maxPaymentAttempts": max_payment_attempts,
            "maxPendingPayments": max_pending_payments,
            "trialDays": trial_days
        }
        return self.client._post(self.url + 'plans', json=payload, headers=self.get_headers())

    def get_plan(self, plan_code):
        """
        Check all the information of a plan for subscriptions associated with the merchant.

        Args:
            plan_code: Plan’s identification code for the merchant.

        Returns:

        """
        return self.client._get(self.url + 'plans/{}'.format(plan_code), headers=self.get_headers())

    def update_plan(self, plan_code):
        raise NotImplementedError

    def delete_plan(self, plan_code):
        """
        Delete an entire subscription plan associated with the merchant.

        Args:
            plan_code: Plan’s identification code for the merchant.

        Returns:

        """
        return self.client._delete(self.url + 'plans/{}'.format(plan_code), headers=self.get_headers())

    def create_customer(self, full_name, email):
        """
        Creation of a customer in the system.

        Args:
            full_name: Customer's complete name.

            Alphanumeric. Max: 255

            email: Customer's email address.

            Alphanumeric. Max: 255

        Returns:

        """
        payload = {
            'fullName': full_name,
            'email': email
        }
        return self.client._post(self.url + 'customers', json=payload, headers=self.get_headers())

    def get_customer(self, customer_id):
        """
        Queries the information related to the customer.

        Args:
            customer_id: Identifier of the client from which you want to find the associated information.

        Returns:

        """
        return self.client._get(self.url + 'customers/{}'.format(customer_id), headers=self.get_headers())

    def update_customer(self, plan_code):
        raise NotImplementedError

    def delete_customer(self, customer_id):
        """
        Removes a user from the system.

        Args:
            customer_id: Identifier of the client to be deleted.

        Returns:

        """
        return self.client._delete(self.url + 'customers/{}'.format(customer_id), headers=self.get_headers())

    def get_headers(self):
        token = '{}:{}'.format(self.client.api_login, self.client.api_key)
        result = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        return {'Authorization': 'Basic {}'.format(result)}
