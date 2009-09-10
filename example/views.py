from django.shortcuts import render_to_response

def hello(request):
    
    return render_to_response('hello.html',
                              {})

def checkout(request):
    """
    Create a payment and show a checkout page.
    """

    import datetime
    from SP import Payment, PickledStorage

    Payment.set_storage(PickledStorage)

    code = datetime.datetime.now().strftime("%H%M%S")
    payment = Payment(code=code)
    payment.set_payment_methods(["nordea", "tapiola"])
    payment.set_value("currency", "EUR")
    payment.set_value("language", "fi")
    payment.set_value("message", "Payment test!")
    payment.set_value("amount", "42,00")
    payment.set_value("fi_reference", "1070")
    payment.save()

    context = {
        "forms": payment.get_checkout_forms()
    }

    return render_to_response('checkout.html',
                              context)
