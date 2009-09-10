#!/usr/bin/python

"""
An example and testing script. Creates a payment and retrieves a
payment form for each method set for the payment.
"""

from processor import PaymentProcessor, success_view
from SP import Payment, PickledStorage

# initialize payment processors with test credentials

PaymentProcessor.set_parameters("nordea", {
    "merchant_key": "12345678",
    "merchant_secret": "LEHTI",
    "merchant_name": "Company Ltd",
    "merchant_account": "29501800000014",
    "return_url": "/order/%s/",
})

PaymentProcessor.set_parameters("sampo", {
    "merchant_key": "000000000000",
    "merchant_secret":
    "jumCLB4T2ceZWGJ9ztjuhn5FaeZnTm5H" +
    "pfDXWU2APRqfDcsrBs8mqkFARzm7uXKd",
    "return_url": "/order/%s/",
})

Payment.set_storage(PickledStorage)

# create a payment instance

payment = Payment(code="1234")
payment.set_payment_methods(("nordea", "sampo"))
payment.set_value("currency", "EUR")
payment.set_value("language", "en")
payment.set_value("message", "Payment test!")
payment.set_value("amount", "42.00")
payment.set_value("fi_reference", "1070")
payment.save()

# print payment.get_checkout_forms()

# simulated return from the bank

from django.http import HttpRequest

request = HttpRequest()
request.GET = {}
request.POST = {}

print success_view(request, "nordea", payment.code)
