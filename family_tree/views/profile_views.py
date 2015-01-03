# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person, Biography
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

@login_required
def profile(request, person_id = 0, requested_language = ''):
    '''
    Shows the profile of a person
    '''

    #If no id is supplied then get users profile
    try:
        if person_id == 0:
            person = Person.objects.get(user_id = request.user.id)
        else:
            person = Person.objects.get(id = person_id)
    except:
        from family_tree.views.tree_views import no_match_found
        return no_match_found(request)

    biography = Biography.objects.get_biography(person.id, requested_language, request.LANGUAGE_CODE)
    if biography is None:
        biography = Biography(
                        person_id=person.id,
                        language=(requested_language if requested_language else request.LANGUAGE_CODE),
                        content=_('A biography has not yet been written for this language'))

    template = loader.get_template('family_tree/profile.html')

    context = RequestContext(request,{
                                'person' : person,
                                'languages' : settings.LOCALES,
                                'biography' : biography,
                            })

    response = template.render(context)
    return HttpResponse(response)




