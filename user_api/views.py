from django_rest_passwordreset.signals import post_password_reset

from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from custom_user.models import User
from family_tree.models import Family, Person
from user_api.serializers import UserSerializer, UserDetailSerializer


class UserList(generics.ListAPIView):

    # There most likely won't be many users in a family tree
    pagination_class = None

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(family_id = self.request.user.family_id
            ).order_by('name')


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def password_change(request):
    """
    API to change passwords.  Requires POST data:
    old_password
    new_password
    The new password must be 8 characters or longer
    """

    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if (not old_password or not new_password):
        raise ParseError('Missing parameters')


    if(not request.user.check_password(old_password)):
        raise PermissionDenied('Incorrect previous password')

    #Invalid password
    if len(new_password) < 8:
        raise ParseError('Password too short')

    request.user.set_password(new_password)
    request.user.save()

    post_password_reset.send(sender="password_change", user=request.user)

    return Response("OK")



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_account(request):
    """
    API to delete account when not last user in family
    Can choose to leave profile or remove profile
    """

    password = request.data.get('password')

    if(not password or not request.user.check_password(password)):
        raise PermissionDenied('Incorrect previous password')

    user_count = User.objects.filter(family_id = request.user.family_id).count()

    # Last user, delete everything
    if user_count == 1:
        person = Person.objects.get(user_id=request.user.id)
        person.delete()

        family = Family.objects.get(id = request.user.family_id)
        family.delete()


    else:
        delete_profile = request.data.get('delete_profile')

        #Delete the profile
        person = Person.objects.get(user_id=request.user.id)

        if delete_profile:
            person.delete()
        else:
            person.user_id = None
            person.email_address = None
            person.save()

        #Delete the user
        request.user.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


