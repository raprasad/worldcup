from worldcup.common.msg_util import *
from worldcup.matches.models import *
from worldcup.teams.models import Team
from worldcup.predictions.models import PredictionStage2
from datetime import datetime
import re

match_data = '''49	1a	2b	1	6/26	16:00	Nelson Mandela Bay
50	1c	2d	1	6/26	20:30	Rustenburg
51	1d	2c	2	6/27	16:00	Mangaung / Bloemfontein
52	1b	2a	2	6/27	20:30	Johannesburg
53	1e	2f	3	6/28	16:00	Durban
54	1g	2h	3	6/28	20:30	Johannesburg
55	1f	2e	4	6/29	16:00	Tshwane/Pretoria
56	1h	2g	4	6/29	20:30	Cape Town
57	1e,2f	1g,2h	0	7/2	16:00	Nelson Mandela Bay
58	1a,2b	1c,2d	0	7/2	20:30	Johannesburg
59	1b,2a	1d,2c	0	7/3	16:00	Cape Town
60	1f,2e	1h,2g	0	7/3	20:30	Johannesburg
61	1	3	0	7/6	20:30	Cape Town
62	2	4	0	7/7	20:30	Durban
63	1,3	2,4	0	7/11	20:30	Nelson Mandela Bay
64	1,3	2,4	0	7/12	20:30	Johannesburg'''.split('\n')

class MatchTeamData:
    def __init__(self, dline):
        items = dline.split('\t')
        if not len(items) == 7:
            return
        match_num, team1_choices, team2_choices, grid_group, dt, time_str, venue_str = items

        self.match_num = int(match_num)
        self.team1_choices = team1_choices
        self.team2_choices = team2_choices
        self.grid_group = int(grid_group)
        '''
        if choices have /d/w: find 1 team based on group letter and placement
            - static
                - get_team_by_group_and_standing(group, standing)
            Team.objects.filter(group__name='Group A/B/C/D/E', group_stage_standing=1 or 2)

        if choices have /d/d: find team1 and team2 in that match
            - get_teams_in_match(match_num)
                - retrieve match
                - user previous method: get_team_by_group_and_standing
            
        if choices have /d,/d: find all teams in that grid
            - get teams by grid
                - retrieve matchTeamData by grid num
                - get_teams_in_match
                
        - find_by_match_num   { match_num : matchTeamData }
            
        '''
    
    def get_all_teams(self, lu_by_grid_num):
        teams = []
        
        teams = self.get_team_choices(lu_by_grid_num)
        teams += self.get_team_choices(lu_by_grid_num, use_team2_choices=True)
        return teams
        
        
    def get_team_choices(self, lu_by_grid_num, use_team2_choices=False):
        #   default to team 1 choices or specify 'use_teams2_choices'
        
        #   e.g. '1a', '1a,2b', '1', '1,2'
        teams = []
        
        if use_team2_choices:
            team_choices = self.team2_choices.split(',')
        else:
            team_choices = self.team1_choices.split(',')

        for tid in team_choices:
            if re.match('^(1|2)[a-h]$', tid):   # single team
                standing = int(tid[0])
                group_name = 'Group %s' % tid[1].upper()
                
                team_qset = Team.objects.filter(group__name=group_name, group_stage_standing=standing)
                if team_qset.count() > 0:
                    teams += list(team_qset)
                    
            elif re.match('^(1|2|3|4)$', tid):   # grid num
                #msg('grid num: %s' % tid)
                #msg(lu_by_grid_num)
                glist = lu_by_grid_num.get(int(tid))
                #msg('glist: %s' % glist)
                if glist is not None:
                    for mtd_obj in glist:
                        teams += mtd_obj.get_all_teams(lu_by_grid_num)

        return teams

                    
class MatchTeamDataManager:
    def __init__(self):
        self.lu_by_match_num = {}
        self.lu_by_grid_num = {}
        self.mtd_list = []
        self.load_data()
        
    def load_data(self):
        for line in match_data:
            mtd = MatchTeamData(line)
            self.mtd_list.append(mtd)
            # match num lookup
            self.lu_by_match_num.update({ mtd.match_num : mtd })

            # grid lookup
            grid_list = self.lu_by_grid_num.get(mtd.grid_group, [])
            grid_list.append(mtd)
            self.lu_by_grid_num.update({ mtd.grid_group : grid_list })
            
    def get_ko_team1_choices(self, match_num):
        mtd = self.lu_by_match_num.get(match_num)
        if mtd is None:
            return None
        return mtd.get_team_choices(self.lu_by_grid_num)

    def get_ko_team2_choices(self, match_num):
        mtd = self.lu_by_match_num.get(match_num)
        if mtd is None:
            return None
        return mtd.get_team_choices(self.lu_by_grid_num, use_team2_choices=True)

"""
from worldcup.teams.models import Team
for t in Team.objects.all():
    t.group_stage_standing = 0
    t.save()
    
    
for g in '''a b c d e f g h'''.split():
    gname = 'Group %s' % g.upper()
    print '-' * 40
    print gname
    for idx, tobj in enumerate( Team.objects.filter(group__name=gname)):
        if idx==2: break
        tobj.group_stage_standing = idx+1
        tobj.save()
        print tobj,  tobj.group_stage_standing
    
    
"""
