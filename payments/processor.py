import settings
from exceptions import PaymentProcessingError

class PaymentProcessor():
    """
    Base class for different payment processors. Not to be used directly.
    """

    payment_processors = {}

    @classmethod
    def register_processor(self, klass):
        """
        Register a new payment processor sub-class.
        """
        self.payment_processors[klass.METHOD] = klass

    @classmethod
    def get_processor(self, kind):
        return self.payment_processors[kind]

    @classmethod
    def get_setting(self, key):
        return settings.PAYMENT_PROCESSORS[self.METHOD][key]
        # return getattr(settings, "PAYMENT_PROCESSORS")[self.METHOD][key]

    @classmethod
    def get_parameter(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            return None

    def __init__(FIXME):

        # params:
        # urls dict
        # cart
        # receiver etc
        
        pass

    # class method to set auditing class
    # class method to set payables?

    @classmethod
    def get_checkout_url(self):
        return self.URL

    @classmethod
    def get_checkout_params(self, payment):

        # FIXME: Need to somehow formalize this a bit and return an
        # actual Django form instance.
        
        data = {}

        # set payment method fixed data
        for key, value in self.DATA_FIXED.items():
            data[key] = value

        # set fixed merchant data
        for key, value in self.DATA_MERCHANT.items():
            value = self.get_setting(value)
            data[key] = value

        # set language
        data[self.LANGUAGE_PARAM] = self.LANGUAGE_DEFAULT
        language = payment.get_value("language")
        if language and language in self.LANGUAGE:
            data[self.LANGUAGE_PARAM] = self.LANGUAGE[language]

        # set currency
        data[self.CURRENCY_PARAM] = self.CURRENCY_DEFAULT
        currency = payment.get_value("currency")
        if currency and currency in self.CURRENCY:
            data[self.CURRENCY_PARAM] = self.CURRENCY[currency]

        # FIXME: This way of massaging the amount is a hack. Should be
        # able to register on a per parameter basis these massaging
        # functions for various payment parameters. That would allow
        # for flexibility on a per payment method basis.

        # set variable payment data
        for key, var in self.DATA_PAYMENT.items():
            value = payment.get_value(var)
            if var == 'amount':
                value = self.massage_amount(value)
            data[key] = value

        # FIXME: The URLs set are missing the protocol and host/port parts!
        # FIXME: Are not, but they're hardwired!

        # set return urls
        for key, value in self.DATA_URLS.items():
            value = "%s/%s/%s/%s/" % \
                (settings.PAYMENT_PROCESSOR_URL,
                 value, self.METHOD, payment.code)
            data[key] = value                

        # get custom data
        data.update(self.checkout_hash(data))

        print "USE_CART:", self.get_parameter("USE_CAR")

        if self.get_parameter("USE_CART"):
            items = payment.get_items()
            for i in range(0, len(items)):
                for key, value in self.DATA_CART.items():
                    data[key % (i+1)] = items[i][value]
            
        return data

    @classmethod
    def checkout_hash(self, data):
        return {}

    @classmethod
    def massage_amount(self, value):
        return value

    @classmethod
    def success(self, request, payment):
        """
        Returned with success URL from the payment processor. Checking
        for return parameters and saving payment status need to be
        done.
        """

        # call processor validation hooks
        self.success_check_mac(request, payment)
        self.success_check_custom(request, payment)
        # ...

        # everything checks okay, store the status
        payment.set_status("success")
        payment.set_value("payment_method", self.METHOD)
        payment.set_value("processor_reference", "FIXME")

        return payment.success()
        
        # should we check the payment value and stuff like that?
        # who makes the call for audit?

    @classmethod
    def success_check_mac(self, request, payment):
        """
        Checks the payment success return parameters (GET or POST) and
        the associated MAC provided by the payment processor.

        If MAC checking is not required, do not define this method for
        the processing class. If MAC is invalid, the the method should
        raise PaymentInvalidMacError.
        """
        pass

    @classmethod
    def success_check_custom(self, request, payment):
        pass

    @classmethod
    def query(self, payment):
        raise NotImplementedError("Query interface not implemented: %s" %
                                  self.METHOD)

    @classmethod
    def refund(self, payment):
        raise NotImplementedError("Refund interface not implemented: %s" %
                                  self.METHOD)
