# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person, Relation
from django.http import Http404
from family_tree.models.relation import PARTNERED, RAISED, RAISED_BY
from family_tree.models.person import MALE, FEMALE, OTHER
from family_tree.decorators import same_family_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.db.models import Q
from custom_user.decorators import set_language

@login_required
@set_language
@same_family_required
def add_relation_view(request, person_id = 0, person = None):
    '''
    Shows the view for adding a relation
    '''

    template = loader.get_template('family_tree/add_relation.html')

    context = RequestContext(request,{
                                'person' : person,
                                'languages' : settings.LANGUAGES,
                            })

    response = template.render(context)
    return HttpResponse(response)


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

        language =  request.POST.get("language")
        #http://stackoverflow.com/a/2917399/1245362
        if language not in [x[0] for x in settings.LANGUAGES]:
            raise Http404

        gender = request.POST.get("gender")
        if gender not in (MALE, FEMALE, OTHER):
            raise Http404

        new_person = Person(name=new_name, gender=gender,language=language,family_id=person.family_id)
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

    return HttpResponseRedirect('/person={0}/'.format(person_id))


@login_required
@set_language
@same_family_required
def break_relation_view(request, person_id = 0, person = None):
    '''
    Shows the view to break relations
    '''
    relations = Relation.objects.filter(Q(from_person_id = person_id) | Q(to_person_id = person_id))

    template = loader.get_template('family_tree/break_relation.html')

    context = RequestContext(request,{
                                'person': person,
                                'relations' : relations,
                            })

    response = template.render(context)
    return HttpResponse(response)


@login_required
@set_language
@same_family_required
def break_relation_post(request, person_id = 0, person = None):
    '''
    Deletes a relation
    '''

    relation_id = int(request.POST.get("relation_id"))

    Relation.objects.filter(id=relation_id).delete()

    return HttpResponseRedirect('/break_relation={0}/'.format(person_id))
