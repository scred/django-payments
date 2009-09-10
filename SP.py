# single payment, rename Payment

# first you create a payment, then somehow you go for the checkout

# checkout is a different view, not handled by this code, but there
# needs to be a way to query for payment methods and forms per
# method. do we get the methods from the payment?

# do we need a payment data storage class
# the storage class needs to be registered for the payment class

from processor import PaymentProcessor

class Payment():

    """
    Mandatory parameters for a payment:
     - ??
    """

    # FIXME: Do we need support for explicit payment states?

    # before clearing: methods that are available
    # after clearing: method that was used

    @classmethod
    def set_storage(self, klass):
        self.storage = klass

    def __init__(self, **kwargs):

        # print "__init__ of Payment() called"

        self.payment_methods = None
        self.values = {"code": kwargs["code"]}
        #self.cart = None
        #self.recipient = None

    @property
    def code(self):
        return self.values["code"]

    def get_payment_methods(self):
        return self.payment_methods

    def set_payment_methods(self, methods):
        self.payment_methods = methods

    def get_checkout_form(self, payment_method):
        pp = PaymentProcessor.get_processor(payment_method)
        return pp.get_checkout_form(self)

    def get_checkout_forms(self):
        forms = {}
        for method in self.get_payment_methods():
            pp = PaymentProcessor.get_processor(method)
            forms[method] = pp.get_checkout_form(self)
        return forms

    def success(payment_method):
        """ testing zunk """

        # 1. mark as cleared
        # 2. set data, if any
        # 3. send signal
        
        self.storage.set_value("cleared", "true")
        self.storage.set_value("method", payment_method)

class PickledPayment(Payment):

    # FIXME: Requires a load to unpickle from the file based on the
    # code. Call load() in an __init__().

    def get_value(self, key):
        return self.values[key]

    def set_value(self, key, value):
        # print "set_value() of PickledPayment() called: %s=%s" % (key, value)
        self.values[key] = value
        return value

    def save(self):
        import pickle
        fh = open("%s.pickle" % self.code, "w")
        pickle.dump(self.values, fh)
        fh.close()
