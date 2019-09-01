from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from common.utils import create_hash, intTryParse
from gallery.models import Image, Gallery
from gallery.models.image import upload_to
from image_api.serializers import ImageSerializer

import os
import PIL

MAX_FILE_SIZE = 15000000  # bytes

class ImageListView(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer

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
        serializer = ImageSerializer(page, many=True)

        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)



    def retrieve(self, request, pk=None):
        '''
        Gets a single image record
        '''
        queryset = Image.objects.filter(family_id = request.user.family_id)
        image = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    def create(self, request):
        '''
        Image upload
        '''
        queryset = Gallery.objects.filter(family_id = request.user.family_id)
        gallery_id, gallery_id_valid = intTryParse(request.data.get("gallery_id"))

        if not gallery_id_valid:
            return HttpResponse(status=400, content='Invalid gallery_id')

        # Check gallery is part of family
        gallery = get_object_or_404(queryset, pk=gallery_id)

        try:
            uploaded = request.FILES['picture']
            name, ext = os.path.splitext(uploaded.name)

            if uploaded.size > MAX_FILE_SIZE:
                return HttpResponse(status=400, content='File too big')

            filename =  create_hash(uploaded.name) +'.jpg'
            image = Image(gallery_id=gallery.id, family_id=gallery.family_id, title=name)

            path = upload_to(image, filename)

            #Write the file to the destination
            destination = open(os.path.join(settings.MEDIA_ROOT, path), 'wb+')

            for chunk in uploaded.chunks():
                destination.write(chunk)
            destination.close()

            image.original_image = path
            PIL.Image.open(os.path.join(settings.MEDIA_ROOT, str(image.original_image))).verify()
            image.save()

            image.upload_files_to_s3()
            image.delete_local_image_files()

            serializer = ImageSerializer(image)
            return Response(serializer.data)

        except Exception as e:


            if image:
                image.delete_local_image_files()
                image.delete()

            return HttpResponse(status=400, content=str(e))


    def destroy(self, request, pk=None):
        '''
        Gets a single image record
        '''
        queryset = Image.objects.filter(family_id = request.user.family_id)
        image = get_object_or_404(queryset, pk=pk)
        image.delete_local_image_files()
        image.delete_remote_image_files()
        image.delete()

        return Response('OK')