from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import RequestContext, loader
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
        template = loader.get_template('about.html')
        context = RequestContext(request)
        response = template.render(context)
        return HttpResponse(response)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('about.html', c)


def handler404(request):
    '''
    Custom 404 handler
    '''
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler505(request):
    '''
    Custom 505 handler
    '''
    response = render_to_response('505.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 505
    return response