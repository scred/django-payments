from processor import PaymentProcessor, MaksunapitPaymentProcessor

class OpPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Payment processor for Osuuspankki (OP) Verkkomaksu.

    Region(s): FI

    Specifications:
      http://bit.ly/1ZsMGk (in Finnish, HTML)
    
    Merchant credentials for testing:
      merchant_key = "Esittelymyyja"
      merchant_secret = "Esittelykauppiaansalainentunnus"

    Client credentials for testing:
      username = "123456"
      password = "7890"
    """

    METHOD = "op"

    URL = "https://kultaraha.op.fi/cgi-bin/krcgi"
    BUTTON_URL = ""

    PARAMETERS = {}

    DATA_FIXED = {
        "action_id": "701",
        "VERSIO": "1",
        "TARKISTE-VERSIO": "1", # FIXME: might need to be flexible
        "VAHVISTE": "K",
    }

    DATA_MERCHANT = {
        "MYYJA": "merchant_key",
        # "merchant_secret"
    }

    CURRENCY = {
        "EUR": "EUR",
    }
    CURRENCY_PARAM = "VALUUTTALAJI"
    CURRENCY_DEFAULT = "EUR"

    LANGUAGE = {
        "fi": "1",
        "sv": "2",
        "en": "3",
    }
    LANGUAGE_PARAM = "LANGUAGE"
    LANGUAGE_DEFAULT = "en"

    DATA_PAYMENT = {
        "SUMMA": "amount",
        "MAKSUTUNNUS": "code",
        "VIITE": "fi_reference",
        "VIESTI": "message",
    }

    DATA_URLS = {
        "PALUU-LINKKI": "success",
        "PERUUTUS-LINKKI": "cancel",
    }

    PAYMENT_REQ_MAC = "TARKISTE"
    PAYMENT_REQ_PARAMS = (
        ("VERSIO", "data"),
        ("MAKSUTUNNUS", "data"),
        ("MYYJA", "data"),
        ("SUMMA", "data"),
        ("VIITE", "data"),
        ("VALUUTTALAJI", "data"),
        ("TARKISTE-VERSIO", "data"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_REQ_SEPARATOR = ""

    PAYMENT_RESP_MAC = "TARKISTE"
    PAYMENT_RESP_PARAMS = (
        ("VERSIO", "GET"),
        ("MAKSUTUNNUS","GET"),
        ("VIITE", "GET"),
        ("ARKISTOINTITUNNUS", "GET"),
        ("TARKISTEVERSIO", "GET"),        
        ("merchant_secret", "processor"),
    )
    PAYMENT_RESP_SEPARATOR = ""

PaymentProcessor.register_processor(OpPaymentProcessor)
