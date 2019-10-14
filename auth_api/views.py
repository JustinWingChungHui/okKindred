from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from auth_api import serializers


from axes.models import AccessAttempt

class AppTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    Also returns language of logged in user
    """
    serializer_class = serializers.AppTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
def is_locked(request):

    ip_address = request.META.get('HTTP_X_REAL_IP')

    try:
        accessAttempt = AccessAttempt.objects.get(ip_address = ip_address)

        locked = accessAttempt.failures_since_start >= settings.AXES_LOGIN_FAILURE_LIMIT
        return Response(locked)
    except:
        return Response(False)

