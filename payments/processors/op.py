from payments import PaymentProcessor, MaksunapitPaymentProcessor

class OpPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Payment processor for Osuuspankki (OP) Verkkomaksu.

    Features: authcap, query

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
    QUERY_URL = "https://kultaraha.op.fi/cgi-bin/krcgi"
    BUTTON_URL = "FIXME"

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
        ("MAKSUTUNNUS", "GET"),
        ("VIITE", "GET"),
        ("ARKISTOINTITUNNUS", "GET"),
        ("TARKISTEVERSIO", "GET"),        
        ("merchant_secret", "processor"),
    )
    PAYMENT_RESP_SEPARATOR = ""

    COST_FIXED = "0.34"
    COST_PERCENTAGE = "0.00"

    @classmethod
    def query(self, payment):
        """
        Automated query for payment status.

        For testing use parameters MAKSUTUNNUS='1997060417052135',
        VIITE='13' and the normal testing merchant credentials.

        FIXME: Works as far as the POST to the bank is
        concerned. Returns a HTML page which has a link that points to
        PALUU-LINKKI. Should be clicked to ensure that the query
        results are recorded. No view or anything is currently
        implemented to handle the PALUU-LINKKI URL.
        """

        import urllib2
        from urllib import urlencode
        import cgi

        data = {}

        data["action_id"] = "708"
        data["VERSIO"] = "0006"
        data["MYYJA"] = self.get_setting("merchant_key")
        data["KYSELYTUNNUS"] = "FIXME"
        data["MAKSUTUNNUS"] = payment.get_value("code")
        data["VIITE"] = payment.get_value("fi_reference")
        data["TARKISTE-VERSIO"] = "6"
        data["PALUU-LINKKI"] = "http://quatloo.dev.scred.com:2345/payment/ping/op-query-response/%s/" % payment.get_value("code") # FIXME
        
        order = ("VERSIO", "MYYJA", "KYSELYTUNNUS", "MAKSUTUNNUS",
                 "VIITE", "TARKISTE-VERSIO", "secret")

        s = ""
        for p in order:
            if p == "secret":
                s += self.get_setting("merchant_secret")
            else:
                s += data[p]

        import md5
        m = md5.new(s)
        data["TARKISTE"] = m.hexdigest().upper()
        
        con = urllib2.urlopen(self.QUERY_URL, urlencode(data))
        resp = con.read()
        print resp

        #respdata = cgi.parse_qs(resp)

        # No response MAC is sent.

        return

        if respdata["ReturnCode"] == "000":
            return (True, respdata)
        else:
            return (False, respdata)

PaymentProcessor.register_processor(OpPaymentProcessor)
