# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
from family_tree.decorators import same_family_required
from custom_user.decorators import set_language
from django.http import Http404


@login_required
@set_language
@same_family_required
def tree(request, person_id = 0, person = None):
    '''
    Shows a tree view centred on the person
    Shows by default one relation distance
    '''

    related_data = Person.objects.get_related_data(person)

    template = loader.get_template('family_tree/tree.html')

    context = RequestContext(request,{
                                'css_320' : get_css(person, related_data, pixel_width=320),
                                'css_480' : get_css(person, related_data, pixel_width=480),
                                'css_768' : get_css(person, related_data, pixel_width=768),
                                'css_1024' : get_css(person, related_data, pixel_width=1024),
                                'css_1200' : get_css(person, related_data, pixel_width=1200),
                                'css_1900' : get_css(person, related_data, pixel_width=1900),
                                'css_2400' : get_css(person, related_data, pixel_width=2400),
                                'people': related_data.people_upper + related_data.people_lower + related_data.people_same_level,
                                'relations': related_data.relations,
                                'person' : person,
                            })

    response = template.render(context)
    return HttpResponse(response)

def get_css(centred_person, related_data, pixel_width):
    '''
    Gets the css for a load of people
    Handles the media queries as well
    '''

    css = []

    #People above
    if len(related_data.people_upper) > 0:
        gap = int(pixel_width / (len(related_data.people_upper) * 2 - 1))
        position_left = 0

        for person in related_data.people_upper:
            css.append('#person%s{left: %spx; top: 0px;}'% (person.id, position_left))
            position_left = position_left + gap

    #Same Level
    if len(related_data.people_same_level) > 0:
        gap = int(pixel_width / (len(related_data.people_same_level) * 2 - 1))
        position_left = 0

        for person in related_data.people_same_level:
            css.append('#person%s{left: %spx; top: 200px;}'% (person.id, position_left))
            position_left = position_left + gap

    #People below
    if len(related_data.people_lower) > 0:
        gap = int(pixel_width / (len(related_data.people_lower) * 2 - 1))
        position_left = 0

        for person in related_data.people_lower:
            css.append('#person%s{left: %spx; top: 400px;}'% (person.id, position_left))
            position_left = position_left + gap

    position_left = int(pixel_width / 3)
    css.append('#person%s{left: %spx; top: 200px;}' % (centred_person.id, position_left))

    return ''.join(css)


@login_required
@set_language
@same_family_required
def how_am_i_related_view(request, person_id = 0, person = None):
    '''
    Gets the how am i related view
    '''

    #Get user person
    user_person = Person.objects.get(user_id = request.user.id)


    people, relations = Person.objects.get_related_path(user_person, person)

    if people is None:
        raise Http404


    template = loader.get_template('family_tree/how_am_i_related.html')

    context = RequestContext(request,{
                                'people': people,
                                'relations' :relations,
                            })

    response = template.render(context)
    return HttpResponse(response)

