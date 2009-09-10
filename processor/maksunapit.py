"""
Hack to implement a base class for all Finnish online debit payments
(= maksunapit / payment buttons).
"""

import md5 # FIXME: use hashlib instead

from PaymentProcessor import PaymentProcessor, PaymentProcessingError

class MaksunapitPaymentProcessor(PaymentProcessor):

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
    def success(self, request, payment_method, payment_code):

        # the check with all maksunapit is the same, we could somehow
        # abstract this

        # FIXME: store an audit event here

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
            raise PaymentProcessingError("Return MAC doesn't match!")

        from SP import Payment

        # FIXME: activate these two lines
        # payment = Payment.lookup(payment_code)
        # payment.success(self.METHOD)
        
        # print "payment:", payment
        #print "payment:", type(payment)

        # FIXME: all ok, now need to do a redirect

        # should we check the payment value and stuff like that?

        # who makes the call for audit?
