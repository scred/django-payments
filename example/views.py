from django.shortcuts import render_to_response

def hello(request):
    
    return render_to_response('hello.html',
                              {})

def checkout(request):
    """
    Create a payment and show a checkout page.
    """

    import datetime
    from payments import PaymentStorage, PickledStorage
    from payments import PaymentProcessor

    Payment.set_storage(PickledStorage)

    methods = (
        ("nordea", True),
        ("tapiola", True),
        ("sampo", False),
        ("op", True),
        ("samlink", True),
        ("luottokunta", True),
        ("spankki", True),
        ("paypal", False),        
    )

    code = datetime.datetime.now().strftime("%H%M%S")
    payment = Payment(code=code)
    payment.set_payment_methods([m[0] for m in methods])
    payment.set_value("currency", "EUR")
    payment.set_value("language", "fi")
    payment.set_value("message", "Payment test!")
    payment.set_value("amount", "1.00")
    payment.set_value("fi_reference", "55")
    payment.add_item(price="42.00", qty="4", tax="0", description="widget")
    payment.add_item(price="12.00", qty="2", tax="0", description="choco")
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

def query(request):
    """
    Create a payment and show a payment query page.
    """

    import datetime
    from SP import Payment, PickledStorage
    from processor import PaymentProcessor

    Payment.set_storage(PickledStorage)

    methods = (
        ("nordea", False),
    )

    code = datetime.datetime.now().strftime("%H%M%S")
    code = "e246df44a03058cb69b2aee147310cd0"
    payment = Payment(code=code)
    payment.set_payment_methods([m[0] for m in methods])
    payment.set_value("currency", "EUR")
    payment.set_value("language", "1")
    payment.set_value("message", "Payment test!")
    payment.set_value("amount", "1,00")
    payment.set_value("fi_reference", "3748")
    payment.save()

    forms = {}
    for method, tested in methods:
        pp = PaymentProcessor.get_processor(method)
        url = pp.URL
        url = "https://solo3.nordea.fi/cgi-bin/SOLOPM10"
        forms[method] = {"url": url,
                         "form": payment.get_query_form(method),
                         "tested": tested}

    context = {
        "forms": forms,
    }

    return render_to_response('query.html',
                              context)
