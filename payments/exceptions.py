class PaymentProcessingError(Exception):
    pass

class PaymentInvalidMacError(PaymentProcessingError):
    pass

class PaymentValidationError(PaymentProcessingError):
    pass
