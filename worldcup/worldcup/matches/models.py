from django.db import models
import os
from django.template.defaultfilters import slugify 
from django.core.urlresolvers import reverse
from worldcup.teams.models import Group, Team

MATCH_TYPE_GROUP_STAGE = 'Group Stage'
MATCH_TYPE_KNOCKOUT_STAGE = 'Knockout Stage'

class Venue(models.Model):
    """Field location"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, blank=True)

    def save(self):
          self.slug = slugify(self.name)
          super(Venue, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


'''
alter table matches_matchtype add column `last_day_to_predict` datetime default '2010-06-10 23:59:00';

'''
class MatchType(models.Model):
    """Group Matches, Round of 16, Quarter finals, etc."""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, blank=True)
    last_day_to_predict = models.DateTimeField()

    def save(self):
          self.slug = slugify(self.name)
          super(MatchType, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Match(models.Model):
    """Scheduled Match"""
    name = models.CharField(max_length=200, blank=True)
    match_type = models.ForeignKey(MatchType)
    team1 = models.ForeignKey(Team)
    team2 = models.ForeignKey(Team, related_name='team2')

    note = models.CharField(max_length=255, blank=True)
    
    venue = models.ForeignKey(Venue)
    
    match_time = models.DateTimeField()

    score_recorded = models.BooleanField(default=False)
    
    team1_regular_time_score = models.IntegerField(default=0)    
    team2_regular_time_score = models.IntegerField(default=0)    
    
    team1_final_score = models.IntegerField(default=0)    
    team2_final_score = models.IntegerField(default=0)    
    
    is_draw = models.BooleanField(default=False, help_text='auto-filled on save')

    last_updated = models.DateTimeField(auto_now=True)
    
    def did_team1_win(self):
        if self.team1_final_score > self.team2_final_score:
            return True
        return False

    def did_team2_win(self):
        if self.team1_final_score < self.team2_final_score:
            return True
        return False
    
    def get_winner(self):
        if not self.score_recorded:
            return None
            
        if self.team1_final_score > self.team2_final_score:
            return self.team1
        if self.team1_final_score < self.team2_final_score:
            return self.team2
        return None
    
    def is_ko_draw(self):
        if not self.score_recorded:
            return False

        if self.team1_regular_time_score == self.team2_regular_time_score:
            return True
        
        return False
      
    def was_match_a_draw(self):
        if not self.score_recorded:
            return False
                
        if self.get_winner() is None:
            return True
        
        return False    

    def __unicode__(self):
        return self.name

    def save(self):
      self.is_draw = self.was_match_a_draw()
      
      if self.match_type.name == 'MATCH_TYPE_GROUP_STAGE':
          self.name = '(%s) %s vs. %s - %s' % (self.id, self.team1, self.team2, self.match_time.strftime('%m/%d %I:%M%p'))
      if self.name == None or self.name =='':
          self.name = 'id: %s unlabeled!'  % self.id
      else:
          pass
          
      super(Match, self).save()


    class Meta:
      ordering = ['match_time']
      verbose_name_plural = "matches"

v = """Johannesburg - JSC		
Cape Town		
Johannesburg - JEP		
Nelson Mandela Bay		
Rustenburg		
Polokwane		
Durban		
Tshwane/Pretoria		
Johannesburg - JSC		
Mangaung / Bloemfontein		
Cape Town		
Rustenburg		
Nelson Mandela Bay		
Johannesburg - JEP		
Nelspruit		
Durban		
Tshwane/Pretoria		
Polokwane		
Mangaung / Bloemfontein		
Johannesburg - JSC		
Nelson Mandela Bay		
Johannesburg - JEP		
Cape Town		
Rustenburg		
Durban		
Tshwane/Pretoria		
Mangaung / Bloemfontein		
Nelspruit		
Johannesburg - JSC		
Cape Town		
Nelson Mandela Bay		
Johannesburg - JEP		
Rustenburg		
Mangaung / Bloemfontein		
Durban		
Polokwane		
Nelson Mandela Bay		
Tshwane/Pretoria		
Johannesburg - JSC		
Nelspruit		
Johannesburg - JEP		
Polokwane		
Rustenburg		
Cape Town		
Durban		
Nelspruit		
Tshwane/Pretoria		
Mangaung / Bloemfontein""".split('\n')
'''    
v = map(lambda x: x.strip(), v)
lu = {}
for p in v: lu.update({p:1})
from worldcup.matches.models import Venue
for k in lu.keys(): v = Venue(name=k); v.save()

v = Venue.objects.all()
v.delete()
'''