from worldcup.common.msg_util import *
from worldcup.predictions.models import Prediction, PredictionStage2
from worldcup.matches.models import MATCH_TYPE_GROUP_STAGE, MATCH_TYPE_KNOCKOUT_STAGE

def score_group_predictions(sender, **kwargs):
    """
    (Sender is a Match object)
    
        (1) Match is saved with "score_recorded" = True
            (1a) post_save signal sent
        (2) Retrieve Predictions for Match
        (3) Score each Prediction and save it
    """
    #msg(sender)
    #msg(kwargs)
    saved_match = kwargs.get('instance', None)
    #msgt('signal sent for %s' % saved_match)
    if saved_match is None:
        return
        
    # Is this a group stage match?
    if saved_match.match_type.name==MATCH_TYPE_GROUP_STAGE:
       # is the score recorded?
       if saved_match.score_recorded:
           # retrieve all predictions
           for p in Prediction.objects.filter(match=saved_match):
               score_team_win_loss(prediction=p, match=saved_match)
               score_group_goals(prediction=p, match=saved_match)
    elif saved_match.match_type.name == MATCH_TYPE_KNOCKOUT_STAGE:
        if saved_match.score_recorded:
            # retrieve all predictions
            for pk in PredictionStage2.objects.filter(match=saved_match):
                # Only score the goals if the teams are picked correctly
                                
               score_ko_group_goals(prediction=pk
                                    , match=saved_match
                                    , potential_points=get_potential_points(saved_match))
               score_ko_team_win_loss(prediction=pk
                                    , match=saved_match
                                    , potential_points=get_potential_points(saved_match))
                
            
def score_group_goals(prediction=None, match=None, potential_points=1):
    """
    Score a user's goals scored prediction
    """
    #msgt('score_group_goals')
    if prediction is None or match is None:
        #msg('none')
        return
    
    prediction.points_scoring = 0

    if match.team1_final_score == prediction.team1_score:
        if match.team2_final_score == prediction.team2_score:
            prediction.points_scoring = potential_points
    prediction.save()
        

def score_ko_group_goals(prediction=None, match=None, potential_points=1):
    """
    Score a user's goals scored prediction - do not count shoot-outs
    """
    #msgt('score_group_goals')
    if prediction is None or match is None:
        #msg('none')
        return

    prediction.points_scoring = 0

    if prediction.team1==match.team1 and prediction.team2==match.team2:
        if match.team1_regular_time_score == prediction.team1_score:
            if match.team2_regular_time_score == prediction.team2_score:
                prediction.points_scoring = potential_points
    prediction.save()


def score_team_win_loss(prediction=None, match=None, potential_points=1):
    """
    Score a user's win/loss/tie prediction
    """
    #msgt('score_team_win_loss')
    
    if prediction is None or match is None:
        #msg('none')
        return
    
    if match.is_draw and prediction.is_draw:
        # draw
        prediction.points_win_loss_draw = potential_points
    elif match.did_team1_win() and prediction.team1_wins:
        # team 1 wins
        prediction.points_win_loss_draw = potential_points
    elif match.did_team2_win() and prediction.team2_wins:
        # team 2 wins
        prediction.points_win_loss_draw = potential_points
    else:
        # bad prediction
        prediction.points_win_loss_draw = 0
    #msgt('points: %s' % prediction.points_win_loss_draw)    
    prediction.save()
 
def get_potential_points(match): 
    if match.name.find('Round of 16') > -1:
        potential_points = 2
    elif match.name.find('Quarter Finals') > -1:
        potential_points = 4
    elif match.name.find('Semi Final') > -1:
        potential_points = 8
    elif match.name.find('3rd/4th Place') > -1:
        potential_points = 8
    elif match.name.find('Final') > -1:
        potential_points = 16
    else:
         potential_points = 1
    
    return potential_points
        
def score_ko_team_win_loss(prediction=None, match=None, potential_points=2):
    """
    Knockout round scoring
    Score a user's win/loss/tie prediction
    """
    
    # start with zero score
    prediction.points_win_loss_draw = 0
    

    if match.did_team1_win() and prediction.team1_wins :
        # team 1 wins and correct team chosen
        if prediction.team1==match.team1: 
            prediction.points_win_loss_draw = potential_points

    elif match.did_team2_win() and prediction.team2_wins:
        # team 2 wins and correct team chosen
        if prediction.team2==match.team2: 
            prediction.points_win_loss_draw = potential_points
      
    prediction.save()


            