from django.conf.urls.defaults import *

urlpatterns = patterns('example.views',
    (r'^hello/$', 'hello'),
    (r'^checkout/$', 'checkout'),
    (r'^query/$', 'query'),
)

urlpatterns += patterns('',
                        (r'^payment/', include('payments.urls')))
