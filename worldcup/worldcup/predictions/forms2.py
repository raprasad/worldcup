from django import forms 
from django.contrib.auth.models import User
from worldcup.predictions.models import PredictionStage2, KO_WIN_DRAW_CHOICES
from worldcup.matches.models import Match
from worldcup.common.msg_util import *
from worldcup.teams.models import Team
from worldcup.predictions.team_choice_chooser import MatchTeamDataManager

_matchTeamDataManager = None
def get_mtd_manager():
    global _matchTeamDataManager
    if _matchTeamDataManager is None:
        _matchTeamDataManager = MatchTeamDataManager()
    return _matchTeamDataManager

class KnockoutPredictionForm(forms.ModelForm):
    user = forms.IntegerField(widget=forms.HiddenInput())
    match = forms.IntegerField(widget=forms.HiddenInput())
    win_draw_choices = forms.IntegerField(widget=forms.RadioSelect(choices=KO_WIN_DRAW_CHOICES))
    team1 = forms.ChoiceField()
    team2 = forms.ChoiceField()
    #team1_score = forms.IntegerField(initial=0)#, widget=forms.TextInput(attrs={'class':'input_score_box'}))
    #team2_score = forms.IntegerField(initial=0)#, widget=forms.TextInput(attrs={'class':'input_score_box'}))

    def __init__(self, *args, **kwargs):
        super(KnockoutPredictionForm, self).__init__(*args, **kwargs)
        
        mtdm = get_mtd_manager()
        t1_choices = mtdm.get_ko_team1_choices(self.instance.match.id)
        if t1_choices is None or len(t1_choices)==0:
            t1_choices = Team.objects.all()
            
        t2_choices = mtdm.get_ko_team2_choices(self.instance.match.id)
        if t2_choices is None or len(t2_choices)==0:
            t2_choices = Team.objects.all()
        
        #msgt('match name: %s' % self.instance.match.name)
        
        if len(t1_choices) == 1:
            self.fields['team1'].choices = [(t.id, t.name) for t in t1_choices]
        else:
            self.fields['team1'].choices = [('', '----------')] + [(t.id, t.name) for t in t1_choices]
            if not self.instance.team1.id == 33:
                self.fields['team1'].initial = self.instance.team1.id

        if len(t2_choices) == 1:
            self.fields['team2'].choices = [(t.id, t.name) for t in t2_choices]
        else:
            self.fields['team2'].choices = [('', '----------')] + [(t.id, t.name) for t in t2_choices]
            if not self.instance.team2.id == 33:
                self.fields['team2'].initial = self.instance.team2.id

        ##Team.objects.filter(id__gt=4)
        self.fields.keyOrder = [
                    'user',
                    'match',
                    'team1',
                    'team2',
                    'win_draw_choices',
                    'team1_score',
                    'team2_score']


    class Meta:
        model = PredictionStage2
        exclude = ['team1_wins'
                    , 'team2_wins'
                    , 'is_draw'
                    , 'points_win_loss_draw'
                    , 'points_scoring'
                    , 'points_final']
                        
    def clean(self):
        return self.cleaned_data    

   
        
    def clean_user(self):
        user = self.cleaned_data.get('user')

        if not user:
           raise forms.ValidationError('User not found')

        try:
            user_obj = User.objects.get(pk=user)
        except User.DoesNotExist:
            raise forms.ValidationError('User not found in database')
        
        return user_obj

    def clean_team1(self):
        team_id = self.cleaned_data.get('team1')

        if not team_id:
           raise forms.ValidationError('Match not found')

        try:
            t = Team.objects.get(pk=team_id)
        except Match.DoesNotExist:
            raise forms.ValidationError('Team not found in database')

        return t


    def clean_team2(self):
        team_id = self.cleaned_data.get('team2')

        if not team_id:
           raise forms.ValidationError('Match not found')

        try:
            t = Team.objects.get(pk=team_id)
        except Match.DoesNotExist:
            raise forms.ValidationError('Team not found in database')

        return t

            
    def clean_match(self):
        match_id = self.cleaned_data.get('match')

        if not match_id:
           raise forms.ValidationError('Match not found')

        try:
            match_obj = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            raise forms.ValidationError('Match not found in database')

        return match_obj
