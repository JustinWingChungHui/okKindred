# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Biography
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from family_tree.decorators import same_family_required

@login_required
@same_family_required
def profile(request, person_id = 0, person = None, requested_language = '', edit_mode = False):
    '''
    Shows the profile of a person
    '''

    #Cannot enter edit mode if profile is locked
    if request.user.id != person.user_id and person.locked == True:
        edit_mode = False


    if edit_mode:

        #Cannot edit the first language or email of someone else if they are a confirmed user
        if not person.user_id:
            show_email_and_language = True
        else:
            if not person.user.is_confirmed or request.user.id == person.user_id:
                show_email_and_language = True
            else:
                show_email_and_language = False


        template = loader.get_template('family_tree/edit_profile.html')
        context = RequestContext(request,{
                                    'person' : person,
                                    'languages' : settings.LOCALES,
                                    'requested_language': requested_language,
                                    'show_locked': (True if request.user.id == person.user_id else False),
                                    'show_email_and_language' : show_email_and_language,
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
@same_family_required
def edit_profile(request, person_id = 0, person = None, requested_language = ''):
    '''
    The form that allows a user to edit the details of a person.  It displays the for and processes it
    '''
    return profile(request, person_id, requested_language, edit_mode = True)




@login_required
@same_family_required
def update_person(request, person_id = 0, person = None):
    '''
    This is an API to set the property of a person field
    Expecting POST values of:
        pk: person ID
        name: field name to change
        value: new value
    '''

    field_name = request.POST.get("name")

    if request.method != 'POST':
        return HttpResponse(status=405, content="Only POST requests allowed")

    #Make sure we can't change locked profiles
    if person.locked and person.user_id != request.user.id:
        return HttpResponse(status=405, content="Access denied to locked profile")

    #Check we don't change any settings for a confirmed user
    if person.user_id and field_name in ['email', 'language']:
        if person.user.is_confirmed and person.user_id != request.user.id:
            return HttpResponse(status=405, content="Access denied to change confirmed user settings")

    try:
        setattr(person, field_name, request.POST.get("value"))
        person.save()
        return HttpResponse(status=200, content="OK")

    except Exception as e:
        return HttpResponse(status=405, content=e)



@login_required
@same_family_required
def edit_biography(request, person_id = 0, person = None, requested_language = 'en'):
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
@same_family_required
def update_biography(request, person_id = 0, person = None, requested_language = 'en'):
    '''
    API to update biography
    '''

    if person.locked and person.user_id != request.user.id:
        return HttpResponse(status=405, content="Access denied to locked profile")

    try:
        biography = Biography.objects.get(person_id=person_id, language=requested_language)
    except:
        biography = Biography(person_id = person_id, language = requested_language)

    biography.content = request.POST.get("biography","")
    biography.save()
    return profile(request, person_id, requested_language)




