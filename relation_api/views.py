from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from family_tree.models import Relation, Person
from family_tree.models.person import ORPHANED_HIERARCHY_SCORE
from family_tree.models.relation import PARTNERED, RAISED, RAISED_BY
from relation_api.serializers import RelationSerializer
from common.utils import intTryParse


# ViewSets define the view behavior for Django REST
class RelationViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        '''
        Lists all relations between people in user's family
        '''
        queryset = Relation.objects.filter(from_person__family_id = request.user.family_id)

        serializer = RelationSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        '''
        Gets a single relation record
        '''
        queryset = Relation.objects.filter(from_person__family_id = request.user.family_id)
        rel = get_object_or_404(queryset, pk=pk)
        serializer = RelationSerializer(rel, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        queryset = Relation.objects.filter(from_person__family_id = request.user.family_id)
        relation = get_object_or_404(queryset, pk=pk)
        relation.delete()

        return Response('OK')


    def create(self, request):
        '''
        Creates a relation record
        '''
        from_person_id, from_person_id_valid  = intTryParse(request.data.get('from_person_id'))
        to_person_id, to_person_id_valid  = intTryParse(request.data.get('to_person_id'))
        relation_type, relation_type_valid  = intTryParse(request.data.get('relation_type'))

        if not (from_person_id_valid and to_person_id_valid and relation_type_valid):
            raise Http404

        if relation_type not in (PARTNERED, RAISED, RAISED_BY):
            raise Http404

        # Ensure people exist
        person_queryset = Person.objects.filter(family_id = request.user.family_id)
        from_person = get_object_or_404(person_queryset, pk=from_person_id)
        to_person = get_object_or_404(person_queryset, pk=to_person_id)

        relation = create_relation(from_person, to_person, relation_type)

        if not relation:
            raise Http404

        serializer = RelationSerializer(relation, context={'request': request})
        return Response(serializer.data)



def create_relation(user, from_person, to_person, relation_type):

    if user.family_id != from_person.family_id or user.family_id != to_person.family_id:
        return None

    relation = Relation(from_person_id=from_person.id, to_person_id=to_person.id, relation_type=relation_type)
    relation.save()

    reevaluate_hierarchy_scores_of_orphans(user.family_id)

    return relation


def reevaluate_hierarchy_scores_of_orphans(family_id):
    '''
    Loads all relations that have a hierarchy score of -1 and tries to resolve them
    Hierarchy scores will eventually be deprecated
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

