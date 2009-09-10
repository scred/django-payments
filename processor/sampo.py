from processor import PaymentProcessor, MaksunapitPaymentProcessor

class SampoPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Specification:
      http://bit.ly/ZURkl (in Finnish, PDF)

    Merchant credentials for testing:
      merchant_key = "000000000000"
      merchant_secret = "jumCLB4T2ceZWGJ9ztjuhn5FaeZnTm5HpfDXWU2APRqfDcsrBs8mqkFARzm7uXKd"
    """

    PREFIX = ""

    PARAMETERS = {}

    DATA_FIXED = {
        "VERSIO": "3",
    }

    DATA_MERCHANT = {
        "KNRO": "merchant_key",
        # "merchant_secret"
    }

    CURRENCY = {
        "EUR": "EUR",
    }
    CURRENCY_PARAM = "VALUUTTA"
    CURRENCY_DEFAULT = "EUR"

    LANGUAGE = {
        "fi": "1",
        "sv": "2",
        "en": "3",
    }
    LANGUAGE_PARAM = "lng"
    LANGUAGE_DEFAULT = "en"

    DATA_PAYMENT = {
        "SUMMA": "amount",
        "VIITE": "fi_reference",
    }

    PAYMENT_REQ_MAC = "TARKISTE"
    PAYMENT_REQ_PARAMS = (
        ("merchant_secret", "processor"),
        ("SUMMA", "data"),
        ("VIITE", "data"),
        ("KNRO", "data"),
        ("VERSIO", "data"),
        ("VALUUTTA", "data"),
        # ("OKURL", "data"), # FIXME
        # ("VIRHEURL", "data"), # FIXME
    )
    PAYMENT_REQ_SEPARATOR = ""

    # OKURL
    # VIRHEURL

PaymentProcessor.register_processor("sampo", SampoPaymentProcessor)