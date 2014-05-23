from django.db import models
import os
from django.template.defaultfilters import slugify 
from django.core.urlresolvers import reverse
from worldcup.settings import TEAM_LOGO_IMAGES

"""
from worldcup.teams.models import *
lst = Group.objects.all()
lst.delete()
for g in '''a b c d e f g h'''.split():
    ng = Group(name='Group %s' % g.upper())
    ng.save()
"""


class Group(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    
    def save(self):
          self.slug = slugify(self.name)
          super(Group, self).save()

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


        
class Team(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(Group)
    slug = models.SlugField(max_length=200, blank=True)
    logo = models.FilePathField(max_length=200, path=TEAM_LOGO_IMAGES, recursive=True, blank=True)  #match="foo.*", recursive=True)
    active = models.BooleanField(default=True)
    group_stage_standing = models.IntegerField(default=0)
    
    def save(self):
          self.slug = slugify(self.name)
          super(Team, self).save()

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
   
TEAM_NOT_DETERMINED = 'Team Not Determined'
GROUP_NOT_DETERMINED = 'Group Not Determined'
     
def get_team_not_determined():
    """
    Used for Stage 2 predictions, where user has to pick the team
    """
    try:
        t = Team.objects.get(name=TEAM_NOT_DETERMINED)    
    except Team.DoesNotExist:        
        try:
            g = Group.objects.get(name=GROUP_NOT_DETERMINED)
        except Group.DoesNotExist:
            g = Group(name=GROUP_NOT_DETERMINED)
            g.save()
        
        t = Team(name=TEAM_NOT_DETERMINED
                , group=g
                , active=True  )
        t.save()
    return t
    
      
"""
tlist = '''Group A
France
Mexico
Uruguay
South Africa

Group B
Argentina
Greece
Nigeria
Korea Republic

Group C
England
USA
Slovenia
Algeria

Group D
Germany
Serbia
Australia
Ghana

Group E
Netherlands
Cameroon
Denmark
Japan

Group F
Italy
Paraguay
Slovakia
New Zealand

Group G
Brazil
Portugal
Cote d'Ivoire
Korea DPR

Group H
Spain
Chile
Switzerland
Honduras'''.split('\n')

from worldcup.teams.models import *
tlist = filter(lambda x: not x == '', tlist)
cg = None
for line in tlist:
    print line
    if line.startswith('Group'):
        print 'Attempt to retrieve: %s' % line
        cg = Group.objects.get(name=line)
    else:
        t = Team(name=line, group=cg)
        t.save()
"""
