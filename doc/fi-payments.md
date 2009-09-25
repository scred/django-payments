FINLAND: Bank Payment Buttons
=============================

Introduction
------------

Families
--------

  Independents:
  - Nordea
  - OP
  - Sampo
  
  Samlink:
  - SP/POP/Aktia
  - Handelsbanken

  Crosskey:
  - Ålandsbanken
  - Tapiola
  - S-Pankki


  authcap variants:
  (1) nordea, crosskey, samlink
  (2) op
  (3) sampo

  query variants:
  (1) Nordea, crosskey
  (2) op
  (3) sampo
  (4) samlink

  refund variants:
  (1) nordea

Authorize and capture
---------------------

Payment status queries
----------------------

Payment processing modules that implement payment status queries have
the capability "query".

Most of the banks support a query interface that can be used to check
the status of a specific payment. The primary use case for the query
interface is to verify payment completion if the customer did not
explicitly click the "return to merchant" link at the bank's site.

The query interfaces are a later addition to the payment button
system. As such each bank has distinct parameters and interaction
pattern.

Models:

 (1) sync: post formdata, return xml
 (2) async: post formdata, return html, click for postdata ping (get/post)
 (3) sync: post formdata, return formdata

 (4) hybrid: post formdata, return HTTP 302 that redirects to ping url
 with get parameters describing status

nordea: (1)+(2)
sampo: (3)
op: (2)
samlink: (4)
s-pankki: (1)+(2)
handelsbanken: (4)

Programmatic refunds
--------------------

??

References
----------

http://www.aivomatic.com/blogi/verkkomaksujen-hinnat/
