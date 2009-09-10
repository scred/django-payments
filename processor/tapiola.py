# -*- coding: iso-8859-9 -*-

from processor import PaymentProcessor, MaksunapitPaymentProcessor

class TapiolaPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Payment processor for Tapiola Verkkomaksupalvelu.

    Note: Tapiola uses the same banking system vendor (Crosskey) as
    Ålandsbanken and S-Pankki. With minor modifications this
    processing module should work with those banks as well.

    Region(s): FI

    Specifications:
      http://bit.ly/dRz1i (in Finnish, PDF) [Tapiola]
      http://bit.ly/c9hXd (in Finnish, PDF) [S-Pankki]
      ?? (in Finnish, PDF) [Ålandsbanken]
    
    Merchant credentials for testing:
      merchant_key = "TAPESHOPID"
      merchant_secret = "PAPUKAIJA"
      merchant_account = "2019363630-01652643"

    Client credentials for testing:
      username = "12345678"
      password = "999"      
    """

    METHOD = "tapiola"

    URL = "https://pankki.tapiola.fi/tap_bv/ebank/auth/initLogin.do"
    BUTTON_URL = "FIXME"

    PARAMETERS = {}

    DATA_FIXED = {
        "AAB_VERSION": "0002",
        "AAB_CONFIRM": "YES",
        "AAB_DATE": "EXPRESS",
        "AAB_KEYVERS": "0001",
        "BV_UseBVCookie": "NO",
    }

    DATA_MERCHANT = {
        "AAB_RCV_ID": "merchant_key",
        "AAB_RCV_NAME": "merchant_name",
        "AAB_RCV_ACCOUNT": "merchant_account",
        # "merchant_secret"
    }

    CURRENCY = {
        "EUR": "EUR",
    }
    CURRENCY_PARAM = "AAB_CUR"
    CURRENCY_DEFAULT = "EUR"

    LANGUAGE = {
        "fi": "1",
        "sv": "2",
    }
    LANGUAGE_PARAM = "AAB_LANGUAGE"
    LANGUAGE_DEFAULT = "fi"

    DATA_PAYMENT = {
        "AAB_AMOUNT": "amount",
        "AAB_STAMP": "code",
        "AAB_REF": "fi_reference",
        "AAB_MSG": "message",
    }

    DATA_URLS = {
        "AAB_RETURN": "success",
        "AAB_CANCEL": "cancel",
        "AAB_REJECT": "error",
    }

    PAYMENT_REQ_MAC = "AAB_MAC"
    PAYMENT_REQ_PARAMS = (
        ("AAB_VERSION", "data"),
        ("AAB_STAMP", "data"),
        ("AAB_RCV_ID", "data"),
        ("AAB_AMOUNT", "data"),
        ("AAB_REF", "data"),
        ("AAB_DATE", "data"),
        ("AAB_CUR", "data"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_REQ_SEPARATOR = "&"

    PAYMENT_RESP_MAC = "AAB-RETURN-MAC"
    PAYMENT_RESP_PARAMS = (
        ("AAB-RETURN-VERSION", "GET"),
        ("AAB-RETURN-STAMP","GET"),
        ("AAB-RETURN-REF", "GET"),
        ("AAB-RETURN-PAID", "GET"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_RESP_SEPARATOR = "&"

PaymentProcessor.register_processor(TapiolaPaymentProcessor)
