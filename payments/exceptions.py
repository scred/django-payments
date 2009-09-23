class PaymentProcessingError(Exception):
    pass

class PaymentInvalidMacError(PaymentProcessingError):
    pass
