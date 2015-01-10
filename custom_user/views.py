'''
This is for site wide views
http://procrastinatingdev.com/django/using-configurable-user-models-in-django-1-5/
'''

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf




'''
Authentication views based on https://www.youtube.com/watch?v=CFypO_LNmcc
'''

def login(request):
    '''
    Handles login requests
    '''
    c = {}
    c.update(csrf(request))
    return render_to_response('custom_user/login.html', c)

def auth_view(request):
    '''
    Handles the authentication from the login screen
    '''
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/accounts/invalid')

def logged_in(request):
    return render_to_response('custom_user/logged_in.html',
                                {'username': request.user.username})

def invalid_login(request):
    return render_to_response('custom_user/invalid_login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')