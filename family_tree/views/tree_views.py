# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
from family_tree.models import Relation


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

    related_data = get_related_data(person)

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



def get_related_data(person):
    '''
    Gets all the relations and people that are related to the arguement person as a named tuple
    people_upper: People with a higher hierachy score (e.g. parents)
    people_lower: People with a lower hierachy score (e.g. kids)
    relations: List of relations
    '''
    import collections
    related_data = collections.namedtuple('related_data', ['people_upper', 'people_same_level', 'people_lower', 'relations'])

    from django.db.models import Q
    relations = Relation.objects.filter(Q(from_person=person) | Q(to_person=person))

    #Yeah get some raw SQL on!  We are assuming that the 'from' has a higher hierarchy than the 'to'
    people_upper = list(Person.objects.raw("""   SELECT p.*
                                            FROM family_tree_person p
                                            INNER JOIN family_tree_relation r
                                                ON r.from_person_id = p.id
                                            WHERE r.to_person_id = %s AND r.relation_type = 2
                                            ORDER BY p.hierarchy_score, gender
                                    """, [person.id]))

    people_same_level = list(Person.objects.raw("""  SELECT p.*
                                                FROM family_tree_person p
                                                INNER JOIN family_tree_relation r
                                                    ON r.from_person_id = p.id
                                                WHERE r.to_person_id = {0} AND r.relation_type = 1
                                                UNION ALL
                                                SELECT p.*
                                                FROM family_tree_person p
                                                INNER JOIN family_tree_relation r
                                                    ON r.to_person_id = p.id
                                                WHERE r.from_person_id = {0} AND r.relation_type = 1
                                                ORDER BY p.hierarchy_score, gender
                                    """.format(person.id)))

    people_lower = list(Person.objects.raw("""   SELECT p.*
                                            FROM family_tree_person p
                                            INNER JOIN family_tree_relation r
                                                ON r.to_person_id = p.id
                                            WHERE r.from_person_id = %s AND r.relation_type = 2
                                            ORDER BY p.hierarchy_score, gender
                                    """, [person.id]))

    return related_data(people_upper, people_same_level, people_lower, relations)



@login_required
def no_match_found(request):
    '''
    Error page if person is not found
    '''

    template = loader.get_template('family_tree/no_match_found.html')

    context = RequestContext(request)
    response = template.render(context)
    return HttpResponse(response)

@login_required
def jquery(request, person_id = 0):
    '''
    Experimental view using jquery
    '''

    #If no id is supplied then we centre the view on the user
    try:
        if person_id == 0:
            person = Person.objects.get(user_id = request.user.id)
        else:
            person = Person.objects.get(id = person_id)
    except:
        return no_match_found(request)

    template = loader.get_template('family_tree/jquery.html')

    context = RequestContext(request)


    response = template.render(context)
    return HttpResponse(response)
