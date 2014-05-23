from django.contrib import admin
from worldcup.matches.models import Venue, Match, MatchType


class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'slug']
admin.site.register(Venue, VenueAdmin)


class MatchTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'slug']#, 'end_date']
admin.site.register(MatchType, MatchTypeAdmin)


class MatchAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['id','name', 'team1', 'team2', 'match_time', 'match_type','score_recorded', 'team1_final_score', 'team2_final_score', 'is_draw']
    list_filter = [ 'score_recorded', 'is_draw', 'match_type']
admin.site.register(Match, MatchAdmin)

