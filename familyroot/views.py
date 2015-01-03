'''
This is for site wide views
http://procrastinatingdev.com/django/using-configurable-user-models-in-django-1-5/
'''

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
    '''
    Index page this redirects to users home page if they are logged in
    '''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        return about(request)


def about(request):
    '''
    The about page is visible on if you are logged in or not
    '''
    if request.user.is_authenticated():
        template = loader.get_template('about.html')
        context = RequestContext(request)
        response = template.render(context)
        return HttpResponse(response)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('about.html', c)



'''
Authentication views based on https://www.youtube.com/watch?v=CFypO_LNmcc
'''

def login(request):
    '''
    Handles login requests
    '''
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_view(request):
    '''
    Handles the authentication from the login screen
    '''
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return index(request)
    else:
        return HttpResponseRedirect('/accounts/invalid')

def logged_in(request):
    return render_to_response('logged_in.html',
                                {'username': request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return about(request)
