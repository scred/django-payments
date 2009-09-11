import md5
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

    URL = "https://dmp2.luottokunta.fi/dmp/html_payments"
    BUTTON_URL = "FIXME"

    PARAMETERS = {}

    DATA_FIXED = {
        "Card_Details_Transmit": "0",
        "Device_Category": "1",
        "Transaction_Type": "1",
    }

    DATA_MERCHANT = {
        "Merchant_Number": "merchant_key",
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
        "Order_ID": "code",
        "Customer_ID": "fi_reference", 
        "Order_Description": "message",
        "Amount": "amount",
    }

    DATA_URLS = {
        "Success_Url": "success",
        "Cancel_Url": "cancel",
        "Failure_Url": "error",
    }

    PAYMENT_REQ_MAC = "Authentication_Mac"
    PAYMENT_REQ_PARAMS = (
        ("Merchant_Number", "data"),
        ("Order_ID", "data"),
        ("Amount", "data"),
        ("Transaction_Type", "data"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_REQ_SEPARATOR = ""

    PAYMENT_RESP_MAC = "LKMAC"
    PAYMENT_RESP_PARAMS = (
        ("FIXME", "GET"),
        ("merchant_secret", "processor"),
    )
    PAYMENT_RESP_SEPARATOR = ""

    @classmethod
    def checkout_hash(self, data):

        s = ""
        for (var, source) in self.PAYMENT_REQ_PARAMS:
            if source == "data":
                s += data[var]
            elif source == 'processor':
                s += self.get_parameter(var)
            else:
                pass
            s += self.PAYMENT_REQ_SEPARATOR

        m = md5.new(s)

        print "MAC string:", s
        print "MAC digest:", m.hexdigest().upper()

        return {
            self.PAYMENT_REQ_MAC: m.hexdigest().upper(),
        }

    @classmethod
    def success_check_mac(self, request, payment):

        s = ""
        for (var, source) in self.PAYMENT_RESP_PARAMS:
            if source == 'GET':
                s += request.GET.get(var, '')
            elif source == 'POST':
                s += request.POST.get(var, '')
            elif source == 'processor':
                print "parameters:", self.get_parameter(var)
                s += self.get_parameter(var)
            else:
                pass
            s += self.PAYMENT_RESP_SEPARATOR

        m = md5.new(s)
        return_mac = request.GET.get(self.PAYMENT_RESP_MAC, '')

        print "MAC-A:", m.hexdigest().upper()
        print "MAC-B:", return_mac.upper()

        if m.hexdigest().upper() != return_mac.upper():
            raise PaymentInvalidMacError("Return MAC doesn't match!")

    @classmethod
    def massage_amount(self, value):
        return value.replace(".", "")


PaymentProcessor.register_processor(LuottokuntaPaymentProcessor)
