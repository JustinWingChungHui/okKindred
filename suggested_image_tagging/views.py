from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from suggested_image_tagging.models import SuggestedTag

from suggested_image_tagging.serializers import SuggestedTagSerializer
from image_tagging_api.serializers import TagSerializer
from message_queue.models import create_message

from common.utils import intTryParse


class SuggestedTagView(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = SuggestedTagSerializer

    def get_queryset(self):
        return SuggestedTag.objects.filter(image__family_id = self.request.user.family_id)


    def list(self, request, *args, **kwargs):
        '''
        Lists suggested tags in users family.
        Use query parameters ?image_id=<id> to filter by image
        '''
        queryset = SuggestedTag.objects.filter(image__family_id = self.request.user.family_id)

        image_id = self.request.query_params.get('image_id', None)

        if image_id is None:
            raise ParseError('Invalid image_id')


        queryset = queryset.filter(image_id=image_id)

        serializer = SuggestedTagSerializer(queryset, many=True)

        return Response(serializer.data)


    def partial_update(self, request, pk=None):
        '''
        Converts suggested tag into a tag
        '''
        queryset = SuggestedTag.objects.filter(image__family_id = self.request.user.family_id)
        suggested_tag = get_object_or_404(queryset, pk=pk)

        person_id, person_id_valid = intTryParse(request.data.get("person_id"))
        if not person_id_valid:
            raise ParseError('Invalid person_id')


        new_tag = suggested_tag.convertToTag(person_id)

        # Send notification email
        new_tag.send_tag_notification_email()

        create_message('tag_converted_process', new_tag.id)

        serializer = TagSerializer(new_tag)
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        '''
        Deletes a suggested tag record
        '''
        queryset = SuggestedTag.objects.filter(image__family_id = self.request.user.family_id)
        suggested_tag = get_object_or_404(queryset, pk=pk)

        suggested_tag.delete()

        return Response('OK')

