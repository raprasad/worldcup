from django.contrib.auth.models import User
from worldcup.predictions.models import Prediction
from worldcup.matches.models import Match, MATCH_TYPE_GROUP_STAGE
from django.db.models import Avg, Max, Min, Count, Sum
from worldcup.common.msg_util import *


class Standing:
    def __init__(self, user):
        self.user = user
        self.total_points = 0
        self.set_points()
        
    def set_points(self):
        
        point_result = Prediction.objects.filter(user=self.user, match__score_recorded=True).aggregate(points_so_far=Sum('points_final'))
        #msg(point_result)
        self.total_points = point_result.get('points_so_far', 0)
        #msg(self.total_points)
        
'''
from worldcup.predictions.models import Prediction
from worldcup.matches.models import Match, MATCH_TYPE_GROUP_STAGE
from django.db.models import Avg, Max, Min, Count, Sum

matches = Match.objects.filter(score_recorded=True)
print matches
lst = Prediction.objects.filter(match__in=matches) #.extra(select={'month': "LEFT(start_time,7)", 'month_fmt' : 
print lst
lst2 = Prediction.objects.filter(match__in=matches).values('user__first_name', 'user__last_name', 'user__username').annotate(points_so_far=Sum('points_final')).order_by('-points_final') 
Prediction.objects.filter(match__in=matches).annotate(points_so_far=Sum('points_final')).order_by('-points_final') 

print lst2
#.extra(select={'month': "LEFT(start_time,7)", 'month_fmt' : 
#AddRemoveLogItem.objects.annotate(num_actions=Count('cn_slug')).order_by('cn_slug')
#lst = Prediction.objects.filter(match__in=matches).extra(select={'month': "LEFT(start_time,7)", 'month_fmt' : "DATE_FORMAT(start_time, '%%b %%Y')" }).values('month', 'month_fmt').annotate(Sum('total_minutes')).order_by('month')#[:5]
'''
        
        
def get_current_standings():
    
    standings = map(lambda x: Standing(x), User.objects.all().order_by('last_name', 'first_name', 'username'))
    
    standings.sort(key=lambda obj: (obj.user.last_name, obj.user.first_name, obj.user.username), reverse=False)
    standings.sort(key=lambda obj: (obj.total_points), reverse=True)
    
    #standings.sort(key=lambda obj: ( obj.user.last_name,), reverse=True)
    
    return standings
    
    
    
