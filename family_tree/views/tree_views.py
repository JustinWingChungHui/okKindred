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

    template = loader.get_template('family_tree/tree.html')

    context = RequestContext(request)

    #context = RequestContext(request,{
    #                          'pages': Page.objects.filter(show_on_menu = 1).order_by('sequence'),
    #                          'page': Page.objects.get(tab_link = 'aktualności'),
    #                         'articles': Article.objects.filter(published = True).order_by('-creation_date')[offset:num_article_stubs_per_page + offset],
    #                          'show_previous': (page_number > 1),
    #                          'show_next': (page_number < num_pages),
    #                          'previous_page': page_number - 1,
    #                          'next_page': page_number + 1,
    #                          'page_number': page_number_text,
    #                          })

    response = template.render(context)
    return HttpResponse(response)


def get_related_data(person):
    '''
    Gets all the relations and people that are related to the arguement person as a named tuple
    people_upper: People with a higher hierachy score (e.g. parents)
    people_lower: People with a lower hierachy score (e.g. kids)
    '''
    import collections
    related_data = collections.namedtuple('related_data', ['people_upper','people_lower', 'relations'])

    from django.db.models import Q
    relations = Relation.objects.filter(Q(from_person=person) | Q(to_person=person))

    #Yeah get some raw SQL on!  We are assuming that the 'from' has a higher hierarchy than the 'to'
    people_upper = Person.objects.raw("""   SELECT p.*
                                            FROM family_tree_person p
                                            INNER JOIN family_tree_relation r
                                                ON r.from_person_id = p.id
                                            WHERE r.to_person_id = %s
                                            ORDER BY p.hierarchy_score, gender
                                    """, [person.id])

    people_lower = Person.objects.raw("""   SELECT p.*
                                            FROM family_tree_person p
                                            INNER JOIN family_tree_relation r
                                                ON r.to_person_id = p.id
                                            WHERE r.from_person_id = %s
                                            ORDER BY p.hierarchy_score, gender
                                    """, [person.id])

    return related_data(people_upper, people_lower, relations)



@login_required
def no_match_found(request):
    '''
    Error page if person is not found
    '''

    template = loader.get_template('family_tree/no_match_found.html')

    context = RequestContext(request)
    response = template.render(context)
    return HttpResponse(response)