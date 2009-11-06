from django.http import HttpResponseRedirect
from payments.processor import PaymentProcessor
from payments.exceptions import PaymentProcessingError

def success(request, payment_method, payment_code):

    from payments.connector import PaymentConnector

    payment = PaymentConnector.get_connector().lookup(payment_code)
    pp = PaymentProcessor.get_processor(payment_method)

    try:
        return pp.success(request, payment)
    except PaymentProcessingError, e:
        # FIXME: redirect to error!
        print "exception: %s" % e
        
        return payment.exception() # FIXME: What bogus is this?

    # FIXME: what about the refund hooks?

    # FIXME: what about the payment check hooks?
