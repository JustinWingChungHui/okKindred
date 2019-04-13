from rest_framework_simplejwt.views import TokenObtainPairView
from auth_api import serializers

class AppTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    Also returns language of logged in user
    """
    serializer_class = serializers.AppTokenObtainPairSerializer

