class PaymentProcessor():

    payment_processors = {}

    @classmethod
    def register_processor(self, kind, klass):
        """
        Register a new payment processor sub-class.
        """
        self.payment_processors[kind] = klass

    @classmethod
    def get_processor(self, kind):
        return self.payment_processors[kind]

    @classmethod
    def set_parameters(self, payment_method, data):
        pp = self.get_processor(payment_method)
        pp.PARAMETERS = data
        # FIXME: should have an add parameter thing as well

    def __init__(FIXME):

        # params:
        # urls dict
        # cart
        # receiver etc
        
        pass

    # class method to set auditing class
    # class method to set payables?

    @classmethod
    def get_checkout_form(self, payment):
        
        data = {}

        # set payment method fixed data
        for key, value in self.DATA_FIXED.items():
            data["%s%s" % (self.PREFIX, key)] = value

        # set fixed merchant data
        for key, value in self.DATA_MERCHANT.items():
            value = self.PARAMETERS[value]
            data["%s%s" % (self.PREFIX, key)] = value

        # set language
        data["%s%s" % (self.PREFIX, self.LANGUAGE_PARAM)] = \
            self.LANGUAGE_DEFAULT
        language = payment.get_value("language")
        if language and language in self.LANGUAGE:
            data["%s%s" % (self.PREFIX, self.LANGUAGE_PARAM)] = \
                self.LANGUAGE[language]

        # set currency
        data["%s%s" % (self.PREFIX, self.CURRENCY_PARAM)] = \
            self.CURRENCY_DEFAULT
        currency = payment.get_value("currency")
        if currency and currency in self.CURRENCY:
            data["%s%s" % (self.PREFIX, self.CURRENCY_PARAM)] = \
                self.CURRENCY[currency]

        # set variable payment data
        for key, value in self.DATA_PAYMENT.items():
            value = payment.get_value(value)
            data["%s%s" % (self.PREFIX, key)] = value

        return data

        # raise NotImplementedError("method not implemented for the processor")


    

def success_view(request, payment_method, payment_code):

    # Q: how to set the return url? on a per processor basis, or on a
    # per payable (/payment) basis?

    # catch PaymentProcessingException?

    pp = PaymentProcessor.get_processor(payment_method)
    return pp.success(request, payment_method, payment_code)
