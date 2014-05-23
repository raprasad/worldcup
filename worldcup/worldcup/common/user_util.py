from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from worldcup.auth_active_directory.urls import *
from django.core.urlresolvers import reverse
from worldcup.settings import  DEBUG

def view_auth_page(request):
    """
    Send the user to the login page
    """
    return HttpResponseRedirect(reverse('view_login') + '?next=%s' % request.get_full_path())


def get_username(request):
    """
    Return several pieces of information used on every page
    """
        
    if request.user and request.user.username:
        return {'username':request.user.username
                , 'user': request.user
                , 'is_authenticated' :request.user.is_authenticated()
                , 'request_path' : request.path
                , 'DEBUG' : DEBUG
                
        }

    return { 'username': None
            , 'DEBUG' : DEBUG}
