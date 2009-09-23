#!/usr/bin/python

"""
An example and testing script. Creates a payment and retrieves a
payment form for each method set for the payment.
"""

import sys
from payments import PaymentProcessor
from payments.connector import PaymentConnector, PickledStorage
from example.PickledPaymentConnector import PickledPaymentConnector

# initialize payment processors with test credentials

PaymentConnector.set_connector(PickledPaymentConnector)

# create a payment instance

payment = PaymentConnector(code="1997060417052135")
#payment = Payment(code="900")
#payment.set_payment_methods(["nordea", "sampo", "op", "samlink", "tapiola"])
payment.set_payment_methods(["nordea"])
payment.set_value("currency", "EUR")
payment.set_value("language", "en")
payment.set_value("message", "Payment test!")
payment.set_value("amount", "13,00")
payment.set_value("fi_reference", "13")
payment.add_item(price="42.00", qty="4", tax="0", description="widget")
payment.add_item(price="12.00", qty="2", tax="0", description="choco")
payment.save()

#print payment.get_items()

for key, value in payment.get_checkout_forms()["nordea"].items():
    print "%s = %s" % (key, value)

#print payment.query("samlink")
#print payment.refund("op")

# simulated return from the bank

from django.http import HttpRequest

request = HttpRequest()
request.GET = {}
request.POST = {}

#print success_view(request, "nordea", payment.code)
