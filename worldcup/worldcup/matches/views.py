from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from worldcup.matches.models import *

"""
matches = '''1	Fri	Jun 11, 2010	16:00	South Africa			Mexico	Johannesburg - JSC		
2	Fri	Jun 11, 2010	20:30	Uruguay			France	Cape Town		
3	Sat	Jun 12, 2010	16:00	Argentina			Nigeria	Johannesburg - JEP		
4	Sat	Jun 12, 2010	13:30	Korea Republic			Greece	Nelson Mandela Bay		
5	Sat	Jun 12, 2010	20:30	England			USA	Rustenburg		
6	Sun	Jun 13, 2010	13:30	Algeria			Slovenia	Polokwane		
7	Sun	Jun 13, 2010	20:30	Germany			Australia	Durban		
8	Sun	Jun 13, 2010	16:00	Serbia			Ghana	Tshwane/Pretoria		
9	Mon	Jun 14, 2010	13:30	Netherlands			Denmark	Johannesburg - JSC		
10	Mon	Jun 14, 2010	16:00	Japan			Cameroon	Mangaung / Bloemfontein		
11	Mon	Jun 14, 2010	20:30	Italy			Paraguay	Cape Town		
12	Tue	Jun 15, 2010	13:30	New Zealand			Slovakia	Rustenburg		
13	Tue	Jun 15, 2010	16:00	Cote d'Ivoire			Portugal	Nelson Mandela Bay		
14	Tue	Jun 15, 2010	20:30	Brazil			Korea DPR	Johannesburg - JEP		
15	Wed	Jun 16, 2010	13:30	Honduras			Chile	Nelspruit		
16	Wed	Jun 16, 2010	16:00	Spain			Switzerland	Durban		
17	Wed	Jun 16, 2010	20:30	South Africa			Uruguay	Tshwane/Pretoria		
18	Thu	Jun 17, 2010	20:30	France			Mexico	Polokwane		
19	Thu	Jun 17, 2010	16:00	Greece			Nigeria	Mangaung / Bloemfontein		
20	Thu	Jun 17, 2010	13:30	Argentina			Korea Republic	Johannesburg - JSC		
21	Fri	Jun 18, 2010	13:30	Germany			Serbia	Nelson Mandela Bay		
22	Fri	Jun 18, 2010	16:00	Slovenia			USA	Johannesburg - JEP		
23	Fri	Jun 18, 2010	20:30	England			Algeria	Cape Town		
24	Sat	Jun 19, 2010	16:00	Ghana			Australia	Rustenburg		
25	Sat	Jun 19, 2010	13:30	Netherlands			Japan	Durban		
26	Sat	Jun 19, 2010	20:30	Cameroon			Denmark	Tshwane/Pretoria		
27	Sun	Jun 20, 2010	13:30	Slovakia			Paraguay	Mangaung / Bloemfontein		
28	Sun	Jun 20, 2010	16:00	Italy			New Zealand	Nelspruit		
29	Sun	Jun 20, 2010	20:30	Brazil			Cote d'Ivoire	Johannesburg - JSC		
30	Mon	Jun 21, 2010	13:30	Portugal			Korea DPR	Cape Town		
31	Mon	Jun 21, 2010	16:00	Chile			Switzerland	Nelson Mandela Bay		
32	Mon	Jun 21, 2010	20:30	Spain			Honduras	Johannesburg - JEP		
33	Tue	Jun 22, 2010	16:00	Mexico			Uruguay	Rustenburg		
34	Tue	Jun 22, 2010	16:00	France			South Africa	Mangaung / Bloemfontein		
35	Tue	Jun 22, 2010	20:30	Nigeria			Korea Republic	Durban		
36	Tue	Jun 22, 2010	20:30	Greece			Argentina	Polokwane		
37	Wed	Jun 23, 2010	16:00	Slovenia			England	Nelson Mandela Bay		
38	Wed	Jun 23, 2010	16:00	USA			Algeria	Tshwane/Pretoria		
39	Wed	Jun 23, 2010	20:30	Ghana			Germany	Johannesburg - JSC		
40	Wed	Jun 23, 2010	20:30	Australia			Serbia	Nelspruit		
41	Thu	Jun 24, 2010	16:00	Slovakia			Italy	Johannesburg - JEP		
42	Thu	Jun 24, 2010	16:00	Paraguay			New Zealand	Polokwane		
43	Thu	Jun 24, 2010	20:30	Denmark			Japan	Rustenburg		
44	Thu	Jun 24, 2010	20:30	Cameroon			Netherlands	Cape Town		
45	Fri	Jun 25, 2010	16:00	Portugal			Brazil	Durban		
46	Fri	Jun 25, 2010	16:00	Korea DPR			Cote d'Ivoire	Nelspruit		
47	Fri	Jun 25, 2010	20:30	Chile			Spain	Tshwane/Pretoria		
48	Fri	Jun 25, 2010	20:30	Switzerland			Honduras	Mangaung / Bloemfontein		'''.split('\n')

from datetime import datetime
from worldcup.matches.models import *

match_type =MatchType(name="Group Stage")
match_type.save()

for line in matches: 
    items = line.split('\t')
    print items
    match_num, day_of_week, dt, time, team1, logo1, logo2, team2, venue_str, ignore1, ignore2 = items
    print dt[4:6]
    dt_obj = datetime(year=2010, month=6, day=int(dt[4:6]), hour=int(time[0:2]), minute=int(time[3:5]))
    
    team1 = Team.objects.get(name=team1)
    team2 = Team.objects.get(name=team2)
    try:
        venue = Venue.objects.get(name=venue_str)
    except Venue.DoesNotExist:
        print 'venue not found: %s' % venue_str
    new_match = Match(team1=team1, team2=team2, match_type=match_type, match_time=dt_obj)
    new_match.venue = venue
    new_match.save()
    
"""
