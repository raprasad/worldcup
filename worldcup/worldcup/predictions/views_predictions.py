from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.models import modelformset_factory
from worldcup.common.msg_util import *
from worldcup.common.user_util import *
from worldcup.matches.models import *
from worldcup.predictions.models import *
from worldcup.predictions.forms import *
from worldcup.predictions.standings import Standing
from datetime import datetime
from worldcup.matches.models import MATCH_TYPE_GROUP_STAGE, MATCH_TYPE_KNOCKOUT_STAGE


def view_user_predictions(request, user_id):
    """
    Current user's predictons
    """
    if not request.user.is_authenticated():
        return view_auth_page(request)

    lu = get_username(request)

    try:
        user_with_predictions = User.objects.get(pk=user_id)
        lu.update({ 'user_with_predictions' : user_with_predictions })
    except User.DoesNotExist:
        lu.update({ 'Err_found':True
                , 'User_with_predictions_not_found': True})
        return render_to_response('predictions/user_predictions.html', lu, context_instance=RequestContext(request))
            
    qset = Prediction.objects.filter(user=user_with_predictions, match__match_type__name=MATCH_TYPE_GROUP_STAGE)
    qset_ko = PredictionStage2.objects.filter(user=user_with_predictions)
    #msgt('user: %s' % user_with_predictions)
    #msg('ko: %s' % qset_ko)
    
    standing = Standing(user_with_predictions)
    
    lu.update({ 'predictions':qset 
                , 'ko_predictions' : qset_ko
                , 'points_for_user' : standing.total_points
                , 'num_matches_played' : Match.objects.filter(score_recorded=True).count()
                
    })
    return render_to_response('predictions/user_predictions.html', lu, context_instance=RequestContext(request) )
    
