from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from family_tree.models import Person
from person_api.serializers import PersonSerializer, PersonListSerializer


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



    def update(self, request, pk=None):
        '''
        Updates a person record
        set fieldName and value
        '''
        queryset = Person.objects.filter(family_id = request.user.family_id)
        person = get_object_or_404(queryset, pk=pk)

        #Make sure we can't change locked profiles
        if person.locked and person.user_id != request.user.id:
            return HttpResponse(status=403, content="Access denied to locked profile")

        field_name = request.data['fieldName']

        if field_name not in [  'email', 'language','locked',
                                'birth_year','year_of_death','telephone_number',
                                'website','address', 'skype_name',
                                'facebook', 'twitter', 'linkedin',
                                'occupation', 'spoken_languages',
                                'name', 'gender', 'biography']:

            return HttpResponse(status=403, content="Access denied to change confirmed user settings")

        #Check we don't change any email or language for a confirmed user
        if person.user_id and field_name in ['email', 'language',]:
            if person.user_id != request.user.id:
                return HttpResponse(status=403, content="Access denied to change confirmed user settings")


        setattr(person, field_name, request.data['value'])
        person.save()
        serializer = PersonSerializer(person)
        return Response(serializer.data)


