from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
    '''
    Index page this redirects to users home page if they are logged in
    '''
    if request.user.is_authenticated():
        request.session['django_language'] = request.user.language
        return HttpResponseRedirect('/home/')
    else:
        return about(request)


def about(request):
    '''
    The about page is visible on if you are logged in or not
    '''
    if request.user.is_authenticated():
        request.session['django_language'] = request.user.language
        template = loader.get_template('about.html')
        context = RequestContext(request)
        response = template.render(context)
        return HttpResponse(response)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('about.html', c)