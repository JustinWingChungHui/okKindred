from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from family_tree.models import Person

import json

def index(request):
    '''
    Index page this redirects to users home page if they are logged in
    '''
    if request.user != None and request.user.is_authenticated:
        request.session['django_language'] = request.user.language

        person_id = Person.objects.get(user_id = request.user.id).id

        return HttpResponseRedirect('/tree/{0}/'.format(person_id))
    else:
        return about(request)


def languages(request):
    '''
    Provides a JSON response of all supported language codes and localised language display text
    '''
    response = []

    if request.user != None and request.user.is_authenticated:
        request.session['django_language'] = request.user.language

    for code, display in settings.LANGUAGES:
        response.append({ 'value' : code, 'text' : display.__str__() })

    return HttpResponse(json.dumps(response), content_type="application/json")


def about(request):
    '''
    The about page is visible on if you are logged in or not
    '''
    if request.user != None and request.user.is_authenticated:
        request.session['django_language'] = request.user.language

    return render(request, 'about.html')


def csrf_failure(request, reason=""):
    response = render(request, 'csrf_failure.html', {})
    response.status_code = 403
    return response

def handler404(request, *args, **argv):
    '''
    Custom 404 handler
    '''
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler505(request, *args, **argv):
    '''
    Custom 505 handler
    '''
    response = render(request, '505.html', {})
    response.status_code = 505
    return response