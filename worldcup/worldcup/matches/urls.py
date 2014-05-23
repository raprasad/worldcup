from django.conf.urls.defaults import *

urlpatterns = patterns('worldcup.matches.views',
    # Example:
    # (r'^meditlog/', include('meditlog.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     #url(r'^view/(?P<portfolio_slug>\w([\w|\.\-])*)/$', 'view_single_project', name='view_single_project'),

     #url(r'^view/(?P<portfolio_slug>\w([\w|\.\-])*)/(?P<image_number>\d{1,3})/$', 'view_single_project', name='view_single_project_with_image_num'),
  
)
