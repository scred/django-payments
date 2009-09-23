from django.http import HttpResponseRedirect

def success(request, payment_method, payment_code):

    # FIXME: lookup payment already here based on the code

    # FIXME: should probably do something different on error

    pp = PaymentProcessor.get_processor(payment_method)

    # FIXME: lookup the payment here

    from SP import Payment, PickledStorage
    Payment.set_storage(PickledStorage)

    payment = Payment.lookup(payment_code)

    try:
        
        pp.success(request, payment)
        return HttpResponseRedirect(pp.get_setting("return_url") %
                                    payment_code)
    except PaymentProcessingError:
        return HttpResponseRedirect(pp.get_setting("return_url") %
                                    payment_code)

    # what about the refund hooks?

    # what about the payment check hooks?
