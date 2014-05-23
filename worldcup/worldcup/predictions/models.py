from django.db import models
import os
from worldcup.common.msg_util import *

from django.template.defaultfilters import slugify 
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from worldcup.teams.models import Team, get_team_not_determined
from worldcup.matches.models import Match


TEAM_1_WINS_VAL = 1
TEAM_2_WINS_VAL = 2
DRAW_VAL = 0
WIN_DRAW_CHOICES = ( (TEAM_1_WINS_VAL, 'Team 1 wins')
                    ,(DRAW_VAL, 'Draw')
                    ,(TEAM_2_WINS_VAL, 'Team 2 wins')                    
                    )

KO_WIN_DRAW_CHOICES = ( (TEAM_1_WINS_VAL, 'Team 1 Advances')
                        ,(TEAM_2_WINS_VAL, 'Team 2 Advances')                    
                    )

                    
class Prediction(models.Model):
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)

    win_draw_choices = models.IntegerField(default=-1, choices=WIN_DRAW_CHOICES)
    
    team1_wins = models.BooleanField(default=False, help_text='auto-filled on save')
    team2_wins = models.BooleanField(default=False, help_text='auto-filled on save')
    is_draw = models.BooleanField(default=False, help_text='auto-filled on save')
    
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    
    points_win_loss_draw = models.IntegerField(default=0)
    points_scoring = models.IntegerField(default=0)
    points_final = models.IntegerField(default=0, help_text='auto-calculated on save')
    
    def __unicode__(self):
        return '%s - %s' % (self.user, self.match)
    
    def save(self):
        #msg('saving: %s [%s]' % (self, self.win_draw_choices))
        
        #
        # set the boolean variables based on the 'win_draw_choices' value
        #
        self.team1_wins = False
        self.team2_wins = False
        self.is_draw = False
        if self.win_draw_choices == 1:
            self.team1_wins = True
        elif self.win_draw_choices == 2:
            self.team2_wins = True
        elif self.win_draw_choices == 0:
            self.is_draw = True
            
        #
        # set the final points based on the scoring and win/loss/draw predictions
        #
        self.points_final = self.points_scoring + self.points_win_loss_draw
            
        super(Prediction, self).save()
        
    
    class Meta:
        ordering = ['user', 'match',]
    
    def calculate_points(self):
        pass


class PredictionStage2(Prediction):
    team1 = models.ForeignKey(Team, related_name='team1_pick')#, default=get_team_not_determined())    
    team2 = models.ForeignKey(Team, related_name='team2_pick')#, default=get_team_not_determined())       
        
        

"""
Scoring Predictions
- after a Match is saved, we want to score the predictions
"""
from django.db.models.signals import post_save      # after a Match is saved, we want to know about it
from worldcup.predictions.scoring import score_group_predictions
post_save.connect(score_group_predictions, sender=Match)

        