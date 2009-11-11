from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('')

urlpatterns += patterns(
    '',
    (r'^payment/', include('payments.urls')))

if settings.DEBUG:
    urlpatterns += patterns(
        'example.views',
        (r'^hello/$', 'hello'),
        (r'^checkout/$', 'checkout'),
        (r'^query/$', 'query'),
    )
