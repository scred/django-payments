from processor import PaymentProcessor, MaksunapitPaymentProcessor

class SamlinkPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Payment processor for Samlink SP/POP/AKTIA-maksu.

    Note: With rather minor modifications this module would work also
    with Handelsbanken who also use Samlink as a technology provider.

    Features: authcap, (query)

    Region(s): FI

    Specifications:
      ??
      http://bit.ly/6XWNf (in Finnish, PDF) [Handelsbanken]
    
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
    QUERY_URL = "https://verkkomaksu.inetpankki.samlink.fi/vm/kysely.html"
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

    @classmethod
    def query(self, payment):
        """
        Automated query for payment status.
        """

        import urllib2
        from urllib import urlencode
        import cgi

        data = {}

        data["NET_VERSION"] = "001"
        data["NET_SELLER_ID"] = self.get_setting("merchant_key")
        data["NET_STAMP"] = payment.get_value("code")
        data["NET_REF"] = payment.get_value("fi_reference")
        data["NET_RETURN"] = "http://quatloo.dev.scred.com:2345/payment/ping/samlink-query-response/%s/" % payment.get_value("code") # FIXME
        data["NET_RETURN"] = "http://localhost:8002/payment/ping/samlink-query-response/%s/" % payment.get_value("code") # FIXME        
        order = ("NET_VERSION", "NET_SELLER_ID", "NET_STAMP", "NET_REF",
                 "secret")

        s = ""
        for p in order:
            if p == "secret":
                s += self.get_setting("merchant_secret") + "&"
            else:
                s += data[p] + "&"

        import md5
        m = md5.new(s)
        data["NET_MAC"] = m.hexdigest().upper()

        #return

#        data = {
#            "NET_VERSION": "001",
#            "NET_SELLER_ID": "0000022222000",
#            "NET_STAMP": "4J5Y1OBYdPSx34567890",
#            "NET_MAC": "3F834F4367280B13C175C38A708A26AC",
#            "NET_RETURN": "http://quatloo.dev.scred.com:2345/payment/ping/samlink-query-response/%s/" % payment.get_value("code"),
#        }

        print "REQ:", urlencode(data)

        # FIXME: Hey, this is not using POST but rather GET! (Or what
        # the fsck am I talking about?)

        try:
            #con = urllib2.urlopen(self.QUERY_URL, urlencode(data))
            con = urllib2.urlopen(data["NET_RETURN"], urlencode(data))
            resp = con.read()
            print "RESP:", resp
        except urllib2.HTTPError:
            print "caught"
            return
            

        #respdata = cgi.parse_qs(resp)

        # No response MAC is sent.

        return

        if respdata["ReturnCode"] == "000":
            return (True, respdata)
        else:
            return (False, respdata)


PaymentProcessor.register_processor(SamlinkPaymentProcessor)
