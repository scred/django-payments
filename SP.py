# single payment, rename Payment

# first you create a payment, then somehow you go for the checkout

# checkout is a different view, not handled by this code, but there
# needs to be a way to query for payment methods and forms per
# method. do we get the methods from the payment?

# do we need a payment data storage class
# the storage class needs to be registered for the payment class

class Payment():

    # need states

    # before clearing: methods that are available
    # after clearing: method that was used

    storage = None

    @classmethod
    def register_storage(self, klass):
        self.storage = klass

    def __init__(self):

        self.payment_methods = []
        self.cart = None
        self.recipient = None

        # how to create the payment

        pass

    def get_checkout_form(self, payment_method):

        pp = PaymentProcessor.get_processor(payment_method)
        return pp.get_checkout_form(self)

    def success(payment_method):

        # 1. mark as cleared
        # 2. set data, if any
        # 3. send signal
        
        self.storage.set_value("cleared", "true")
        self.storage.set_value("method", payment_method)
        
        pass

class PickledPayment(Payment):

    def get_value(self, key):
        pass

    def set_value(self, key, value):
        pass
