from processor import PaymentProcessor, MaksunapitPaymentProcessor

class NordeaPaymentProcessor(MaksunapitPaymentProcessor):

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

    # MAC_PARAMS_IN = None
    # MAC_PARAMS_OUT = None

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

PaymentProcessor.register_processor("nordea", NordeaPaymentProcessor)
