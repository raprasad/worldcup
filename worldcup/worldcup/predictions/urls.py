from django.conf.urls.defaults import *

urlpatterns = patterns(
    'worldcup.predictions.views_predictions'

    # view predictions for a specific user
     , url(r'user-predictions/(?P<user_id>(\d){1,5})/$', 'view_user_predictions', name='view_user_predictions')

 
    , 
)


urlpatterns += patterns(
    'worldcup.predictions.views_knockout'
    # Make prediction
     , url(r'ko-fill-in/(?P<match_type_slug>(-|\w|_){1,50})/$', 'view_ko_prediction_form', name='view_ko_prediction_form')

     # Make prediction success
     , url(r'ko-fill-in-success/(?P<match_type_slug>(-|\w|_){1,50})/$', 'view_ko_prediction_saved_success', name='view_ko_prediction_saved_success')

)



urlpatterns += patterns(
    'worldcup.predictions.views'
    # Make prediction
     , url(r'fill-in/(?P<match_type_slug>(-|\w|_){1,50})/$', 'view_prediction_form2', name='view_prediction_form')

     # Make prediction success
     , url(r'fill-in-success/(?P<match_type_slug>(-|\w|_){1,50})/$', 'view_prediction_saved_success', name='view_prediction_saved_success')

    # List Match Types
     , url(r'$', 'view_prediction_list', name='view_prediction_list')

     # home page
     , url(r'$', 'view_prediction_list', name='home_url')
    , 
)


