from django.contrib import admin
from worldcup.predictions.models import Prediction, PredictionStage2



class PredictionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['user', 'match', 'team1_wins', 'team2_wins', 'is_draw', 'team1_score', 'team2_score']
    list_filter = [ 'user', 'match',]
admin.site.register(Prediction, PredictionAdmin)


class PredictionStage2Admin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['user', 'match', 'team1', 'team2', 'team1_wins', 'team2_wins', 'is_draw', 'team1_score', 'team2_score']
    list_filter = [ 'user', 'match',]
admin.site.register(PredictionStage2, PredictionStage2Admin)


