from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.models import modelformset_factory
from worldcup.common.msg_util import *
from worldcup.common.user_util import *
from worldcup.matches.models import *
from worldcup.predictions.models import *
from worldcup.predictions.forms import *
from worldcup.teams.models import get_team_not_determined
from worldcup.predictions.standings import get_current_standings
from datetime import datetime

def view_prediction_list(request):
    """
    "Landing Page" with links to forms and some stats
    """
    if not request.user.is_authenticated():
        return view_auth_page(request)

    lu = get_username(request)


    lu.update({'match_types' :MatchType.objects.all() 
                , 'number_predictions' : Prediction.objects.all().count() 
                , 'number_users' : Prediction.objects.values('user').distinct().count()
                , 'standings' : get_current_standings()
                , 'num_matches_played' : Match.objects.filter(score_recorded=True).count()
                })

    return render_to_response('predictions/prediction_home.html', lu, context_instance=RequestContext(request) )


def get_new_prediction(user, match_type, match):
    if user is None or match_type is None:
        return None

    if match_type.name == MATCH_TYPE_KNOCKOUT_STAGE:
        p = PredictionStage2(user=user
                            , match=match
                            , team1=get_team_not_determined()
                            , team2=get_team_not_determined()
                            )
    else:
        p = Prediction(user=user, match=m)

    p.save()
    return p

def get_users_predictions(request, user, match_type):
    """For a given user and match type, return Prediction objects.
    If they don't exist, create them."""
    if user is None or match_type is None:
        return None
            
    #msgt('get_users_predictions')
    #msg('match_type: [%s]' % match_type)
    # minimal check, either user has no predictions or all of them
    num_matches = Match.objects.filter(match_type=match_type).count()
    
    if match_type.name == MATCH_TYPE_KNOCKOUT_STAGE:
        PredictionObj = eval('PredictionStage2')
    else:
        PredictionObj = eval('Prediction')
            
    
    # get user's predictions for this match type
    qset = PredictionObj.objects.filter(user=user, match__match_type=match_type)
    #msg(qset)
    if qset.count() == 0:   
        #
        # need to create Predictions for this user        
        #msg('zero qset')
    
        for m in Match.objects.filter(match_type=match_type):
            get_new_prediction(user, match_type, m)
            #p = PredictionObj(user=user, match=m)
            #p.save()
        return PredictionObj.objects.filter(user=user, match__match_type=match_type)
        
    elif qset.count() == num_matches:   
        #
        # correct number of Predictions
        #msg('matched: %s' % num_matches)
        return qset
        
    else:   
        #
        # wrong number of predictions, create new ones
        #msg('wrong number of Predictions [%s]'% qset)
        for m in Match.objects.filter(match_type=match_type):
            #msg('match: %s' % m)
            if PredictionObj.objects.filter(user=user, match=m).count() > 0:
                pass
            else:
                get_new_prediction(user, match_type, m)
                
        return PredictionObj.objects.filter(user=request.user, match__match_type=match_type)
        #msg('wrong number of Predictions: %s' % qset.count())
        #assert(False, "wrong number of Predictions")
        #return None

def view_prediction_saved_success(request, match_type_slug):
    if not request.user.is_authenticated():
        return view_auth_page(request)

    lu = get_username(request)
        
    try:
        match_type = MatchType.objects.get(slug=match_type_slug)
        lu.update({ 'match_type' : match_type })
    except MatchType.DoesNotExist:
        lu.update({ 'Err_found':True
                    , 'MatchType_not_Found': True})
        return render_to_response('predictions/add_prediction_success.html', lu, context_instance=RequestContext(request))
              
    qset = get_users_predictions(request, request.user,  match_type)
        
      
    lu.update({ 'predictions':qset })
    return render_to_response('predictions/add_prediction_success.html', lu, context_instance=RequestContext(request) )


def view_prediction_form2(request, match_type_slug):
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
        return render_to_response('predictions/add_prediction.html', lu, context_instance=RequestContext(request) )

    #   Is it too late to make a  prediction?
    #
    if datetime.now() > match_type.last_day_to_predict:
        lu.update({ 'Err_found':True
                    , 'Too_late_to_predict': True})
        return render_to_response('predictions/add_prediction.html', lu, context_instance=RequestContext(request) )
        

    lu.update({ 'user' : request.user })

    PredictionFormSet = modelformset_factory(Prediction, form=PredictionForm, extra=0)
    qset = get_users_predictions(request, request.user,  match_type)
    
    
    if request.method == 'POST':
        #deal with posting the data
        formset = PredictionFormSet(request.POST, queryset=qset)
        if formset.is_valid():
            formset.save()
            redirect_url = reverse('view_prediction_saved_success'
                                 , kwargs={ 'match_type_slug':match_type.slug })
                   
            return HttpResponseRedirect(redirect_url)
             
        #else:
        #    msg(formset.errors)
    else:
        formset = PredictionFormSet(queryset=qset)
        
    lu.update({ 'formset':formset })
    return render_to_response('predictions/add_prediction.html', lu, context_instance=RequestContext(request) )

    
    