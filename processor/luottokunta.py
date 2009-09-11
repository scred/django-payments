from processor import PaymentProcessor

class LuottokuntaPaymentProcessor(PaymentProcessor):

    """
    Payment processor for credit card billing by Luottokunta.

    Region(s): FI

    Specifications:
      ?? (in Finnish, PDF)
    
    Merchant credentials for testing:
      merchant_key = "??"
      merchant_secret = "??"
      merchant_account = "??"

    Client credentials for testing:
      Use valid credit card and cancel charges from the admin UI, or
      alternatively contact Luottokunta to set the gateway for
      specific merchant key to testing mode.
    """

    METHOD = "luottokunta"

    URL = "FIXME"
    BUTTON_URL = "FIXME"

    PARAMETERS = {}

    DATA_FIXED = {
        "Card_Details_Transmit": "0",
        "Device_Category": "1",
        "Transaction_
        #"SOLOPMT_VERSION": "0003",
        #"SOLOPMT_CONFIRM": "YES",
        #"SOLOPMT_DATE": "EXPRESS",
    }

    # FIXME: KEYVERS: needed or not

    DATA_MERCHANT = {
        "Merchant_Number": "merchant_key",
        #"SOLOPMT_RCV_NAME": "merchant_name",
        #"SOLOPMT_RCV_ACCOUNT": "merchant_account",
        # "merchant_secret"
    }

    CURRENCY = {
        "EUR": "978",
    }
    CURRENCY_PARAM = "Currency_Code"
    CURRENCY_DEFAULT = "EUR"

    LANGUAGE = {
        "fi": "FI",
        "sv": "SV",
        "en": "EN",
    }
    LANGUAGE_PARAM = "Language"
    LANGUAGE_DEFAULT = "en"

    DATA_PAYMENT = {
        "Order_ID", "code",
        #"Customer_ID", "FIXME", 

        "Amount": "amount",
        #"SOLOPMT_REF": "fi_reference",
        #"SOLOPMT_MSG": "message",
    }

    DATA_URLS = {
        #"SOLOPMT_RETURN": "success",
        #"SOLOPMT_CANCEL": "cancel",
        #"SOLOPMT_REJECT": "error",
    }

    PAYMENT_REQ_MAC = "SOLOPMT_MAC"
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

PaymentProcessor.register_processor(LuottokuntaPaymentProcessor)
