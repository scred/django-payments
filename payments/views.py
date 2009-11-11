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
        return pp.error(request, payment, e)

# FATAL: missing error() and cancel() views completely!
