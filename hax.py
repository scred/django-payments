#!/usr/bin/python

"""
A hacky testing script.
"""

from processor import PaymentProcessor
from SP import PickledPayment

PaymentProcessor.set_parameters("nordea", {
    "merchant_key": "12345678",
    "merchant_secret": "LEHTI",
    "merchant_name": "Company Ltd",
    "merchant_account": "29501800000014"
})

PaymentProcessor.set_parameters("sampo", {
    "merchant_key": "000000000000",
    "merchant_secret":
    "jumCLB4T2ceZWGJ9ztjuhn5FaeZnTm5H" +
    "pfDXWU2APRqfDcsrBs8mqkFARzm7uXKd"
})

# PaymentProcessors.enable("nordea")

payment = PickledPayment()

nordea = PaymentProcessor.get_processor("nordea")
sampo = PaymentProcessor.get_processor("sampo")

print nordea.get_checkout_form(payment)
