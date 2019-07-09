from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from gallery.models import Image
from image_api.serializers import ImageListSerializer, ImageSerializer


class ImageListView(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Image.objects.filter(family_id = self.request.user.family_id).order_by('creation_date')[:20]

    def list(self, request):
        '''
        Lists images in users family.
        Use query parameters ?gallery_id=<id> to filter by gallery or
        ?person_id=<id> to filter by tagged people
        '''
        queryset = Image.objects.filter(family_id = self.request.user.family_id).order_by('creation_date')

        gallery_id = self.request.query_params.get('gallery_id', None)
        if gallery_id is not None:
            queryset = queryset.filter(gallery_id=gallery_id).order_by('creation_date')

        person_id = self.request.query_params.get('person_id', None)
        if person_id is not None:
            queryset= Image.objects.filter(tag__person_id = person_id).order_by('creation_date')

        page = self.paginate_queryset(queryset)
        # page = self.paginate_queryset(queryset)
        serializer = ImageListSerializer(page, many=True)

        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)



    def retrieve(self, request, pk=None):
        '''
        Gets a single image record
        '''
        queryset = Image.objects.filter(family_id = request.user.family_id)
        person = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(person)
        return Response(serializer.data)