# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from family_tree.models import Relation
from relation_api.serializers import RelationSerializer


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