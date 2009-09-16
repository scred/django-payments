#!/usr/bin/python

"""
An example and testing script. Creates a payment and retrieves a
payment form for each method set for the payment.
"""

import sys
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

PaymentProcessor.set_parameters("op", {
    "merchant_key": "Esittelymyyja",
    "merchant_secret": "Esittelykauppiaansalainentunnus",
    "return_url": "/order/%s/",
})

PaymentProcessor.set_parameters("samlink", {
    "merchant_key": "0000000000",
    "merchant_secret": "11111111111111111111",
    "merchant_account": "448710-126",
    "return_url": "/order/%s/",
})

PaymentProcessor.set_parameters("tapiola", {
    "merchant_key": "TAPESHOPID",
    "merchant_secret": "PAPUKAIJA",
    "merchant_account": "2019363630-01652643",
    "merchant_name": "Company Ltd",
    "return_url": "/order/%s/",
})

Payment.set_storage(PickledStorage)

p = Payment.lookup("1234567890")
print p.get_values()

sys.exit(0)

# create a payment instance

payment = Payment(code="1998052212254471")
#payment.set_payment_methods(["nordea", "sampo", "op", "samlink", "tapiola"])
payment.set_payment_methods(["nordea"])
payment.set_value("currency", "EUR")
payment.set_value("language", "en")
payment.set_value("message", "Payment test!")
payment.set_value("amount", "570,00")
payment.set_value("fi_reference", "55")
payment.save()

for key, value in payment.get_checkout_forms()["nordea"].items():
    print "%s = %s" % (key, value)

# simulated return from the bank

from django.http import HttpRequest

request = HttpRequest()
request.GET = {}
request.POST = {}

#print success_view(request, "nordea", payment.code)
