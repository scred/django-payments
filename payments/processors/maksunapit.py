"""
Hack to implement a base class for all Finnish online debit payments
(= maksunapit / payment buttons).
"""

import md5 # FIXME: use hashlib instead

from payments.processor import PaymentProcessor
from payments.exceptions import PaymentProcessingError, PaymentInvalidMacError

class MaksunapitPaymentProcessor(PaymentProcessor):

    @classmethod
    def checkout_hash(self, data):
        s = ""
        for (var, source) in self.PAYMENT_REQ_PARAMS:
            if source == "data":
                s += data[var]
            elif source == 'processor':
                s += self.get_setting(var)
            else:
                pass
            s += self.PAYMENT_REQ_SEPARATOR

        m = md5.new(s)

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
                s += self.get_setting(var)
            elif source == 'payment':
                s += payment.get_value(var)
            elif source == 'fixed':
                s += var
            else:
                raise PaymentProcessingError("unknown MAC source: %s" % source)
            s += self.PAYMENT_RESP_SEPARATOR

        digest = md5.md5(s).hexdigest()
        return_mac = request.GET.get(self.PAYMENT_RESP_MAC, '')

        if digest.upper() != return_mac.upper():
            raise PaymentInvalidMacError("Return MAC doesn't match!")

    @classmethod
    def success_check_params(self, request, payment):
        pass

    @classmethod
    def massage_amount(self, value):
        return value.replace(".", ",")

    @classmethod
    def get_processor_reference(self, request):
        if self.PAYMENT_RESP_PROCESSOR_REFERENCE:
            return request.GET.get(self.PAYMENT_RESP_PROCESSOR_REFERENCE, '')
        return '-'
