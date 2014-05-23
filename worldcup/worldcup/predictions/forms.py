from django import forms 
from django.contrib.auth.models import User
from worldcup.predictions.models import Prediction, WIN_DRAW_CHOICES, DRAW_VAL, TEAM_1_WINS_VAL, TEAM_2_WINS_VAL
from worldcup.matches.models import Match

class PredictionForm(forms.ModelForm):
    user = forms.IntegerField(widget=forms.HiddenInput())
    match = forms.IntegerField(widget=forms.HiddenInput())
    win_draw_choices = forms.IntegerField(widget=forms.RadioSelect(choices=WIN_DRAW_CHOICES))
    #team1_score = forms.IntegerField(initial=0)#, widget=forms.TextInput(attrs={'class':'input_score_box'}))
    #team2_score = forms.IntegerField(initial=0)#, widget=forms.TextInput(attrs={'class':'input_score_box'}))

    class Meta:
        model = Prediction
        exclude = ['team1_wins'
                    , 'team2_wins'
                    , 'is_draw'
                    , 'points_win_loss_draw'
                    , 'points_scoring'
                    , 'points_final']
                        
    def clean(self):
        return self.cleaned_data    

        '''
        team1_score = self.cleaned_data.get('team1_score')
        team2_score = self.cleaned_data.get('team2_score')
        win_draw_choices = self.cleaned_data.get('win_draw_choices')
        '''
        
        """
        if win_draw_choices==DRAW_VAL:
            if not team1_score == team2_score:
                raise forms.ValidationError('If you choose "Draw", the scores must be the same')
        elif win_draw_choices == TEAM_1_WINS_VAL:
            if not team1_score > team2_score:
                raise forms.ValidationError('If you choose "Team 1 Wins", the Team 1 score must be greater')
        elif win_draw_choices == TEAM_2_WINS_VAL:
            if not team2_score > team1_score:
                raise forms.ValidationError('If you choose "Team 2 Wins", the Team 2 score must be greater')
        """
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
            
    def clean_match(self):
        match_id = self.cleaned_data.get('match')

        if not match_id:
           raise forms.ValidationError('Match not found')

        try:
            match_obj = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            raise forms.ValidationError('Match not found in database')

        return match_obj
 