from django.conf.urls.defaults import *

urlpatterns = patterns('example.views',
    (r'^hello/$', 'hello'),
    (r'^checkout/$', 'checkout'),
    (r'^query/$', 'query'),
)

urlpatterns += patterns('processor.PaymentProcessor',
    (r'^payment/success/(.+?)/(.+?)/$', 'success_view'),
)
