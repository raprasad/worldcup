from datetime import datetime
from worldcup.matches.models import *

    
    
"""
# match num	team 1	team 2	grid group	date	time
matches = '''49	1a	2b	1	6/26	16:00	Nelson Mandela Bay
50	1c	2d	1	6/26	20:30	Rustenburg
51	1d	2c	2	6/27	16:00	Mangaung / Bloemfontein
52	1b	2a	2	6/27	20:30	Johannesburg
53	1e	2f	3	6/28	16:00	Durban
54	1g	2h	3	6/28	20:30	Johannesburg
55	1f	2e	4	6/29	16:00	Tshwane/Pretoria
56	1h	2g	4	6/29	20:30	Cape Town
57	53	54		7/2	16:00	Nelson Mandela Bay
58	49	50		7/2	20:30	Johannesburg
59	52	51		7/3	16:00	Cape Town
60	55	56		7/3	20:30	Johannesburg
61	1	3		7/6	20:30	Cape Town
62	2	4		7/7	20:30	Durban
63	1,3	2,4		7/11	20:30	Nelson Mandela Bay
64	1,3	2,4		7/12	20:30	Johannesburg'''.split('\n')

from worldcup.matches.models import *
from worldcup.teams.models import get_team_not_determined
from datetime import datetime

try:
    match_type = MatchType.objects.get(name="Knockout Stage")
except MatchType.DoesNotExist:
    match_type =MatchType(name="Knockout Stage", last_day_to_predict=datetime(year=2010,month=6,day=25))
    match_type.save()

for line in matches: 
    items = line.split('\t')
    print items
    match_num, team1_choices, team1_choices, grid_group, dt, time_str, venue_str = items
    mm, dd = dt.split('/')
    hh, min = time_str.split(':')
    dt_obj = datetime(year=2010, month=int(mm), day=int(dd), hour=int(hh), minute=int(min))
    team1 = get_team_not_determined()   #Team.objects.get(name=team1)
    team2 = get_team_not_determined()   #Team.objects.get(name=team2)
    venues = Venue.objects.filter(name__startswith=venue_str)
    if venues.count() == 0:
        print 'venue not found: %s' % venue_str
    else:
        venue=venues[0]  
    
    match_num = int(match_num)
    if match_num == 64:
        mname = 'Game %s: Final' % match_num
    elif match_num == 63:
        mname = 'Game %s: 3rd/4th Place' % match_num
    elif match_num in [61, 62]:
        mname = 'Game %s: Semi Finals' % match_num
    elif match_num in range(57,61):
        mname = 'Game %s: Quarter Finals' % match_num
    else:
        mname = 'Game %s: Round of 16' % match_num
    
    new_match = Match(name=mname, team1=team1, team2=team2, match_type=match_type, match_time=dt_obj)
    new_match.venue = venue
    new_match.save()
"""
