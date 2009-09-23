from django.http import HttpResponseRedirect
from payments.processor import PaymentProcessor
from payments.exceptions import PaymentProcessingError

def success(request, payment_method, payment_code):

    # FIXME: should probably do something different on error

    from payments.connector import PaymentConnector
    from example.utils import PickledPaymentConnector

    # FIXME: Setting the connector class here is way problematic.
    PaymentConnector.set_connector(PickledPaymentConnector)

    pp = PaymentProcessor.get_processor(payment_method)
    payment = PaymentConnector.get_connector().lookup(payment_code)

    print "payment:", payment

    try:
        pp.success(request, payment)
        return HttpResponseRedirect(pp.get_setting("return_url") %
                                    payment_code)
    except PaymentProcessingError:
        return HttpResponseRedirect(pp.get_setting("return_url") %
                                    payment_code)

    # FIXME: what about the refund hooks?

    # FIXME: what about the payment check hooks?
