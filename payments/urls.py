from django.conf.urls.defaults import patterns

urlpatterns = patterns('payments.views',
    (r'^success/(.+?)/(.+?)/$', 'success'),
)
