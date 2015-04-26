from family_tree.models import Relation
from family_tree.models.relation import PARTNERED, RAISED, RAISED_BY
import random

def get_first_relation_suggestion(person):
    '''
    Gets a relation person suggestion to be related
    '''
    suggestions = get_relation_suggestions(person)

    if len(suggestions) == 0:
        return None, None

    # Randomize so doesn't always suggest same relation
    random.shuffle(suggestions)

    return suggestions[0], suggestions[0].to_person


def get_relation_suggestions(person):
    '''
    Gets relation suggestions when creating new relationships
    '''
    suggestions = []

    relations_by_person = Relation.objects.get_navigable_relations(person.family_id)

    for first_relation in relations_by_person[person.id]:

        #Suggest all children of partner
        if first_relation.relation_type == PARTNERED:
            suggestions.extend(_get_unrelated_childred_of_partner(person.id, first_relation.to_person_id, relations_by_person))

        #Suggest all parents of child
        if first_relation.relation_type == RAISED:
            suggestions.extend(_get_unrelated_parents_of_child(person.id, first_relation.to_person_id, relations_by_person))

        #Suggest all partners of parent
        if first_relation.relation_type == RAISED_BY:
            suggestions.extend(_get_unrelated_partners_of_parent(person.id, first_relation.to_person_id, relations_by_person))

    return suggestions



def _is_related(person1_id, person2_id, relations_by_person):
    '''
    returns whether the two people are already related
    '''
    for relation in relations_by_person[person1_id]:
        if relation.to_person_id == person2_id:
            return True

    return False



def _get_unrelated_childred_of_partner(person_id, partner_id, relations_by_person):
    '''
    Gets all the unrelated children of partner
    '''
    suggestions = []

    for second_relation in relations_by_person[partner_id]:

        if  second_relation.relation_type == RAISED and \
            not _is_related(person_id, second_relation.to_person_id, relations_by_person) and \
            second_relation.to_person_id != person_id:

            relation = Relation(from_person_id = person_id, to_person_id = second_relation.to_person_id, relation_type = RAISED)

            suggestions.append(relation)

    return suggestions


def _get_unrelated_parents_of_child(person_id, child_id, relations_by_person):
    '''
    Gets all the unrelated parents of child
    '''
    suggestions = []

    for second_relation in relations_by_person[child_id]:

        if  second_relation.relation_type == RAISED_BY and \
            not _is_related(person_id, second_relation.to_person_id, relations_by_person) and \
            second_relation.to_person_id != person_id:

            relation = Relation(from_person_id = person_id, to_person_id = second_relation.to_person_id, relation_type = PARTNERED)

            suggestions.append(relation)

    return suggestions



def _get_unrelated_partners_of_parent(person_id, parent_id, relations_by_person):
    '''
    Gets all the unrelated partners of parents
    '''
    suggestions = []

    for second_relation in relations_by_person[parent_id]:

        if  second_relation.relation_type == PARTNERED and \
            not _is_related(person_id, second_relation.to_person_id, relations_by_person) and \
            second_relation.to_person_id != person_id:

            relation = Relation(from_person_id = person_id, to_person_id = second_relation.to_person_id, relation_type = RAISED_BY)

            suggestions.append(relation)

    return suggestions