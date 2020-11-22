from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from family_tree.models import Person
from gallery.models import Tag, Image
from message_queue.models import create_message
from image_tagging_api.serializers import TagSerializer

from common.utils import intTryParse, floatTryParse


class TagView(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(person__family_id = self.request.user.family_id)


    def list(self, request, *args, **kwargs):
        '''
        Lists tags in users family.
        Use query parameters ?image_id=<id> to filter by image
        ?person_id=<id> to filter by tagged person
        '''
        queryset = Tag.objects.filter(person__family_id = self.request.user.family_id)

        image_id = self.request.query_params.get('image_id', None)

        if image_id is None:
            raise ParseError('Invalid image_id')


        queryset = queryset.filter(image_id=image_id)

        person_id = self.request.query_params.get('person_id', None)
        if person_id is not None:
            queryset= queryset.filter(person_id = person_id)

        serializer = TagSerializer(queryset, many=True)

        return Response(serializer.data)



    def destroy(self, request, pk=None):
        '''
        deletes a single tag
        '''
        queryset = Tag.objects.filter(person__family_id = request.user.family_id)
        tag = get_object_or_404(queryset, pk=pk)
        tag.delete()

        return Response('OK')


    def create(self, request):
        '''
        Creates a tag
        '''

        person_id, person_id_valid = intTryParse(request.data.get("person_id"))
        if not person_id_valid:
            raise ParseError('Invalid person_id')


        person_queryset = Person.objects.filter(family_id = self.request.user.family_id)
        person = get_object_or_404(person_queryset, pk=person_id)

        image_id, image_id_valid = intTryParse(request.data.get("image_id"))
        if not image_id_valid:
            raise ParseError('Invalid image_id')


        image_queryset = Image.objects.filter(family_id = self.request.user.family_id)
        image = get_object_or_404(image_queryset, pk=image_id)

        x1, x1_valid = floatTryParse(request.data.get("x1"))
        x2, x2_valid = floatTryParse(request.data.get("x2"))
        y1, y1_valid = floatTryParse(request.data.get("y1"))
        y2, y2_valid = floatTryParse(request.data.get("y2"))

        if not (x1_valid and x2_valid and y1_valid and y2_valid):
            raise ParseError('Invalid x1, x2, y1, or y2')


        tag = Tag.objects.create(image_id=image.id, x1=x1, y1=y1, x2=x2, y2=y2, person_id=person.id)

        create_message('resize_tag', tag.id)

        # Send notification email
        tag.send_tag_notification_email()

        serializer = TagSerializer(tag, many=False)
        return Response(serializer.data)



