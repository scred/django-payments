
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

class SampoPaymentProcessor(PaymentProcessor):

    pass

PaymentProcessor.register_processor("sampo", SampoPaymentProcessor)

class NordeaPaymentProcessor(PaymentProcessor):

    """
    Payment processor for Nordea's "E-maksu".

    Region(s): FI

    Specifications:
      http://bit.ly/2K2tIn (in Finnish, PDF)
    
    Merchant credentials for testing:
      merchant_key = "12345678"
      merchant_secret = "LEHTI"
      merchant_account = "29501800000014"
    """

    PREFIX = "SOLOPMT_"

    PARAMETERS = {}

    DATA_FIXED = {
        "VERSION": "0003",
        "CONFIRM": "YES",
        "DATE": "EXPRESS",
    }

    DATA_MERCHANT = {
        "RCV_ID": "merchant_key",
        "RCV_NAME": "merchant_name",
        "RCV_ACCOUNT": "merchant_account",
        # "merchant_secret"
    }

    CURRENCY = {
        "EUR": "EUR",
    }
    CURRENCY_PARAM = "CUR"
    CURRENCY_DEFAULT = "EUR"

    LANGUAGE = {
        "fi": "1",
        "sv": "2",
        "en": "3",
    }
    LANGUAGE_PARAM = "LANGUAGE"
    LANGUAGE_DEFAULT = "en"

    DATA_PAYMENT = {
        "AMOUNT": "amount",
        "STAMP": "code",
        "REF": "fi_reference",
        "MSG": "message",
    }

    MAC_PARAMS_IN = None
    MAC_PARAMS_OUT = None

    #merchant_key
    #merchant_secret
    #merchant_account
    #merchant_name

    # urls
    # RETURN
    # CANCEL
    # REJECT

    # MAC

    # KEYVERS
    
    # how to get the parameters

    # what about the refund hooks?

    # what about the payment check hooks?

    # classmethods needed for setting fixed merchant parameters (done
    # in eg settings.py)

    def success(request, payment_method, payment_code):

        nordea = settings.PAYMENTS['nordea']

        # use hashlib instead of md5

        # the check with all maksunapit is the same, we could somehow
        # abstract this

        # FIXME: store an audit event here

        payment = None # FIXME

        MAC = "SOLOPMT_RETURN_MAC"
        MACP = (
            ("SOLOPMT_RETURN_VERSION", 'GET',),
            ("SOLOPMT_RETURN_STAMP",'GET',),
            ("SOLOPMT_RETURN_REF",'GET',),
            ("SOLOPMT_RETURN_PAID", 'GET',),
            ("merchant_secret", "processor",),
        )
        MAC_SEPARATOR = "&"

        m = md5.new()
        for (var, source) in MACP:
            if source == 'GET':
                m.update(request.GET.get(var, ''))
            elif source == 'POST':
                m.update(request.POST.get(var, ''))
            elif source == 'processor':
                m.update(payment.get_value(var))
            else:
                pass
            m.update("&")

        return_mac = request.GET.get("SOLOPMT_RETURN_MAC", "")
        if m.hexdigest().upper() != return_mac.upper():
            raise PaymentProcessingError("Return MAC doesn't match!")

        # checked validity of the return

        # then use super to send the signal? (but paypal doesn't work
        # that way)

        # should we check the payment value and stuff like that?

        # who makes the call for audit?

        # 1. lookup payment
        # 2. call the success() of the payment (with method) ?
        # 3. return redirect to the payment's ok url

    @classmethod
    def get_checkout_form(self, payment):

        # this should probably be with the super class and be automated
        
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

PaymentProcessor.register_processor("nordea", NordeaPaymentProcessor)
    

def success_view(request, payment_method, payment_code):

    # Q: how to set the return url? on a per processor basis, or on a
    # per payable (/payment) basis?

    # catch PaymentProcessingException?

    pp = PaymentProcessor.get_processor(payment_method)
    return pp.success(request, payment_method, payment_code)
