"""
Hack to implement a base class for all Finnish online debit payments
(= maksunapit / payment buttons).
"""

import md5 # FIXME: use hashlib instead

from PaymentProcessor import PaymentProcessor

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

        # use hashlib instead of md5

        # the check with all maksunapit is the same, we could somehow
        # abstract this

        # FIXME: store an audit event here

        payment = None # FIXME

        MAC = "SOLOPMT_RETURN_MAC"
        MACP = (
            ("SOLOPMT_RETURN_VERSION", 'GET',),
            ("SOLOPMT_RETURN_STAMP",'GET',),
            ("SOLOPMT_RETURN_REF",'GET',),
            ("SOLOPMT_RETURN_PAID", 'GET',),
            ("merchant_secret", "processor",),
        )
        MAC_SEPARATOR = "&"

        m = md5.new()
        for (var, source) in MACP:
            if source == 'GET':
                m.update(request.GET.get(var, ''))
            elif source == 'POST':
                m.update(request.POST.get(var, ''))
            elif source == 'processor':
                m.update(payment.get_value(var))
            else:
                pass
            m.update("&")

        return_mac = request.GET.get("SOLOPMT_RETURN_MAC", "")
        if m.hexdigest().upper() != return_mac.upper():
            raise PaymentProcessingError("Return MAC doesn't match!")

        # checked validity of the return

        # then use super to send the signal? (but paypal doesn't work
        # that way)

        # should we check the payment value and stuff like that?

        # who makes the call for audit?

        # 1. lookup payment
        # 2. call the success() of the payment (with method) ?
        # 3. return redirect to the payment's ok url
