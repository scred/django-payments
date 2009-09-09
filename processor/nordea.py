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

    PAYMENT_REQ_MAC = "MAC"
    PAYMENT_REQ_PARAMS = (
        ("SOLOPMT_VERSION", "data"), # 
        ("SOLOPMT_STAMP", "data"), # SOLOPMT_STAMP
        ("SOLOPMT_RCV_ID", "data"), # SOLOPMT_RCV_ID
        ("SOLOPMT_AMOUNT", "data"), # SOLOPMT_AMOUNT
        ("SOLOPMT_REF", "data"), # SOLOPMT_REF
        ("SOLOPMT_DATE", "data"), # SOLOPMT_DATE
        ("SOLOPMT_CUR", "data"), # SOLOPMT_CUR
        ("merchant_secret", "processor"),
    )
    PAYMENT_REQ_SEPARATOR = "&"

    # urls
    # RETURN
    # CANCEL
    # REJECT

    # KEYVERS: ??
    
    # how to get the parameters

    # what about the refund hooks?

    # what about the payment check hooks?

    # classmethods needed for setting fixed merchant parameters (done
    # in eg settings.py)

PaymentProcessor.register_processor("nordea", NordeaPaymentProcessor)
