from payments import PaymentProcessor, SamlinkPaymentProcessor

class AktiaPaymentProcessor(SamlinkPaymentProcessor):

    """
    Payment processor for Aktia/SP/POP-maksu. Extends the generic
    Samlink payment processor.

    Features: authcap, (query)

    Region(s): FI

    Specifications:
      ??
    
    Merchant credentials for testing:
      merchant_key = "0000000000"
      merchant_secret = "11111111111111111111"

    Client credentials for testing:
      username = "11111111"
      password = "123456"
    """

    METHOD = "aktia"

    URL = "https://verkkomaksu.inetpankki.samlink.fi/vm/login.html"
    QUERY_URL = "https://verkkomaksu.inetpankki.samlink.fi/vm/kysely.html"
    BUTTON_URL = "FIXME"

    COST_FIXED = "0.34"
    COST_PERCENTAGE = "0.00"
    
PaymentProcessor.register_processor(AktiaPaymentProcessor)
