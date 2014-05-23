from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.models import modelformset_factory
from worldcup.common.msg_util import *
from worldcup.common.user_util import *
from worldcup.matches.models import *
from worldcup.predictions.models import *
from worldcup.predictions.views import get_users_predictions
from worldcup.predictions.forms2 import KnockoutPredictionForm
from datetime import datetime


def view_ko_prediction_saved_success(request, match_type_slug):
    if not request.user.is_authenticated():
        return view_auth_page(request)

    lu = get_username(request)
        
    try:
        match_type = MatchType.objects.get(slug=match_type_slug)
        lu.update({ 'match_type' : match_type })
    except MatchType.DoesNotExist:
        lu.update({ 'Err_found':True
                    , 'MatchType_not_Found': True})
        return render_to_response('predictions/ko_round/add_ko_prediction_success.html', lu, context_instance=RequestContext(request))
              
    qset = get_users_predictions(request, request.user,  match_type)
        
      
    lu.update({ 'predictions':qset })
    return render_to_response('predictions/ko_round/add_ko_prediction_success.html', lu, context_instance=RequestContext(request) )


def view_ko_prediction_form(request, match_type_slug):
    """
    Prediction form for the group stage
    """
    if not request.user.is_authenticated():
        return view_auth_page(request)

    lu = get_username(request)
        
    try:
        match_type = MatchType.objects.get(slug=match_type_slug)
        lu.update({ 'match_type' : match_type })
    except MatchType.DoesNotExist:
        lu.update({ 'Err_found':True
                    , 'MatchType_not_Found': True})
        return render_to_response('predictions/ko_round/add_ko_prediction.html', lu, context_instance=RequestContext(request) )

    #   Is it too late to make a  prediction?
    #
    if datetime.now() > match_type.last_day_to_predict:
        lu.update({ 'Err_found':True
                    , 'Too_late_to_predict': True})
        return render_to_response('predictions/ko_round/add_ko_prediction.html', lu, context_instance=RequestContext(request) )
        

    lu.update({ 'user' : request.user })

    PredictionFormSet = modelformset_factory(PredictionStage2, form=KnockoutPredictionForm, extra=0)
    qset = get_users_predictions(request, request.user,  match_type)
    
    
    if request.method == 'POST':
        #deal with posting the data
        formset = PredictionFormSet(request.POST, queryset=qset)
        if formset.is_valid():
            formset.save()
            redirect_url = reverse('view_ko_prediction_saved_success'
                                 , kwargs={ 'match_type_slug':match_type.slug })
                   
            return HttpResponseRedirect(redirect_url)
             
        #else:
        #    msg(formset.errors)
    else:
        formset = PredictionFormSet(queryset=qset)
        
    lu.update({ 'formset':formset })
    return render_to_response('predictions/ko_round/add_ko_prediction.html', lu, context_instance=RequestContext(request) )

    
