import md5
from payments import PaymentProcessor
from payments.exceptions import PaymentInvalidMacError

class PaypalPaymentProcessor(PaymentProcessor):

    """
    Payment processor for PayPal.

    Region(s): Global

    Specifications:
      ?? (in English, PDF)

    Required parameters:
      merchant_acount = email address of the payment receiver
    
    Merchant credentials for testing:
      Either use a regular Premium or Business account, or register
      for a sandbox account.
      
    Client credentials for testing:
      As with merchant credentials.
    """

    METHOD = "paypal"

    URL = "https://www.paypal.com/cgi-bin/webscr"
    BUTTON_URL = "FIXME"

    PARAMETERS = {}

    USE_CART = True

    DATA_CART = {
        "amount_%d": "price",
        "quantity_%d": "qty",
        "tax_%d": "tax",
        "item_name_%d": "description",
    }

    DATA_FIXED = {
        "cmd": "_cart",
        "upload": "1",
        "paymentaction": "sale",
        "charset": "utf-8",
        "no_shipping": "2",
        "no_note": "1",
        "rm": "2",
    }

    DATA_MERCHANT = {
        "business": "merchant_account",
    }

    CURRENCY = { # FIXME: Not all of the supported currencies are included.
        "EUR": "EUR",
        "USD": "USD",
    }
    CURRENCY_PARAM = "currency_code"
    CURRENCY_DEFAULT = "EUR"

    LANGUAGE = { # FIXME: probably buggy
        "en": "EN",
    }
    LANGUAGE_PARAM = "language"
    LANGUAGE_DEFAULT = "en"

    DATA_PAYMENT = {
        "invoice": "code",
    }

    DATA_URLS = {
        "return": "processing",
        "cancel_return": "cancel",
        "notify_url": "notify",
    }

    PAYMENT_REQ_MAC = ""
    PAYMENT_REQ_PARAMS = (
    )
    PAYMENT_REQ_SEPARATOR = ""

    PAYMENT_RESP_MAC = ""
    PAYMENT_RESP_PARAMS = (
    )
    PAYMENT_RESP_SEPARATOR = ""

    @classmethod
    def success_check_mac(self, request, payment):

        s = ""
        for (var, source) in self.PAYMENT_RESP_PARAMS:
            if source == 'GET':
                s += request.GET.get(var, '')
            elif source == 'POST':
                s += request.POST.get(var, '')
            elif source == 'processor':
                s += self.get_parameter(var)
            elif source == 'payment':
                value = payment.get_value(var)
                if var == 'amount':
                    value = self.massage_amount(value)
                s += value
                
            elif source == 'fixed':
                s += var
            else:
                pass
            s += self.PAYMENT_RESP_SEPARATOR

        m = md5.new(s)
        return_mac = request.GET.get(self.PAYMENT_RESP_MAC, '')

        if m.hexdigest().upper() != return_mac.upper():
            raise PaymentInvalidMacError("Return MAC doesn't match!")

    @classmethod
    def massage_amount(self, value):
        return value.replace(".", "")

PaymentProcessor.register_processor(PaypalPaymentProcessor)
