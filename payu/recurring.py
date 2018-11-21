import base64


class Recurring(object):

    def __init__(self, client):
        self.client = client
        self.url = self.client.url + '/payments-api/rest/v{}/'.format(self.client.recurring_api_version)

    def create_plan(self, *, plan_code, description, interval, interval_count, max_payments_allowed,
                    payment_attempts_delay, plan_value, plan_tax, plan_tax_return_base, currency,
                    max_payment_attempts=None, max_pending_payments=None, trial_days=None):
        """
        Creating a new plan for subscriptions associated with the merchant.

        Args:

            plan_code: Unique code assigned by the merchant to the plan in order to identify it.
            Alphanumeric. Min: 1 Max: 255.

            description: Plan description.
            Alphanumeric. Min: 1 Max: 255.

            interval: Interval that defines how often the suscription payment is performed.
            The possible values are: DAY, WEEK, MONTH y YEAR.
            Alphanumeric. Min: 3 Max: 5.

            interval_count: Interval count that defines how often the suscription payment is performed.
            Numeric.

            max_payments_allowed: Total amount of payments for the suscription.
            Numeric.

            payment_attempts_delay: Total amount of waiting days between the payment attempts of the suscription.
            Numeric.

            plan_value: total value of the plan.
            Alphanumeric. Min: 1 Max: 255.

            plan_tax: tax value associated to the value of the plan.
            Alphanumeric. Min: 1 Max: 255.

            plan_tax_return_base: tax return base value associated to the value of the plan.
            Alphanumeric. Min: 1 Max: 255.

            currency: The ISO currency code associated with the amount.
            http://developers.payulatam.com/en/api/variables_table.html

            max_payment_attempts: Total amount of payment attempts performed when a suscription payment is declined.
            Numeric. Max: 3.

            max_pending_payments: Total amount of pending payments that a suscription can have before it is cancelled.
            Numeric.

            trial_days: Total amount of trial days of the suscription.
            Numeric.

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

    def create_customer(self, *, full_name, email):
        """
        Creation of a customer in the system.

        Args:
            full_name: Customer's complete name.
            Alphanumeric. Max: 255.

            email: Customer's email address.
            Alphanumeric. Max: 255.

        Returns:

        """
        payload = {
            "fullName": full_name,
            "email": email
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

    def create_credit_card(self, *, customer_id, name, document, number, exp_month, exp_year, type, address):
        """
        Creating a credit card (Token) and assigning it to a user.

        Args:
            customer_id: Identifier of the client with whom you are going to associate the token with.

            name: Full name of the credit card holder as shown in the credit card.
            Alphanumeric. Min: 1 Max: 255.

            document: Identification number of the credit card holder.
            Alphanumeric. Min: 1 Max: 30.

            number: Credit card number.
            Numeric. Min: 13 Max: 20.

            exp_month: Credit card’s expiration month.
            Numeric. Min: 1 Max: 12.

            exp_year: Credit card’s expiration year. If it is a two digit value, it represents the years
            between 2000 (00) and 2099 (99). It the value has more than two digits it is used literally,
            being 2000 the minimum value.
            Numeric. Min: 00 Max: 2999.

            type: The franchise or credit card type.
            http://developers.payulatam.com/en/api/variables_table.html
            Alphanumeric.

            address: Credit card holder's billing address, associated to the credit card.

        Returns:

        """
        payload = {
            "name": name,
            "document": document,
            "number": number,
            "expMonth": exp_month,
            "expYear": exp_year,
            "type": type,
            "address": address
        }
        fmt = 'customers/{}/creditCards'.format(customer_id)
        return self.client._post(self.url + fmt, json=payload, headers=self.get_headers())

    def get_credit_card(self, credit_card_id):
        """
        Check the information of a credit card (Token) data identifier.

        Args:
            credit_card_id: Credit Card Token you want to consult.

        Returns:

        """
        return self.client._get(self.url + 'creditCards/{}'.format(credit_card_id), headers=self.get_headers())

    def update_credit_card(self):
        raise NotImplementedError

    def delete_credit_card(self, *, customer_id, credit_card_id):
        """
        Delete a credit card (Token) associated with a user.

        Args:
            customer_id: Identifier of the client of whom you are going to delete the token.
            credit_card_id: Identifier of the token to be deleted.

        Returns:

        """
        fmt = 'customers/{}/creditCards/{}'.format(customer_id, credit_card_id)
        return self.client._delete(self.url + fmt, headers=self.get_headers())

    def create_subscription(self, *, customer_id, credit_card_token, plan_code, quantity=None, installments=None,
                            trial_days=None, immediate_payment=None, extra1=None, extra2=None, delivery_address=None,
                            notify_url=None, recurring_bill_items=None):
        """
        Creating a new subscription of a client to a plan.

        Args:
            customer_id: Customer that will be associated to the subscription.
            You can find more information in the "Customer" section of this page.

            credit_card_token: Customer's credit card that is selected to make the payment.
            You can find more information in the "Credit card" section of this page.

            plan_code: Plan that will be associated to the subscription.
            You can find more information in the "Plan" section of this page.

            quantity: Total amount of plans that will be acquired with the subscription.
            Numeric.

            installments: Total amount of installments to defer the payment.
            Numeric.

            trial_days: Total amount of trial days of the subscription.
            This variable has preference over the plan's trial days.
            Numeric.

            immediate_payment:

            extra1:

            extra2:

            delivery_address:

            notify_url:

            recurring_bill_items:

        Returns:

        """
        payload = {
            "quantity": quantity,
            "installments": installments,
            "trialDays": trial_days,
            "immediatePayment": immediate_payment,
            "extra1": extra1,
            "extra2": extra2,
            "customer": {
                "id": customer_id,
                "creditCards": [
                    {
                        "token": credit_card_token
                    }
                ]
            },
            "plan": {
                "planCode": plan_code
            },
            "deliveryAddress": delivery_address,
            "notifyUrl": notify_url,
            "recurringBillItems": recurring_bill_items
        }
        return self.client._post(self.url + 'subscriptions', json=payload, headers=self.get_headers())

    def get_subscription(self, subscription_id):
        """
        Check the basic information associated with the specified subscription.

        Args:
            subscription_id: Identification of the subscription.

        Returns:

        """
        return self.client._put(self.url + 'subscriptions/{}'.format(subscription_id), headers=self.get_headers())

    def update_subscription(self, *, subscription_id, credit_card_token):
        """
        Update information associated with the specified subscription. At the moment it is only possible
        to update the token of the credit card to which the charge of the subscription is made.

        Args:
            subscription_id: Identification of the subscription.
            credit_card_token:

        Returns:

        """
        payload = {
            "creditCardToken": credit_card_token
        }
        fmt = 'subscriptions/{}'.format(subscription_id)
        return self.client._put(self.url + fmt, json=payload, headers=self.get_headers())

    def delete_subscription(self, subscription_id):
        """
        Unsubscribe, delete the relationship of the customer with the plan.

        Args:
            subscription_id: Identification of the subscription.

        Returns:

        """
        return self.client._delete(self.url + 'subscriptions/{}'.format(subscription_id), headers=self.get_headers())

    def create_additional_charge(self, *, subscription_id, description, plan_value, plan_tax, plan_tax_return_base,
                                 currency):
        """
        Adds extra charges to the respective invoice for the current period.

        Args:
            subscription_id: Identification of the subscription
            description:
            plan_value:
            plan_tax:
            plan_tax_return_base:
            currency:

        Returns:

        """
        payload = {
            "description": description,
            "additionalValues": [
                {
                    "name": "ITEM_VALUE",
                    "value": plan_value,
                    "currency": currency
                },
                {
                    "name": "ITEM_TAX",
                    "value": plan_tax,
                    "currency": currency
                },
                {
                    "name": "ITEM_TAX_RETURN_BASE",
                    "value": plan_tax_return_base,
                    "currency": currency
                }
            ]
        }
        fmt = 'subscriptions/{}/recurringBillItems'.format(subscription_id)
        return self.client._post(self.url + fmt, json=payload, headers=self.get_headers())

    def get_additional_charge_by_identifier(self, recurring_billing_id):
        """
        Query extra charge information of an invoice from its identifier.

        Args:
            recurring_billing_id: Identifier of the additional charge.

        Returns:

        """
        fmt = 'recurringBillItems/{}'.format(recurring_billing_id)
        return self.client._get(self.url + fmt, headers=self.get_headers())

    def get_additional_charge_by_description(self, description):
        """
        Query extra charges of shop’s invoices that meet the stipulated filters.

        Args:
            description: Description entered in the extra charge.

        Returns:

        """
        params = {
            "description": description
        }
        return self.client._get(self.url + 'recurringBillItems/', params=params, headers=self.get_headers())

    def get_additional_charge_by_subscription(self, subscription_id):
        """
        Query extra charges of shop’s invoices that meet the stipulated filters.

        Args:
            subscription_id: Identification of the subscription.

        Returns:

        """
        params = {
            "subscriptionId": subscription_id
        }
        return self.client._get(self.url + 'recurringBillItems/', params=params, headers=self.get_headers())

    def update_additional_charge(self, *, recurring_billing_id, description, plan_value, plan_tax, plan_tax_return_base,
                                 currency):
        """
        Updates the information from an additional charge in an invoice.

        Args:
            recurring_billing_id: Identifier of the additional charge.
            description:
            plan_value:
            plan_tax:
            plan_tax_return_base:
            currency:

        Returns:

        """
        payload = {
            "description": description,
            "additionalValues": [
                {
                    "name": "ITEM_VALUE",
                    "value": plan_value,
                    "currency": currency
                },
                {
                    "name": "ITEM_TAX",
                    "value": plan_tax,
                    "currency": currency
                },
                {
                    "name": "ITEM_TAX_RETURN_BASE",
                    "value": plan_tax_return_base,
                    "currency": currency
                }
            ]
        }
        fmt = 'recurringBillItems/{}'.format(recurring_billing_id)
        return self.client._put(self.url + fmt, payload=payload, headers=self.get_headers())

    def delete_additional_charge(self, recurring_billing_id):
        """
        Remove an extra charge from an invoice.

        Args:
            recurring_billing_id: Identifier of the additional charge.

        Returns:

        """
        fmt = 'recurringBillItems/{}'.format(recurring_billing_id)
        return self.client._delete(self.url + fmt, headers=self.get_headers())

    def get_recurring_bill_by_client(self, *, customer_id, date_begin=None, date_final=None):
        """
        Consulta de las facturas que están pagadas o pendientes por pagar. Se puede consultar por cliente,
        por suscripción o por rango de fechas.

        Args:
            customer_id:
            date_begin:
            date_final:

        Returns:

        """
        params = {
            "customerId": customer_id,
        }
        if date_begin and date_final:
            params['dateBegin'] = date_begin.strftime('%Y-%m-%d')
            params['dateFinal'] = date_final.strftime('%Y-%m-%d')
        return self.client._get(self.url + 'recurringBill', params=params, headers=self.get_headers())

    def get_recurring_bill_by_subscription(self, subscription_id):
        """
        Consulta de las facturas que están pagadas o pendientes por pagar. Se puede consultar por cliente,
        por suscripción o por rango de fechas.

        Args:
            subscription_id:

        Returns:

        """
        params = {
            "subscriptionId": subscription_id,
        }
        return self.client._get(self.url + 'recurringBill', params=params, headers=self.get_headers())

    def get_headers(self):
        token = '{}:{}'.format(self.client.api_login, self.client.api_key)
        result = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        return {'Authorization': 'Basic {}'.format(result)}
