# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
from family_tree.services import tree_service
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

    related_data = tree_service.get_related_data(person)

    template = loader.get_template('family_tree/tree.html')

    context = RequestContext(request,{
                                'css_normal' : _get_css(person, related_data, pixel_width=970),
                                'css_320' : _get_css(person, related_data, pixel_width=320),
                                'css_480' : _get_css(person, related_data, pixel_width=480),
                                #Matches bootstrap media queries
                                'css_768' : _get_css(person, related_data, pixel_width=750),
                                'css_992' : _get_css(person, related_data, pixel_width=970),
                                'css_1200' : _get_css(person, related_data, pixel_width=1170),
                                'people': related_data.people_upper + related_data.people_lower + related_data.people_same_level,
                                'relations': related_data.relations,
                                'person' : person,
                            })

    response = template.render(context)
    return HttpResponse(response)



def _get_css(centred_person, related_data, pixel_width):
    '''
    Gets the css for a load of people
    Handles the media queries as well
    '''

    #Mobile devices scale down nodes
    if pixel_width < 768:
        node_width = 90
        height_change = 150
    else:
        node_width = 120
        height_change = 200

    css = []

    height = 0

    #People above
    if len(related_data.people_upper) > 1:

        gap = int((pixel_width - len(related_data.people_upper) * node_width)  / (len(related_data.people_upper) - 1))
        position_left = 0

        for person in related_data.people_upper:
            css.append('#person%s{left: %spx; top: 0px;}'% (person.id, position_left))
            position_left = position_left + node_width + gap

        height = height_change

    if len(related_data.people_upper) == 1:
        person = related_data.people_upper[0]
        position_left = int((pixel_width - node_width) / 2)
        css.append('#person%s{left: %spx; top: 0px;}'% (person.id, position_left))

        height = height_change


    #Same Level
    if len(related_data.people_same_level) > 0:
        gap = int((pixel_width - (len(related_data.people_same_level) + 1) * node_width)  / (len(related_data.people_same_level)))
        position_left = 0

        count = 1
        for person in related_data.people_same_level:
            css.append('#person%s{left: %spx; top: %spx;}'% (person.id, position_left, height))

            count +=1
            if count <= (len(related_data.people_same_level) + 1) / 2:
                position_left = position_left + gap
            else:
                position_left = position_left + gap + node_width + gap


    position_left = int((pixel_width - node_width) / 2)
    css.append('#person%s{left: %spx; top: %spx;}' % (centred_person.id, position_left, height))

    height = height + height_change + 50

    #People below
    if len(related_data.people_lower) > 1:
        gap = int((pixel_width - len(related_data.people_lower) * node_width)  / (len(related_data.people_lower) - 1))
        position_left = 0

        for person in related_data.people_lower:
            css.append('#person%s{left: %spx; top: %spx;}'% (person.id, position_left, height))
            position_left = position_left + node_width + gap

    if len(related_data.people_lower) == 1:
        person = related_data.people_lower[0]
        position_left = int((pixel_width - node_width) / 2)
        css.append('#person%s{left: %spx; top: %spx;}'% (person.id, position_left, height))


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


    people, relations = tree_service.get_related_path(user_person, person)

    if people is None:
        raise Http404


    template = loader.get_template('family_tree/how_am_i_related.html')

    context = RequestContext(request,{
                                'people': people,
                                'relations' :relations,
                            })

    response = template.render(context)
    return HttpResponse(response)


@login_required
@set_language
def whole_tree(request):
    '''
    Generates view to show entire family tree
    Crazy!!!
    '''

    people_list_by_hierarchy, relations = tree_service.get_whole_tree(request.user.family_id)
    people = []
    largest_layer = 0

    for hierarchy, people_list in people_list_by_hierarchy.items():

        if largest_layer < len(people_list):
            largest_layer = len(people_list)

        for person in people_list:
            people.append(person)


    template = loader.get_template('family_tree/whole_tree.html')

    context = RequestContext(request,{
                                'people': people,
                                'relations' :relations,
                                'css' : _get_css_all(largest_layer, people_list_by_hierarchy)
                            })

    response = template.render(context)
    return HttpResponse(response)


@login_required
@set_language
@same_family_required
def get_descendants(request, person_id = 0, person = None):
    '''
    Gets a view of the descendants
    '''
    people_list_by_hierarchy, relations = tree_service.get_descendants(person)
    return _render_blood_relations(request, people_list_by_hierarchy, relations )


@login_required
@set_language
@same_family_required
def get_ancestors(request, person_id = 0, person = None):
    '''
    Gets a view of the descendants
    '''
    people_list_by_hierarchy, relations = tree_service.get_ancestors(person)
    return _render_blood_relations(request, people_list_by_hierarchy, relations )


def _render_blood_relations(request, people_list_by_hierarchy, relations):
    '''
    Gets a view of all blood relations
    '''
    people = []
    largest_layer = 0

    for hierarchy, people_list in people_list_by_hierarchy.items():

        if largest_layer < len(people_list):
            largest_layer = len(people_list)

        for person in people_list:
            people.append(person)


    template = loader.get_template('family_tree/whole_tree.html')

    context = RequestContext(request,{
                                'people': people,
                                'relations' :relations,
                                'css' : _get_css_all(largest_layer, people_list_by_hierarchy),
                                'css_mobile' : _get_css_all_mobile(largest_layer, people_list_by_hierarchy)
                            })

    response = template.render(context)
    return HttpResponse(response)



def _get_css_all(largest_layer, people_list_by_hierarchy):
    '''
    Returns css to display all large family tree
    '''
    total_width = 150 * (largest_layer + 1)
    css = []
    hierarchy_score = 0
    left = 0
    top = -300

    for hierarchy, people_list in people_list_by_hierarchy.items():

        if hierarchy > hierarchy_score:
            hierarchy_score = hierarchy
            top = top + 300
            gap = (total_width) / (len(people_list) + 1)
            left = -150

        for person in people_list:
            left = left + gap
            css.append('#person%s{left: %spx; top: %spx;}'% (person.id, left, top))

    return ''.join(css)

def _get_css_all_mobile(largest_layer, people_list_by_hierarchy):
    '''
    Returns css to display all large family tree
    '''
    total_width = 100 * (largest_layer + 1)
    css = []
    hierarchy_score = 0
    left = 0
    top = -180

    for hierarchy, people_list in people_list_by_hierarchy.items():

        if hierarchy > hierarchy_score:
            hierarchy_score = hierarchy
            top = top + 180
            gap = (total_width) / (len(people_list) + 1)
            left = -100

        for person in people_list:
            left = left + gap
            css.append('#person%s{left: %spx; top: %spx;}'% (person.id, left, top))
    return ''.join(css)