from family_tree.models import Person,Relation
from family_tree.models.relation import PARTNERED,RAISED, RAISED_BY
from django.db.models import Q
import collections


'''
Service that provides data to populate family tree views
'''

def get_related_data(person):
    '''
    Gets all the relations and people that are related to the arguement person as a named tuple
    people_upper: People with a higher hierachy score (e.g. parents)
    people_lower: People with a lower hierachy score (e.g. kids)
    relations: List of relations
    '''

    #Yeah get some raw SQL on!  I wonder if it would be easier to select all people in a family...
    all_relatives= Person.objects.raw("""   SELECT p.*
                                            FROM family_tree_person p
                                            INNER JOIN family_tree_relation r
                                                ON r.from_person_id = p.id
                                                AND r.to_person_id = {0}
                                            UNION ALL
                                            SELECT p.*
                                            FROM family_tree_person p
                                            INNER JOIN family_tree_relation r
                                                ON r.to_person_id = p.id
                                                AND r.from_person_id = {0}
                                            ORDER BY hierarchy_score, gender;
                                        """.format(person.id))

    people_upper = []
    people_same_level = []
    people_lower = []
    person_ids =[]

    #Separate into above, below and same level
    for relative in all_relatives:

        person_ids.append(relative.id)

        if relative.hierarchy_score < person.hierarchy_score:
            people_upper.append(relative)
        elif relative.hierarchy_score > person.hierarchy_score:
            people_lower.append(relative)
        else:
            people_same_level.append(relative)

    #Get all the relations
    person_ids.append(person.id)
    if len(people_lower) > 2:
        #Reduce number of drawn relations if more than two children
        relations = Relation.objects.filter(Q(from_person_id=person.id) | Q(to_person_id=person.id))
    else:
        relations = Relation.objects.filter(from_person__in=person_ids, to_person__in=person_ids)

    related_data = collections.namedtuple('related_data', ['people_upper', 'people_same_level', 'people_lower', 'relations'])
    return related_data(people_upper, people_same_level, people_lower, relations)



def get_related_path(user_person, to_person):
        '''
        Gets the path from one relative to another
        '''
        relations_by_person = Relation.objects.get_navigable_relations(to_person.family_id)

        visited_person_ids = []
        route = []
        route.append(to_person.id)
        found_route = _search_next_node(relations_by_person, visited_person_ids, route, user_person.id)

        #No path found
        if found_route is None:
            return None, None

        #Get the profiles of the people in the route
        people_path = list(Person.objects.filter(pk__in=found_route))

        #Sort them by the found_route
        people_path.sort(key=lambda p: found_route.index(p.pk))

        return people_path, _get_path_relations(found_route, relations_by_person)


def _get_path_relations(route, relations_by_person):
    '''
    Gets the relation objects associated with the route
    '''

    relations = []

    #Short circuit outahere!
    if len(route) < 2:
        return relations

    for i in range(len(route) - 1):

        j = 0
        from_person_id = route[i]

        while True:
            if relations_by_person[from_person_id][j].to_person_id == route[i + 1]:
                relations.append(relations_by_person[route[i]][j])
                break

            j += 1

            if j > 200:
                raise Exception("Infinite loop")

    return relations


def _search_next_node(paths_by_person, visited_person_ids, route, end_node_id):
    '''
    Searches the next node to see if the end node is conected to it
    Recursive path search
    '''

    #Last element of the list
    start_node_id = route[-1]

    for path in paths_by_person[start_node_id]:
        if not path.to_person_id in visited_person_ids:

            visited_person_ids.append(start_node_id)

            #Success!
            if end_node_id == path.to_person_id:
                route.append(path.to_person_id)
                return route

            #Copy lists http://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list-in-python
            new_route = list(route)
            new_route.append(path.to_person_id)

            #Recursively search next node
            result = _search_next_node(paths_by_person, visited_person_ids, new_route, end_node_id)

            if not result is None:
                return result

    #No route found
    return None


def get_whole_tree(family_id):
    '''
    Gets the whole tree sorted by some magical rules
    1. Hierarchy
    2. Partners
    2. Relation to parent
    '''

    list_of_people_by_hierachy = collections.OrderedDict()
    people_included = {}
    people_by_id = {}

    #Get people by hierarchy
    people = Person.objects.filter(family_id = family_id).order_by("hierarchy_score", "gender")
    for person in people:
        people_by_id[person.id] =  person

    relations = Relation.objects.get_all_relations_for_family_id(family_id)
    relations_by_person = Relation.objects.get_navigable_relations(family_id, relations)

    if people.count() == 0:
        return list_of_people_by_hierachy


    for person in people:

        if person.id not in people_included:
            if person.hierarchy_score not in list_of_people_by_hierachy:
                list_of_people_by_hierachy[person.hierarchy_score] = []

            list_of_people_by_hierachy[person.hierarchy_score].append(person)
            people_included[person.id] = person

            _add_related(person, people_by_id, list_of_people_by_hierachy, people_included, relations_by_person)

    return list_of_people_by_hierachy, relations



def get_descendants(person):
    '''
    Gets the descendants of the person
    '''
    return _get_blood_relations(person, RAISED)


def get_ancestors(person):
    '''
    Gets the ancestors of the person
    '''
    return _get_blood_relations(person, RAISED_BY)


def _get_blood_relations(person, relation_type):
    '''
    Gets the blood relations of a person by setting relation_type to RAISED or RAISED_BY
    RAISED gets descendants, RAISED_BY gets ancestors
    '''

    list_of_people_by_hierachy = collections.OrderedDict()
    people_included = {}
    people_by_id = {}

    #Add this person to the descendants
    list_of_people_by_hierachy[person.hierarchy_score] = [person,]
    people_included[person.id] = person

    #Get all the people in family to navigate through
    people = Person.objects.filter(family_id = person.family_id).order_by("hierarchy_score", "gender")
    for p in people:
        people_by_id[p.id] =  p


    #Get relations to navigate through
    all_relations = Relation.objects.get_all_relations_for_family_id(person.family_id)
    relations_by_person = Relation.objects.get_navigable_relations(person.family_id, all_relations)

    #Recurse through raised
    _add_related(person, people_by_id, list_of_people_by_hierachy, people_included, relations_by_person, relation_types=(relation_type,))

    #Only return relevant relations in the descendants
    relations = []
    for relation in all_relations:
        if relation.from_person_id in people_by_id and relation.to_person_id in people_by_id:
            relations.append(relation)

    return collections.OrderedDict(sorted(list_of_people_by_hierachy.items())), relations



def _add_related(person, people_by_id, list_of_people_by_hierachy, people_included, relations_by_person, relation_types=(PARTNERED, RAISED, RAISED_BY)):
    '''
    Recursively adds people to a sorted tree
    Looks to add in order of relation_types parameter
    '''

    for relation_type in relation_types:

        for path in relations_by_person[person.id]:

            if path.to_person_id not in people_included and path.relation_type == relation_type:

                relation = people_by_id[path.to_person_id]

                if relation.hierarchy_score not in list_of_people_by_hierachy:
                    list_of_people_by_hierachy[relation.hierarchy_score] = []

                list_of_people_by_hierachy[relation.hierarchy_score].append(relation)
                people_included[relation.id] = relation

                _add_related(relation, people_by_id, list_of_people_by_hierachy, people_included, relations_by_person, relation_types)
