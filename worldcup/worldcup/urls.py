from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

MCB_WC_URL_PREFIX = 'mcb-wc/'

urlpatterns = patterns('',
    # Example:

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^portfolio/', include('nymdesign.portfolio.urls')),

    # login 
     (r'^' + MCB_WC_URL_PREFIX + 'l/', include('worldcup.auth_active_directory.urls')),

    # predictions
     (r'^' + MCB_WC_URL_PREFIX + 'predictions/', include('worldcup.predictions.urls')),

    # Uncomment the next line to enable the admin:
     (r'^' + MCB_WC_URL_PREFIX + 'worldcup-admin/(.*)', admin.site.root),

     # default
     (r'^' + MCB_WC_URL_PREFIX + '$', include('worldcup.predictions.urls')),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/ramanprasad/projects/worldcup/media'}),)
