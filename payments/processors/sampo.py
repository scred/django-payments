from payments import PaymentProcessor, MaksunapitPaymentProcessor

class SampoPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Payment processor for Sampo Pankki Verkkomaksupalvelu.

    Features: authcap, (query)

    Region(s): FI

    Specification:
      http://bit.ly/ZURkl (in Finnish, PDF)

    Merchant credentials for testing:
      merchant_key = "000000000000"
      merchant_secret = "jumCLB4T2ceZWGJ9ztjuhn5FaeZnTm5HpfDXWU2APRqfDcsrBs8mqkFARzm7uXKd"

    Client credentials for testing:
      There are no separate client credentials for testing. Normal
      production credentials are to be used, but ne credit transfers
      will be effected nor service fees charged.
    """

    # FATAL: What about cancelled returns? Do they have response MAC
    # (something that can be replayed as successes)?

    METHOD = "sampo"
    API_VERSION = "3"

    URL = "https://verkkopankki.sampopankki.fi/SP/vemaha/VemahaApp"
    QUERY_URL = "https://netbank.danskebank.dk/HB"
    BUTTON_URL = "https://www.sampopankki.fi/verkkopalvelu/logo.gif"

    PARAMETERS = {}

    DATA_FIXED = {
        "VERSIO": API_VERSION,
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

    DATA_URLS = {
        "OKURL": "success",
        "VIRHEURL": "error",
    }

    PAYMENT_REQ_MAC = "TARKISTE"
    PAYMENT_REQ_PARAMS = (
        ("merchant_secret", "processor"),
        ("SUMMA", "data"),
        ("VIITE", "data"),
        ("KNRO", "data"),
        ("VERSIO", "data"),
        ("VALUUTTA", "data"),
        ("OKURL", "data"),
        ("VIRHEURL", "data"),
    )
    PAYMENT_REQ_SEPARATOR = ""

    PAYMENT_RESP_MAC = "TARKISTE"
    PAYMENT_RESP_PARAMS = (
        ("merchant_secret", "processor"),
        ("fi_reference", "payment"), # VIITE
        ("SUMMA", "GET"),
        ("STATUS", "GET"),
        ("KNRO", "GET"),
        (API_VERSION, "fixed"), # VERSIO
        ("VALUUTTA", "GET"),
    )
    PAYMENT_RESP_SEPARATOR = ""
    PAYMENT_RESP_PROCESSOR_REFERENCE = None

    COST_FIXED = "0.35"
    COST_PERCENTAGE = "0.00"

    @classmethod
    def query(self, payment):
        """
        Automated query for payment status.
        """

        import urllib2
        from urllib import urlencode
        import cgi

        data = {}

        data["Refno"] = payment.get_value("fi_reference")
        data["MerchantID"] = self.get_setting("merchant_key")
        data["gsAftlnr"] = "foobar" # FIXME: wtf is this
        data["gsSprog"] = "EN"
        data["gsProdukt"] = "IBV"
        data["gsNextObj"] = "InetPayV"
        data["gsNextAkt"] = "InetPaySt"
        data["Version"] = "0001"
        data["gsResp"] = "S"
        
        order = ("secret", "MerchantID", "Refno")

        s = ""
        for p in order:
            if p == "secret":
                s += self.get_setting("merchant_secret")
            else:
                s += data[p]

        import md5
        m = md5.new(s)
        data["VerifyCode"] = m.hexdigest().upper()
        
        con = urllib2.urlopen(self.QUERY_URL, urlencode(data))
        resp = con.read()

        respdata = cgi.parse_qs(resp)

        # No response MAC is sent.

        if respdata["ReturnCode"] == "000":
            return (True, respdata)
        else:
            return (False, respdata)

PaymentProcessor.register_processor(SampoPaymentProcessor)
