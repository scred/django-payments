from processor import PaymentProcessor, MaksunapitPaymentProcessor

class NordeaPaymentProcessor(MaksunapitPaymentProcessor):

    """
    Payment processor for Nordea E-maksu.

    Features: authcap, query, refund

    Region(s): FI

    Specifications:
      http://bit.ly/2K2tIn (in Finnish, PDF)
    
    Merchant credentials for testing:
      merchant_key = "12345678"
      merchant_secret = "LEHTI"
      merchant_account = "29501800000014"

    Client credentials for testing:
      username = anything goes / automatically populated
      password = anything goes / automatically populated
    """

    METHOD = "nordea"

    URL = "https://solo3.nordea.fi/cgi-bin/SOLOPM01"
    QUERY_URL = "https://solo3.nordea.fi/cgi-bin/SOLOPM10"
    BUTTON_URL = "FIXME"

    PARAMETERS = {}

    DATA_FIXED = {
        "SOLOPMT_VERSION": "0003",
        "SOLOPMT_CONFIRM": "YES",
        "SOLOPMT_DATE": "EXPRESS",
    }

    # FIXME: KEYVERS: needed or not

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

    # https://solo3.nordea.fi/cgi-bin/SOLOPM10
    #SOLOPMT_VERSION = "0001"
    #SOLOPMT_TIMESTMP = "VVVVKKPPHHMMSSnnnn"
    #SOLOPMT_RCV_ID
    #SOLOPMT_LANGUAGE
    #SOLOPMT_RESPTYPE = xml/html
    #SOLOPMT_RESPDATA
    #SOLOPMT_RESPDETL
    #SOLOPMT_STAMP
    #SOLOPMT_REF
    #SOLOPMT_AMOUNT
    #SOLOPMT_CUR
    #SOLOPMT_ALG "01"
    #SOLOPMT_MAC

    @classmethod
    def get_query_form(self, payment):

        """
        The Nordea payment query interface has two basic operations
        modes: one targeted at operator instigated queries and another
        for automated queries. The RESPTYPE variable determines the
        mode of operation.

        With RESPTYPE being 'html' the mode targeted at human
        operators is invoked. You post a form and it returns a HTML
        page with the payment details. If you've set the RESPDATA
        parameter, there is a form on the details page that will post
        the payment details to the specified URL.

        On the other hand if RESPTYPE is 'xml' the post to Nordea will
        return an XML document with the payment details that can then
        be processed in anyway that makes sense.

        Here only the automated query is implemented and is intended
        for background queries.
        """

        # FIXME: we need for parameters flexible forward and backwards
        # parameter marshalling methods

        import httplib
        from urlparse import urlparse

        data = {}

        data["SOLOPMT_VERSION"] = "0001"
        data["SOLOPMT_TIMESTMP"] = "199911161024590001" # FIXME
        data["SOLOPMT_RCV_ID"] = self.get_setting("merchant_key")
        #data["SOLOPMT_LANGUAGE"] = payment.get_value("language")
        data["SOLOPMT_LANGUAGE"] = "1" # FIXME
        data["SOLOPMT_RESPTYPE"] = "xml" # "html" or "xml"
        #data["SOLOPMT_RESPDATA"] = "http://158.233.9.9/hsmok.htm" # FIXME
        data["SOLOPMT_RESPDATA"] = "text/xml" # FIXME
        #data["SOLOPMT_RESPDETL"] = "Y"
#        data["SOLOPMT_STAMP"] = payment.get_value("code")
        data["SOLOPMT_REF"] = payment.get_value("fi_reference")
#        data["SOLOPMT_AMOUNT"] = payment.get_value("amount")
#        data["SOLOPMT_CUR"] = payment.get_value("currency")
        data["SOLOPMT_KEYVERS"] = "0001" # FIXME
        data["SOLOPMT_ALG"] = "01"        

        order = ("VERSION", "TIMESTMP", "RCV_ID", "LANGUAGE", "RESPTYPE",
                 "RESPDATA", "RESPDETL", "STAMP", "REF", "AMOUNT", "CUR",
                 "KEYVERS", "ALG", "secret")

#        order = ("VERSION", "TIMESTMP", "RCV_ID", "LANGUAGE", "RESPTYPE",
#                 "RESPDATA", "RESPDETL", "STAMP",
#                 #"REF", "AMOUNT", "CUR", 
#                 "KEYVERS", "ALG", "secret")

        s = ""
        for p in order:
            if p == "secret":
                s += self.get_setting("merchant_secret") + "&"
            else:
                key = "SOLOPMT_%s" % p
                if key in data:
                    s += data[key] + "&"

        #print "MAC:", s
        #print "WANT:", "0001&199911161024590001&12345678&1&html&http://158.233.9.9/hsmok.htm&Y&501&0001&01&LEHTI&"

        import md5
        m = md5.new(s)
        data["SOLOPMT_MAC"] = m.hexdigest().upper()

        #print "pp.get_query_form() called"

        print "MAC-0:", data["SOLOPMT_MAC"]

        import urllib2
        from urllib import urlencode
        
        con = urllib2.urlopen(self.QUERY_URL, urlencode(data))
        resp = con.read()
        #print resp

        # https:///cgi-bin/SOLOPM10
        #http = httplib.HTTPSConnection("solo3.nordea.fi", 443)
        #http.putrequest("POST", "/cgi-bin/SOLOPM10")

        from xml.etree.ElementTree import XML, SubElement

        QUERY_RESP_PARAMS = (
            "SOLOPMT_VERSION",
            "SOLOPMT_TIMESTMP",
            "SOLOPMT_RCV_ID",
            "SOLOPMT_RESPCODE",
            "SOLOPMT_STAMP",
            "SOLOPMT_RCV_ACCOUNT",
            "SOLOPMT_REF",
            "SOLOPMT_DATE",
            "SOLOPMT_AMOUNT",
            "SOLOPMT_CUR",
            "SOLOPMT_PAID",
            "SOLOPMT_STATUS",
            "SOLOPMT_KEYVERS",
            "SOLOPMT_ALG",
        )

        macs = ""
        respdata = {}
        respmac = ""
        xml = XML(resp)
        for e in xml.getiterator():
            if e.tag in QUERY_RESP_PARAMS:
                macs += e.text + "&"
                respdata[e.tag] = e.text
            if e.tag == "SOLOPMT_MAC":
                respmac = e.text
            print "%s = %s" % (e.tag, e.text)
        macs += self.get_setting("merchant_secret") + "&"

        import md5
        m = md5.new(macs)
        print "macs", macs
        print "MAC-A", m.hexdigest().upper()
        print "MAC-B", respmac

        # FIXME: check the mac!

        return respdata

PaymentProcessor.register_processor(NordeaPaymentProcessor)
