from django.conf.urls.defaults import *

urlpatterns = patterns('example.views',
    (r'^hello/$', 'hello'),
    (r'^checkout/$', 'checkout'),
    (r'^query/$', 'query'),
)

urlpatterns += patterns('payments.views',
    url(r'^payment/success/(.+?)/(.+?)/$', 'success'),
)
