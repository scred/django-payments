from processor import PaymentProcessor, MaksunapitPaymentProcessor

class NordeaPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Payment processor for Nordea's E-maksu.

    Region(s): FI

    Specifications:
      http://bit.ly/2K2tIn (in Finnish, PDF)
    
    Merchant credentials for testing:
      merchant_key = "12345678"
      merchant_secret = "LEHTI"
      merchant_account = "29501800000014"
    """

    METHOD = "nordea"
    URL = "FIXME"

    PARAMETERS = {}

    DATA_FIXED = {
        "SOLOPMT_VERSION": "0003",
        "SOLOPMT_CONFIRM": "YES",
        "SOLOPMT_DATE": "EXPRESS",
    }

    DATA_MERCHANT = {
        "SOLOPMT_RCV_ID": "merchant_key",
        "SOLOPMT_RCV_NAME": "merchant_name",
        "SOLOPMT_RCV_ACCOUNT": "merchant_account",
        # "merchant_secret"
    }

    CURRENCY = {
        "EUR": "EUR",
    }
    CURRENCY_PARAM = "SOLOPMT_CUR"
    CURRENCY_DEFAULT = "EUR"

    LANGUAGE = {
        "fi": "1",
        "sv": "2",
        "en": "3",
    }
    LANGUAGE_PARAM = "SOLOPMT_LANGUAGE"
    LANGUAGE_DEFAULT = "en"

    DATA_PAYMENT = {
        "SOLOPMT_AMOUNT": "amount",
        "SOLOPMT_STAMP": "code",
        "SOLOPMT_REF": "fi_reference",
        "SOLOPMT_MSG": "message",
    }

    DATA_URLS = {
        "SOLOPMT_RETURN": "success",
        "SOLOPMT_CANCEL": "cancel",
        "SOLOPMT_REJECT": "error",
    }

    PAYMENT_REQ_MAC = "MAC"
    PAYMENT_REQ_PARAMS = (
        ("SOLOPMT_VERSION", "data"),
        ("SOLOPMT_STAMP", "data"),
        ("SOLOPMT_RCV_ID", "data"),
        ("SOLOPMT_AMOUNT", "data"),
        ("SOLOPMT_REF", "data"),
        ("SOLOPMT_DATE", "data"),
        ("SOLOPMT_CUR", "data"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_REQ_SEPARATOR = "&"

    PAYMENT_RESP_MAC = "SOLOPMT_RETURN_MAC"
    PAYMENT_RESP_PARAMS = (
        ("SOLOPMT_RETURN_VERSION", "GET"),
        ("SOLOPMT_RETURN_STAMP","GET"),
        ("SOLOPMT_RETURN_REF", "GET"),
        ("SOLOPMT_RETURN_PAID", "GET"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_RESP_SEPARATOR = "&"

    # KEYVERS: ??

PaymentProcessor.register_processor(NordeaPaymentProcessor)
