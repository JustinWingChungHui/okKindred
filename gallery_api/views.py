from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from gallery.models import Gallery
from gallery_api.serializers import GallerySerializer


class GalleryView(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = GallerySerializer

    def get_queryset(self):
        return Gallery.objects.filter(family_id = self.request.user.family_id).order_by('last_updated_date')[:20]

    def list(self, request):
        '''
        Lists galleries in users family.
        '''
        queryset = Gallery.objects.filter(family_id = self.request.user.family_id).order_by('last_updated_date')

        page = self.paginate_queryset(queryset)

        serializer = GallerySerializer(page, many=True)

        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)



    def retrieve(self, request, pk=None):
        '''
        Gets a single Gallery record
        '''
        queryset = Gallery.objects.filter(family_id = request.user.family_id)
        gallery = get_object_or_404(queryset, pk=pk)
        serializer = GallerySerializer(gallery)
        return Response(serializer.data)