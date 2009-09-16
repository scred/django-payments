from django.shortcuts import render_to_response

def hello(request):
    
    return render_to_response('hello.html',
                              {})

def checkout(request):
    """
    Create a payment and show a checkout page.
    """

    # FIXME: hax hax hax

    import datetime
    from SP import Payment, PickledStorage
    from processor import PaymentProcessor

    Payment.set_storage(PickledStorage)

    methods = (
        ("nordea", True),
        ("tapiola", True),
        ("sampo", False),
        ("op", True),
        ("samlink", True),
        ("luottokunta", False),
        ("spankki", False),
    )

    code = datetime.datetime.now().strftime("%H%M%S")
    code = "1234567890"
    payment = Payment(code=code)
    payment.set_payment_methods([m[0] for m in methods])
    payment.set_value("currency", "EUR")
    payment.set_value("language", "fi")
    payment.set_value("message", "Payment test!")
    payment.set_value("amount", "456.23")
    payment.set_value("fi_reference", "55")
    payment.save()

    forms = {}
    for method, tested in methods:
        pp = PaymentProcessor.get_processor(method)
        forms[method] = {"url": pp.URL,
                         "form": payment.get_checkout_form(method),
                         "tested": tested}

    context = {
        "forms": forms,
    }

    return render_to_response('checkout.html',
                              context)
