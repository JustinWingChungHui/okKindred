from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from custom_user.models import User
from user_api.serializers import UserSerializer


# ViewSets define the view behavior for Django REST
class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
        return Response("Missing parameters", status=status.HTTP_400_BAD_REQUEST)

    if(not request.user.check_password(old_password)):
        return Response("Incorrect previous password", status=status.HTTP_401_UNAUTHORIZED)

    #Invalid password
    if len(new_password) < 8:
        return Response("Password too short", status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(new_password)
    request.user.save()

    return Response("OK")
