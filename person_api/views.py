# Create your views here.
from django.shortcuts import get_object_or_404
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
        Lists all people in user's family
        '''
        queryset = Person.objects.filter(family_id = request.user.family_id
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