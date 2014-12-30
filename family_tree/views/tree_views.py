# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person



@login_required
def tree(request, person_id = 0):
    '''
    Shows a tree view centred on the person
    Shows by default one relation distance
    '''

    #If no id is supplied then we centre the view on the user
    try:
        if person_id == 0:
            person = Person.objects.get(user_id = request.user.id)
        else:
            person = Person.objects.get(id = person_id)
    except:
        return no_match_found(request)

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
        gap = pixel_width / (len(related_data.people_upper) + 1)
        position_left = gap

        for person in related_data.people_upper:
            css.append('#person%s{left: %spx; top: 0px;}'% (person.id, position_left))
            position_left = position_left + gap

    #Same Level
    if len(related_data.people_same_level) > 0:
        gap = pixel_width / (len(related_data.people_same_level) + 1)
        position_left = gap

        for person in related_data.people_same_level:
            css.append('#person%s{left: %spx; top: 100px;}'% (person.id, position_left))
            position_left = position_left + gap

    #People below
    if len(related_data.people_lower) > 0:
        gap = pixel_width / (len(related_data.people_lower) + 1)
        position_left = gap

        for person in related_data.people_lower:
            css.append('#person%s{left: %spx; top: 200px;}'% (person.id, position_left))
            position_left = position_left + gap

    position_left = pixel_width / 3
    css.append('#person%s{left: %spx; top: 100px;}' % (centred_person.id, position_left))

    return ''.join(css)



@login_required
def no_match_found(request):
    '''
    Error page if person is not found
    '''

    template = loader.get_template('family_tree/no_match_found.html')

    context = RequestContext(request)
    response = template.render(context)
    return HttpResponse(response)

