from django.http import HttpResponse
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
        Gets any pending invite email information for a person id
        '''

        # Make sure request comes user in same family
        queryset = Person.objects.filter(family_id = request.user.family_id)
        person = get_object_or_404(queryset, pk=pk)

        # Get the invite email data
        inviteEmail = get_object_or_404(EmailConfirmation, person_id = person.id)
        serializer = InviteEmailSerializer(inviteEmail, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        '''
        Creates email invite
        '''
        # Make sure request comes user in same family
        queryset = Person.objects.filter(family_id = request.user.family_id)
        person_id = self.request.data.get('person_id')

        if not person_id:
            return HttpResponse(status=400, content="Invalid person_id")

        person = get_object_or_404(queryset, pk=person_id)

        #ensure user does not already exist
        if person.user_id:
            return HttpResponse(status=400, content="User already exists")

        #ensure email exists
        if not person.email:
            return HttpResponse(status=400, content="No Email Address")

        #Check a pending invite does not already exist to the email address
        try:
            pending_invite = EmailConfirmation.objects.get(person_id = person_id)
        except:
            pending_invite = None

        if pending_invite and pending_invite.email_address == person.email:
            return HttpResponse(status=400, content="There is already a Pending Invite")

        elif pending_invite:
            #Delete pending invite if email has changed
            pending_invite.delete()

        inviteEmail = EmailConfirmation.objects.create(
                        email_address=person.email,
                        person_id=person.id,
                        user_who_invited_person=request.user)

        serializer = InviteEmailSerializer(inviteEmail, context={'request': request})
        return Response(serializer.data)

