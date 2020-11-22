import json
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from family_tree.models import Person
from family_tree.models.person import MALE, FEMALE, OTHER, NON_BINARY, PREFER_NOT_TO_SAY
from family_tree.models.relation import PARTNERED, RAISED, RAISED_BY
from person_api.serializers import PersonSerializer, PersonListSerializer
from relation_api.views import create_relation
from relation_api.serializers import RelationSerializer
from message_queue.models import create_message

from common.utils import intTryParse
import reversion

# ViewSets define the view behavior for Django REST
class PersonViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        '''
        Lists all people in user's family use ?search= parameter to find people by name
        '''
        queryset = Person.objects.filter(family_id = request.user.family_id
                        ).order_by('hierarchy_score', 'birth_year', 'gender')

        search_term = self.request.query_params.get('search', None)
        if search_term is not None:
            queryset = queryset.filter(name__icontains=search_term
                        ).order_by('hierarchy_score', 'birth_year', 'gender')

        serializer = PersonListSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        '''
        Gets a single person record
        '''
        queryset = Person.objects.filter(family_id = request.user.family_id)
        person = get_object_or_404(queryset, pk=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)



    def partial_update(self, request, pk=None):
        '''
        Updates a person record
        set fieldName and value
        '''
        queryset = Person.objects.filter(family_id = request.user.family_id)

        with reversion.create_revision():
            person = get_object_or_404(queryset, pk=pk)

            #Make sure we can't change locked profiles
            if person.locked and person.user_id != request.user.id:
                raise PermissionDenied('Access denied to locked profile')

            field_name = request.data.get('fieldName')

            if not field_name or field_name not in ['email', 'language','locked',
                                    'birth_year','year_of_death','telephone_number',
                                    'website','address', 'skype_name',
                                    'facebook', 'twitter', 'linkedin',
                                    'occupation', 'spoken_languages',
                                    'name', 'gender', 'biography']:

                raise PermissionDenied('Access denied to change confirmed user settings')


            #Check we don't change any email or language for a confirmed user
            if person.user_id:
                if person.user_id != request.user.id:
                    if field_name in ['email', 'language', 'locked']:
                        raise PermissionDenied('Access denied to change confirmed user settings')


            else:
                # profile is not a user
                if field_name == 'locked':
                    raise PermissionDenied('Access denied to change confirmed user settings')


            setattr(person, field_name, request.data.get('value'))
            person.save()

            # Store some meta-information.
            reversion.set_user(request.user)
            reversion.set_comment('Update ' + request.META.get('HTTP_X_REAL_IP'))

            serializer = PersonSerializer(person)
            return Response(serializer.data)


    def destroy(self, request, pk=None):
        '''
        Deletes a person record if not associated with a user
        '''
        queryset = Person.objects.filter(family_id = request.user.family_id)

        with reversion.create_revision():
            person = get_object_or_404(queryset, pk=pk)

            if person.user_id:
                raise PermissionDenied('Profile is a user and cannot be deleted')

            person.delete()

            # Store some meta-information.
            reversion.set_user(request.user)
            reversion.set_comment('Delete ' + request.META.get('HTTP_X_REAL_IP'))

            message = {
                'family_id': request.user.family_id,
                'person_id': int(pk)
            }

            message_encoded = json.dumps(message)

            create_message('person_deleted_update_face_model', message_encoded)

            return Response(status=status.HTTP_204_NO_CONTENT)


    def create(self, request):
        '''
        Creates a new person record and links it to another person
        needs from_person_id, relation_type, name, gender, birth_year and address
        '''

        queryset = Person.objects.filter(family_id = request.user.family_id)

        from_person_id, from_person_id_valid = intTryParse(request.data.get("from_person_id"))
        if not from_person_id_valid:
            raise ParseError('Invalid from_person_id')


        from_person = get_object_or_404(queryset, pk=from_person_id)

        relation_type, relation_type_valid = intTryParse(request.data.get("relation_type"))
        if not relation_type_valid or relation_type not in (PARTNERED, RAISED, RAISED_BY):
            raise ParseError('Invalid relation_type')


        name = request.data.get("name")
        if not name or len(name.strip()) == 0:
            raise ParseError('Invalid name')


        gender = request.data.get("gender")
        if gender not in (MALE, FEMALE, OTHER, NON_BINARY, PREFER_NOT_TO_SAY):
            raise ParseError('Invalid gender')


        birth_year, birth_year_valid = intTryParse(request.POST.get("birth_year"))
        if not birth_year_valid:
            birth_year = 0

        with reversion.create_revision():
            new_person = Person(name=name.strip(), gender=gender, family_id=from_person.family_id, birth_year=birth_year)

            address = request.data.get("address")
            if address:
                new_person.address = address

            # Hierarchy scores will eventually be deprecated
            if relation_type == PARTNERED:
                new_person.hierarchy_score = from_person.hierarchy_score
            elif relation_type == RAISED:
                new_person.hierarchy_score = from_person.hierarchy_score + 1
            elif relation_type == RAISED_BY:
                new_person.hierarchy_score = from_person.hierarchy_score - 1
            new_person.save()

            # Store some meta-information.
            reversion.set_user(request.user)
            reversion.set_comment('Create ' + request.META.get('HTTP_X_REAL_IP'))

            relation = create_relation(request.user, from_person, new_person, relation_type)
            relation_serializer = RelationSerializer(relation)

            person_serializer = PersonSerializer(new_person)
            return Response({'person': person_serializer.data, 'relation': relation_serializer.data})


