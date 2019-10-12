from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from common.utils import intTryParse, create_hash
from family_tree.models import Person
from message_queue.models import create_message

from person_api.serializers import PersonListSerializer

MAX_FILE_SIZE = 15000000  # bytes

# ViewSets define the view behavior for Django REST
class ProfileImageSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    def update(self, request, pk=None):

        queryset = Person.objects.filter(family_id = request.user.family_id)
        person = get_object_or_404(queryset, pk=pk)

        #Make sure we can't change locked profiles
        if person.locked and person.user_id != request.user.id:
            return HttpResponse(status=403, content="Access denied to locked profile")

        x, x_valid = intTryParse(request.data.get("x"))
        y, y_valid = intTryParse(request.data.get("y"))
        w, w_valid = intTryParse(request.data.get("w"))
        h, h_valid = intTryParse(request.data.get("h"))
        r, r_valid = intTryParse(request.data.get("r"))

        if not (x_valid and y_valid and w_valid and h_valid and r_valid):
            return HttpResponse(status=400, content='Invalid crop parameters')


        try:
            uploaded = request.FILES['picture']

            if uploaded.size > MAX_FILE_SIZE:
                raise ValueError('File is too big')

            filename =  create_hash(person.name) +'.jpg'
            photo_file = ''.join([settings.MEDIA_ROOT, 'profile_photos/', filename])

            #Write the file to the destination
            destination = open(photo_file, 'wb+')


            for chunk in uploaded.chunks():
                destination.write(chunk)
            destination.close()

            person.set_profile_image_crop_rotate_resize(photo_file, x, y, w, h, r)
            person.save()

        except Exception as e:
            return HttpResponse(status=400, content=str(e))

        create_message('profile_photo_process', person.id)

        serializer = PersonListSerializer(person)
        return Response(serializer.data)







