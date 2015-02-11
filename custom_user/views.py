'''
This is for site wide views
http://procrastinatingdev.com/django/using-configurable-user-models-in-django-1-5/
'''

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from axes.decorators import is_already_locked, get_ip, check_request
from axes.models import AccessLog


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
    if is_already_locked(request):
        return account_locked(request)

    username = request.POST.get('username', '').lower()
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    login_unsuccessful = user is None

    AccessLog.objects.create(
                             user_agent=request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
                             ip_address=get_ip(request),
                             username=username,
                             http_accept=request.META.get('HTTP_ACCEPT', '<unknown>'),
                             path_info=request.META.get('PATH_INFO', '<unknown>'),
                             trusted=not login_unsuccessful,
                             )

    check_request(request, login_unsuccessful)

    if not login_unsuccessful:
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

def account_locked(request):
    return render_to_response('custom_user/account_locked.html')