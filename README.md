django-payments
===============

A generic payments module for bilateral (ie, customer to merchant)
online payments as a pluggable Django application.

Status: Early stages of development with many Finnish payment systems
implemented and working. Internal and external API are liable to
change. Use with caution.

Goals and design parameters
---------------------------
 
Assumptions:

  - Merchant is not PCI compliant and does not need to become PCI
    compliant.

  - Customer credentials (credit card number, username or password)
    are taken at the payment processors site.

Not to be supported:

  - Support for credit card billing where credit card is taken on the
    merchant's site.

  - Subscription payments and other forms of recurring payments.

Supported payment systems
-------------------------

  - Finland, online debit payments via banks:

    - Nordea         ("nordea")
    - Tapiola        ("tapiola")
    - Sampo          ("sampo")
    - Osuuspankki    ("op")
    - Aktia/POP/SP   ("samlink")
    - S-Pankki       ("spankki")
    - Ålandsbanken   [under construction]
    - Handelsbanken  [under construction]

  - Finland (and Scandinavia), credit card processors:

    - Luottokunta    ("luottokunta")
    - DIBS           [planned]

  - Finland, payment aggregators:

    - Suomen Verkkomaksut  [planned]
    - checkout.fi  [planned]
    - Maksuturva  [planned]

  - Global:

    - PayPal Website Payments Standard  [planned]

Contributors
------------

  - ??
  - ??
