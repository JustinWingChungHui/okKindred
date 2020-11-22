from django.contrib.auth.signals import user_login_failed
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from axes.handlers.proxy import AxesProxyHandler

from email_confirmation.models import EmailConfirmation
from family_tree.models import Person
from custom_user.models import User

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
        person_id = request.data.get('person_id')

        if not person_id:
            raise ParseError('Invalid person_id')


        person = get_object_or_404(queryset, pk=person_id)

        #ensure user does not already exist
        if person.user_id:
            raise ParseError('User already exists')


        #ensure email exists
        if not person.email:
            raise ParseError('No Email Address')


        #Check a pending invite does not already exist to the email address
        try:
            pending_invite = EmailConfirmation.objects.get(person_id = person_id)
        except:
            pending_invite = None

        if pending_invite and pending_invite.email_address == person.email:
            raise ParseError('There is already a Pending Invite')


        elif pending_invite:
            #Delete pending invite if email has changed
            pending_invite.delete()

        inviteEmail = EmailConfirmation.objects.create(
                        email_address=person.email,
                        person_id=person.id,
                        user_who_invited_person=request.user)

        serializer = InviteEmailSerializer(inviteEmail, context={'request': request})
        return Response(serializer.data)


class InviteEmailConfirmationViewSet(viewsets.ViewSet):

    permission_classes = (AllowAny,)

    def get_invite(self, request, pk):
        #Check ip has not been locked
        if not AxesProxyHandler.is_allowed(request):
            raise PermissionDenied('Requests from this ip addess has been locked for 48 hours')


        # Check confirmation key exists
        try:
            invite = EmailConfirmation.objects.get(confirmation_key=pk)
        except:

            user_login_failed.send(
                                sender=InviteEmailViewSet,
                                credentials={'username': pk },
                                request=request)

            raise PermissionDenied('Invalid invite token')

        return invite

    def retrieve(self, request, pk):
        invite = self.get_invite(request, pk)
        serializer = InviteEmailSerializer(invite, context={'request': request})
        return Response(serializer.data)


    def partial_update(self, request, pk):
        '''
        Handles the confirmation of invite and :
        1. Creates a user correctly
        2. Assigns the user to a person
        3. Deletes the invite
        4. Logs in and displays home page
        '''

        invite = self.get_invite(request, pk)

        password = request.data.get("password")

        # Invalid password should be checked by UI
        if len(password) < 8:
            raise ParseError('Password too short')


        # Do all the checks
        if invite.person.family is None \
            or invite.person.language is None \
            or invite.email_address != invite.person.email \
            or invite.email_address is None:
            raise ParseError('Invalid parameters')


        user = User.objects.create_user(email=invite.email_address, password=password, name=invite.person.name, family_id=invite.person.family_id, language=invite.person.language)
        invite.person.user_id = user.id
        invite.person.save()
        invite.delete()

        serializer = InviteEmailSerializer(invite, context={'request': request})
        return Response(serializer.data)

