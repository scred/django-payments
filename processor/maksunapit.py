"""
Hack to implement a base class for all Finnish online debit payments
(= maksunapit / payment buttons).
"""

import md5 # FIXME: use hashlib instead

from PaymentProcessor import PaymentProcessor, PaymentProcessingError

class MaksunapitPaymentProcessor(PaymentProcessor):

    @classmethod
    def checkout_hash(self, data):

        m = md5.new()
        for (var, source) in self.PAYMENT_REQ_PARAMS:
            if source == "data":
                m.update(data[var] or '')
            elif source == 'processor':
                m.update(self.PARAMETERS[var])
            else:
                pass
            m.update(self.PAYMENT_REQ_SEPARATOR)

        return {
            self.PAYMENT_REQ_MAC: m.hexdigest(),
        }

    @classmethod
    def success(self, request, payment_method, payment_code):

        # the check with all maksunapit is the same, we could somehow
        # abstract this

        # FIXME: store an audit event here

        m = md5.new()
        for (var, source) in self.PAYMENT_RESP_PARAMS:
            if source == 'GET':
                m.update(request.GET.get(var, ''))
            elif source == 'POST':
                m.update(request.POST.get(var, ''))
            elif source == 'processor':
                m.update(self.PARAMETERS[var])
            else:
                pass
            m.update("&")

        return_mac = request.GET.get(self.PAYMENT_RESP_MAC, '')
        if m.hexdigest().upper() != return_mac.upper():
            # FIXME: Activate the raise here!
            # raise PaymentProcessingError("Return MAC doesn't match!")
            pass

        from SP import Payment

        payment = Payment.lookup(payment_code)
        payment.success(self.METHOD)
        
        print "payment:", payment
        #print "payment:", type(payment)

        # FIXME: all ok, now need to do a redirect

        # should we check the payment value and stuff like that?

        # who makes the call for audit?
