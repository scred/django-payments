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

    def __init__(self, **kwargs):
        """ Deprecated! """

        self.connector = None
        self.payment_methods = None
        self.values = {"code": kwargs["code"]}
        self.cart = []
        self.payment_method = None

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

    def get_checkout_form(self, payment_method):
        logging.warn("Deprecated method get_checkout_form() called!")
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.get_checkout_form(self)

    def get_checkout_forms(self):
        logging.warn("Deprecated method get_checkout_forms() called!")
        forms = {}
        for method in self.get_payment_methods():
            pp = PaymentProcessor.get_processor(method)
            forms[method] = pp.get_checkout_form(self)
        return forms

    def get_query_form(self, payment_method):
        # FIXME: deprecated! kill kill!
        print "get_query_form() called"
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.get_query_form(self)

    # FIXME: buggy! the payment method must already have been defined,
    # ie the payment completed, or otherwise it makes no sense to do a
    # query like this.

    # FIXME: No validation or status parameter setting is done, but
    # perhaps should.
    
    def query(self, payment_method):
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.query(self)

    def refund(self, payment_method):
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.refund(self)

    def success(self, payment_method):
        
        self.set_value("__cleared", "true")
        self.set_value("_method", payment_method)
        self.save()

        # FIXME: Sending signal is missing!

    def get_value(self, key):
        raise NotImplementedError("connector doesn't implement get_value()")
        #return self.storage.get_value(self, key)

    def set_value(self, key, value):
        return self.storage.set_value(self, key, value)

    def get_values(self):
        return self.storage.get_values(self)

    def save(self):
        raise NotImplementedError()
        return self.storage.save(self)

    def load(self):
        raise NotImplementedError()
        return self.storage.load(self)

    def add_item(self, **kwargs):
        return self.storage.add_item(self, **kwargs)

    def get_items(self):
        return self.storage.get_items(self)

    def get_status(self):
        return self.get_value("__status")

    def set_status(self, value):
        return self.set_value("__status", value)

    @classmethod
    def lookup(self, code):
        raise NotImplementedError("connector must implement lookup()")

        c = self.get_connector()
        return c.lookup(code)
        print "c:", c
        return None
        #payment = Payment(code=code)
        #payment.load()
        #return payment

class PickledStorage():

    @classmethod
    def get_value(self, payment, key):
        return payment.values[key]

    @classmethod
    def set_value(self, payment, key, value):
        payment.values[key] = value
        return value

    @classmethod
    def get_values(self, payment):
        return payment.values

    @classmethod
    def add_item(self, payment, **kwargs):
        payment.cart.append(kwargs)
        return kwargs

    @classmethod
    def get_items(self, payment):
        return payment.cart

    @classmethod
    def save(self, payment):
        import pickle
        fh = open("%s.pickle" % payment.code, "w")
        pickle.dump(payment.values, fh)
        fh.close()

    @classmethod
    def load(self, payment):
        import pickle
        fh = open("%s.pickle" % payment.code, "r")
        payment.values = pickle.load(fh)
        fh.close()
