from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common.geocoder import geocode_address



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def geocode_addess(request):

    address = request.GET.get('address', None)

    if not address:
        return Response('Missing address parameter', status=status.HTTP_400_BAD_REQUEST)

    location = geocode_address(address)

    result = {
        'latitude': location.latitude,
        'longitude': location.longitude
    }
    response = Response(result, status=status.HTTP_200_OK)

    return response