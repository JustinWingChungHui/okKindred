from django.http import HttpResponseRedirect
from django.shortcuts import render
from family_tree.models import Person

def index(request):
    '''
    Index page this redirects to users home page if they are logged in
    '''
    if request.user != None and request.user.is_authenticated():
        request.session['django_language'] = request.user.language

        person_id = Person.objects.get(user_id = request.user.id).id

        return HttpResponseRedirect('/tree/{0}/'.format(person_id))
    else:
        return about(request)


def about(request):
    '''
    The about page is visible on if you are logged in or not
    '''
    if request.user != None and request.user.is_authenticated():
        request.session['django_language'] = request.user.language

    return render(request, 'about.html')


def csrf_failure(request, reason=""):
    response = render(request, 'csrf_failure.html', {})
    response.status_code = 403
    return response

def handler404(request):
    '''
    Custom 404 handler
    '''
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler505(request):
    '''
    Custom 505 handler
    '''
    response = render(request, '505.html', {})
    response.status_code = 505
    return response