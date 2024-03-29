from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import Http404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from axes.handlers.proxy import AxesProxyHandler
from django.contrib.auth.signals import user_login_failed

from custom_user.models import User
from family_tree.models import Person
from family_tree.models.person import MALE, FEMALE, OTHER, NON_BINARY, PREFER_NOT_TO_SAY
from sign_up.models import SignUp

from common.utils import intTryParse

from user_api.serializers import UserSerializer
from sign_up_api.serializers import SignUpSerializer


class SignUpViewSet(viewsets.ViewSet):

    permission_classes = (AllowAny,)

    def create(self, request):
        '''
        Handles when a sign up is submitted
        '''

        #Check ip has not been locked
        if not AxesProxyHandler.is_allowed(request):
            raise Http404

        name = request.data.get("name")
        email = request.data.get("email")
        gender = request.data.get("gender")
        language = request.data.get("language")
        ip_address = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')

        if not (name and email and gender and language):
            raise ParseError('Invalid name, email, gender, language')


        if gender not in (MALE, FEMALE, OTHER, NON_BINARY, PREFER_NOT_TO_SAY):
            raise ParseError('Invalid gender')


        name = name.strip()
        email = email.strip().lower()

        # assign non required stuff
        birth_year, birth_year_valid = intTryParse(request.data.get("birth_year"))
        if not birth_year_valid:
            birth_year = 0

        address = request.data.get("address")
        if not address:
            address = ""

        try:
            validate_email(email)
        except ValidationError:
            # return invalid email template
            raise ParseError('Invalid Email')


        #Check email is not being used
        if is_email_in_use(email):
            raise ParseError('Email in Use')


        new_signup = SignUp.objects.create(
                    name = name,
                    email_address = email,
                    gender = gender,
                    language = language,
                    address = address,
                    birth_year = birth_year,
                    ip_address = ip_address)

        serializer = SignUpSerializer(new_signup)
        return Response(serializer.data)


    def update(self, request, pk=None):
        '''
        Handles the sign up confirmation
        '''

        #Check ip has not been locked
        if not AxesProxyHandler.is_allowed(request):
            raise Http404

        try:
            sign_up = SignUp.objects.get(confirmation_key=pk)
        except:

            user_login_failed.send(
                                sender=SignUpViewSet,
                                credentials={'username': pk },
                                request=request)
            raise Http404


        password = request.data.get("password")

        #Invalid password should be checked bu UI
        if len(password) < 8:
            raise ParseError('Password too Short')


        user = sign_up.complete_registration(password)

        serializer = UserSerializer(user)
        return Response(serializer.data)



def is_email_in_use(email):
    '''
    Checks if email is in use
    '''
    if User.objects.filter(email = email).count():
        return True

    if Person.objects.filter(email = email).count():
        return True

    if SignUp.objects.filter(email_address = email).count():
        return True

    return False





