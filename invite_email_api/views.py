from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from email_confirmation.models import EmailConfirmation
from family_tree.models import Person

from invite_email_api.serializers import InviteEmailSerializer

class InviteEmailViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        '''
        Gets invite email information sent
        '''

        # Make sure request comes user in same family
        queryset = Person.objects.filter(family_id = request.user.family_id)
        person = get_object_or_404(queryset, pk=pk)

        # Get the invite email data
        inviteEmail = get_object_or_404(EmailConfirmation, person_id = person.id)
        serializer = InviteEmailSerializer(inviteEmail, context={'request': request})
        return Response(serializer.data)

