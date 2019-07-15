from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from custom_user.models import User
from user_api.serializers import UserSerializer


# ViewSets define the view behavior for Django REST
class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user



