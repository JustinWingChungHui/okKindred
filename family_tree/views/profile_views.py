# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person, Biography
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404


@login_required
def profile(request, person_id = 0, requested_language = '', edit_mode = False):
    '''
    Shows the profile of a person
    '''

    #If no id is supplied then get users profile
    if person_id == 0:
        person = get_object_or_404(Person, user_id = request.user.id)
    else:
        person = get_object_or_404(Person, id = person_id)


    #Cannot enter edit mode if profile is locked
    if request.user.id != person.user_id and person.locked == True:
        edit_mode = False


    if edit_mode:
        template = loader.get_template('family_tree/edit_profile.html')
        context = RequestContext(request,{
                                    'person' : person,
                                    'languages' : settings.LOCALES,
                                    'requested_language': requested_language,
                                    'show_locked': (True if request.user.id == person.user_id else False),
                                })
    else:


        #Get the biography
        biography = Biography.objects.get_biography(person.id, requested_language, ('en' if request.LANGUAGE_CODE.startswith('en') else request.LANGUAGE_CODE))
        if biography is None:
            biography = Biography(
                            person_id=person.id,
                            language=(requested_language if requested_language else 'en'),
                            content=_('A biography has not yet been written for this language'))

        template = loader.get_template('family_tree/profile.html')

        context = RequestContext(request,{
                                    'person' : person,
                                    'languages' : settings.LOCALES,
                                    'biography' : biography,
                                    'requested_language': requested_language,
                                    'locked': (True if request.user.id != person.user_id and person.locked else False),
                                })

    response = template.render(context)
    return HttpResponse(response)


@login_required
def edit_profile(request, person_id = 0, requested_language = ''):
    '''
    The form that allows a user to edit the details of a person.  It displays the for and processes it
    '''
    return profile(request, person_id, requested_language, edit_mode = True)




@login_required
def update_person(request):
    '''
    This is an API to set the property of a person field
    Expecting POST values of:
        pk: person ID
        name: field name to change
        value: new value
    '''

    if request.method != 'POST':
        return HttpResponse(status=405, content="Only POST requests allowed")

    try:
        person = Person.objects.get(id = request.POST.get("pk"))
    except:
        return HttpResponse(status=405, content="Person ID is invalid")

    if person.locked and person.user_id != request.user.id:
        return HttpResponse(status=405, content="Access denied to locked profile")

    try:
        setattr(person, request.POST.get("name"), request.POST.get("value"))
        person.save()
        return HttpResponse(status=200, content="OK")

    except Exception:
        return HttpResponse(status=405, content="Error updating person")



@login_required
def edit_biography(request, person_id = 0, requested_language = 'en'):
    '''
    View to edit the biography in a particular language
    '''

    try:
        biography = Biography.objects.get_biography(person_id, requested_language)
    except:
        from family_tree.views.tree_views import no_match_found
        return no_match_found(request)

    template = loader.get_template('family_tree/edit_biography.html')

    context = RequestContext(request,{
                                'person_id' : person_id,
                                'language' : requested_language,
                                'biography' : biography,
                            })
    response = template.render(context)
    return HttpResponse(response)



@login_required
def update_biography(request, person_id, requested_language):
    '''
    API to update biography
    '''

    try:
        person = Person.objects.get(id = person_id)
    except:
        return HttpResponse(status=405, content="Person ID is invalid")

    if person.locked and person.user_id != request.user.id:
        return HttpResponse(status=405, content="Access denied to locked profile")

    try:
        biography = Biography.objects.get_biography(person_id, requested_language)
    except:
        biography = Biography(person_id = person_id, langauage = requested_language)

    biography.content = request.POST.get("biography","")
    biography.save()
    return edit_biography(request, person_id, requested_language)
