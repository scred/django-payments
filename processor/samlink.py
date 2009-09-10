from processor import PaymentProcessor, MaksunapitPaymentProcessor

class SamlinkPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Payment processor for Samlink SP/POP/AKTIA-maksu.

    Region(s): FI

    Specifications:
      ?? (in Finnish, HTML)
    
    Merchant credentials for testing:
      merchant_key = "0000000000"
      merchant_secret = "11111111111111111111"
      merchant_account = "448710-126"

    Client credentials for testing:
      username = "11111111"
      password = "123456"
    """

    METHOD = "samlink"

    URL = "https://verkkomaksu.inetpankki.samlink.fi/vm/login.html"
    BUTTON_URL = "FIXME"

    PARAMETERS = {}

    DATA_FIXED = {
        "NET_VERSION": "001",
        "NET_CONFIRM": "YES",
        "NET_DATE": "EXPRESS",
    }

    DATA_MERCHANT = {
        "NET_SELLER_ID": "merchant_key",
        #"NET_SELLER_NAME": "merchant_name",
        #"NET_SELLER_ACCOUNT": "merchant_account",
        # "merchant_secret"
    }

    CURRENCY = {
        "EUR": "EUR",
    }
    CURRENCY_PARAM = "NET_CUR"
    CURRENCY_DEFAULT = "EUR"

    LANGUAGE = {
        "fi": "1",
        "sv": "2",
        "en": "3",
    }
    LANGUAGE_PARAM = "NET_LANG"
    LANGUAGE_DEFAULT = "en"

    DATA_PAYMENT = {
        "NET_AMOUNT": "amount",
        "NET_STAMP": "code",
        "NET_REF": "fi_reference",
        "NET_MSG": "message",
    }

    DATA_URLS = {
        "NET_RETURN": "success",
        "NET_CANCEL": "cancel",
        "NET_REJECT": "error",
    }

    PAYMENT_REQ_MAC = "NET_MAC"
    PAYMENT_REQ_PARAMS = (
        ("NET_VERSION", "data"),
        ("NET_STAMP", "data"),
        ("NET_SELLER_ID", "data"),
        ("NET_AMOUNT", "data"),
        ("NET_REF", "data"),
        ("NET_DATE", "data"),
        ("NET_CUR", "data"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_REQ_SEPARATOR = "&"

    PAYMENT_RESP_MAC = "NET_RETURN_MAC"
    PAYMENT_RESP_PARAMS = (
        ("NET_RETURN_VERSION", "GET"),
        ("NET_RETURN_STAMP","GET"),
        ("NET_RETURN_REF", "GET"),
        ("NET_RETURN_PAID", "GET"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_RESP_SEPARATOR = "&"

PaymentProcessor.register_processor(SamlinkPaymentProcessor)
