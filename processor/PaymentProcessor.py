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
            data[key] = value

        # set fixed merchant data
        for key, value in self.DATA_MERCHANT.items():
            value = self.PARAMETERS[value]
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

        # set variable payment data
        for key, value in self.DATA_PAYMENT.items():
            value = payment.get_value(value)
            data[key] = value

        # FIXME: The URLs set are missing the protocol and host/port parts!

        # set return urls
        for key, value in self.DATA_URLS.items():
            value = "/payment/%s/%s/%s/" % \
                (value, self.METHOD, payment.code)
            data[key] = value                

        # get custom data
        data.update(self.checkout_hash(data))

        # FIXME: Itemized cart data for Paypal et al is not done.
            
        return data

    @classmethod
    def success(self, request, payment_method, payment_code):
        raise NotImplementedError("method not implemented for the processor")

class PaymentProcessingError(Exception):
    pass

from django.http import HttpResponseRedirect

def success_view(request, payment_method, payment_code):

    # FIXME: lookup payment already here based on the code

    # FIXME: should probably do something different on error

    pp = PaymentProcessor.get_processor(payment_method)
    try:        
        pp.success(request, payment_method, payment_code)
        #return HttpResponseRedirect(pp.PARAMETERS["return_url"] % payment_code)
    except PaymentProcessingError:
        pass
        #return HttpResponseRedirect(pp.PARAMETERS["return_url"] % payment_code)



    # what about the refund hooks?

    # what about the payment check hooks?
