# encoding: utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from family_tree.models import Person, Relation
from family_tree.models.person import ORPHANED_HIERARCHY_SCORE
from family_tree.models.person import MALE, FEMALE, OTHER, NON_BINARY, PREFER_NOT_TO_SAY
from family_tree.models.relation import PARTNERED, RAISED, RAISED_BY
from family_tree.decorators import same_family_required
from family_tree.services import relation_suggestion_service

from common.utils import intTryParse

from custom_user.decorators import set_language

@login_required
@set_language
@same_family_required
def add_relation_view(request, person_id = 0, person = None):
    '''
    Shows the view for adding a relation
    '''
    suggested_relation, suggested_person = relation_suggestion_service.get_first_relation_suggestion(person)

    return render(request, 'family_tree/add_relation.html', {
                                'person' : person,
                                'languages' : settings.LANGUAGES,
                                'suggested_relation' : suggested_relation,
                                'suggested_person' : suggested_person,
                            })


@login_required
@set_language
@same_family_required
def add_relation_post(request, person_id = 0, person = None):
    '''
    Receives post information for a new relation
    '''
    relation_type = int(request.POST.get("relation_type"))
    if relation_type not in ( PARTNERED, RAISED, RAISED_BY):
        raise Http404

    #If person does not exist, create a new person
    existing_person = int(request.POST.get("existing_person"))
    if not existing_person:

        new_name = request.POST.get("name").strip()
        if len(new_name) == 0:
            raise Http404

        language = request.POST.get("language")
        #http://stackoverflow.com/a/2917399/1245362
        if language not in [x[0] for x in settings.LANGUAGES]:
            raise Http404

        gender = request.POST.get("gender")
        if gender not in (MALE, FEMALE, OTHER, NON_BINARY, PREFER_NOT_TO_SAY):
            raise Http404

        birth_year, birth_year_valid = intTryParse(request.POST.get("birth_year"))
        if not birth_year_valid:
            birth_year = 0

        new_person = Person(name=new_name, gender=gender,language=language,family_id=person.family_id, birth_year=birth_year)

        address = request.POST.get("address")
        if address:
            new_person.address = address


        if relation_type == PARTNERED:
            new_person.hierarchy_score = person.hierarchy_score
        elif relation_type == RAISED:
            new_person.hierarchy_score = person.hierarchy_score + 1
        elif relation_type == RAISED_BY:
            new_person.hierarchy_score = person.hierarchy_score - 1
        new_person.save()

        relation_id = new_person.id

    else: #Existing person
        relation_id = int(request.POST.get("relation_id"))

    new_relation = Relation(from_person_id=person.id, to_person_id=relation_id, relation_type=relation_type)
    new_relation.save()

    reevaluate_hierarchy_scores_of_orphans(request.user.family_id)

    return HttpResponseRedirect('/tree/{0}/'.format(person_id))


def reevaluate_hierarchy_scores_of_orphans(family_id):
    '''
    Loads all relations that have a hierarchy score of -1 and tries to resolve them
    '''
    for person in list(Person.objects.filter(family_id=family_id, hierarchy_score=ORPHANED_HIERARCHY_SCORE)):

        for relation in list(Relation.objects.filter(from_person_id = person.id)):
            if relation.to_person.hierarchy_score != ORPHANED_HIERARCHY_SCORE:
                if relation.relation_type == PARTNERED:
                    person.hierarchy_score = relation.to_person.hierarchy_score
                elif relation.relation_type == RAISED:
                    person.hierarchy_score = relation.to_person.hierarchy_score - 1

                person.save()
                return

        for relation in list(Relation.objects.filter(to_person_id = person.id)):
            if relation.from_person.hierarchy_score != ORPHANED_HIERARCHY_SCORE:
                if relation.relation_type == PARTNERED:
                    person.hierarchy_score = relation.from_person.hierarchy_score
                elif relation.relation_type == RAISED:
                    person.hierarchy_score = relation.from_person.hierarchy_score + 1

                person.save()
                return


@login_required
@set_language
@same_family_required
def break_relation_view(request, person_id = 0, person = None):
    '''
    Shows the view to break relations
    '''
    relations = Relation.objects.filter(Q(from_person_id = person_id) | Q(to_person_id = person_id))

    return render(request, 'family_tree/break_relation.html', {
                                'person': person,
                                'relations' : relations,
                            })

@login_required
@set_language
@same_family_required
def break_relation_post(request, person_id = 0, person = None):
    '''
    Deletes a relation
    '''

    relation_id = int(request.POST.get("relation_id"))

    relation = Relation.objects.get(id=relation_id)

    from_person_id = relation.from_person_id
    to_person_id = relation.to_person_id

    relation.delete()

    reassign_hierarchy_score(from_person_id)
    reassign_hierarchy_score(to_person_id)

    return HttpResponseRedirect('/break_relation={0}/'.format(person_id))


def reassign_hierarchy_score(person_id):
    '''
    Checks if the person has any relations and reassigns hierarchy score if not
    '''

    relation_count =  Relation.objects.filter(Q(from_person_id=person_id) | Q(to_person_id=person_id)).count()
    if relation_count == 0:
        person = Person.objects.get(id=person_id)

        # Do not reassign if last person
        if Person.objects.all().count() > 1:
            person.hierarchy_score = ORPHANED_HIERARCHY_SCORE
            person.save()
