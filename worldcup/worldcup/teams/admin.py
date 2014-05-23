from django.contrib import admin
from worldcup.teams.models import Group, Team

class GroupAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', ]
admin.site.register(Group, GroupAdmin)


class TeamAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'slug', 'logo', 'group', 'group_stage_standing', 'active']
    list_filter = ['active', 'group', 'group_stage_standing']
    
admin.site.register(Team, TeamAdmin)

