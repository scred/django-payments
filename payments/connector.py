# single payment, rename Payment

# first you create a payment, then somehow you go for the checkout

# checkout is a different view, not handled by this code, but there
# needs to be a way to query for payment methods and forms per
# method. do we get the methods from the payment?

# do we need a payment data storage class
# the storage class needs to be registered for the payment class

# FIXME: Maybe do this by sub-classing instead of having storage
# classes, ie the sub-classes have the requirement to do
# storage. Could also have different types of payments that eg support
# carts. Processors could require specific types of payments.

# FIXME: processors should have support for mandatory and optional
# parameters

import logging
from processor import PaymentProcessor

class PaymentConnector():
    """
    Mandatory parameters for a payment:
     - ??
    """

    # FIXME: Do we need support for explicit payment states?

    # before clearing: methods that are available
    # after clearing: method that was used

    @classmethod
    def get_connector(self):
        return self.connector

    @classmethod
    def set_connector(self, klass):
        self.connector = klass

    @classmethod
    def lookup(self, code):
        raise NotImplementedError("connector must implement lookup()")

    def __init__(self):
        pass

    @property
    def code(self):
        return self.get_value("code")

    def get_payment_methods(self):
        return self.payment_methods

    def set_payment_methods(self, methods):
        self.payment_methods = methods

    def get_checkout_url(self, payment_method):
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.get_checkout_url()

    def get_checkout_params(self, payment_method):
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.get_checkout_params(self)

    def get_costs(self, payment_method):
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.get_costs(self)
    
    def get_value(self, key):
        raise NotImplementedError("connector doesn't implement get_value()")

    def set_value(self, key, value):
        raise NotImplementedError("connector doesn't implement set_value()")

    def get_values(self):
        raise NotImplementedError("connector doesn't implement get_values()")

    def save(self):
        raise NotImplementedError("connector doesn't implement save()")

    def load(self):
        raise NotImplementedError("connector doesn't implement load()")

    def add_item(self, **kwargs):
        raise NotImplementedError("not implemented by the connector")        
        return self.storage.add_item(self, **kwargs)

    def get_items(self):
        raise NotImplementedError("not implemented by the connector")
        return self.storage.get_items(self)

    def get_status(self):
        raise NotImplementedError("not implemented by the connector")

    def set_status(self, value):
        raise NotImplementedError("not implemented by the connector")        

    def query(self, payment_method):
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.query(self)

    def refund(self, payment_method):
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.refund(self)

    def success(self):
        raise NotImplementedError("connector doesn't implement success()")
