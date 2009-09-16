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
    def set_parameters(self, payment_method, data):
        pp = self.get_processor(payment_method)
        pp.PARAMETERS = data
        # FIXME: should have an add parameter thing as well

    @classmethod
    def get_parameter(self, key):
        import settings
        return settings.PAYMENT_PROCESSORS[self.METHOD][key]
        # return getattr(settings, "PAYMENT_PROCESSORS")[self.METHOD][key]

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

        # FIXME: Need to somehow formalize this a bit and return an
        # actual Django form instance.
        
        data = {}

        # set payment method fixed data
        for key, value in self.DATA_FIXED.items():
            data[key] = value

        # set fixed merchant data
        for key, value in self.DATA_MERCHANT.items():
            value = self.get_parameter(value)
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
            value = "http://localhost:8001/payment/%s/%s/%s/" % \
                (value, self.METHOD, payment.code)
            data[key] = value                

        # get custom data
        data.update(self.checkout_hash(data))

        # FIXME: Itemized cart data for Paypal et al is not done.
            
        return data

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

        # call processor hooks
        self.success_check_mac(request, payment)
        self.success_check_custom(request, payment)
        # ...
        
        from SP import Payment

        # FIXME: activate these two lines
        # payment = Payment.lookup(payment_code)
        # payment.success(self.METHOD)
        
        # print "payment:", payment
        #print "payment:", type(payment)

        # FIXME: all ok, now need to do a redirect

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

from django.http import HttpResponseRedirect

def success_view(request, payment_method, payment_code):

    # FIXME: lookup payment already here based on the code

    # FIXME: should probably do something different on error

    pp = PaymentProcessor.get_processor(payment_method)

    # FIXME: lookup the payment here

    from SP import Payment, PickledStorage
    Payment.set_storage(PickledStorage)

    payment = Payment.lookup(payment_code)

    print "foo:", pp.get_parameter("merchant_secret")
    try:
        
        pp.success(request, payment)
        return HttpResponseRedirect(pp.get_parameter("return_url") % payment_code)
    except PaymentProcessingError:
        return HttpResponseRedirect(pp.get_parameter("return_url") % payment_code)

    # what about the refund hooks?

    # what about the payment check hooks?
