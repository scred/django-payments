#!/usr/bin/python

from PaymentProcessor import PaymentProcessor
from SP import PickledPayment

PaymentProcessor.set_parameters("nordea",
                                {"merchant_key": "12345678",
                                 "merchant_secret": "LEHTI",
                                 "merchant_name": "Company Ltd",
                                 "merchant_account": "29501800000014"})
# PaymentProcessors.enable("nordea")

payment = PickledPayment()

pp = PaymentProcessor.get_processor("nordea")

form = pp.get_checkout_form(payment)

print form
