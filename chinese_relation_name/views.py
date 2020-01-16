from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import json

from chinese_relation_name.relation_name_dictionary import relation_names, RelationNameEncoder

# Public
@api_view(['GET'])
@permission_classes((AllowAny,))
def family_member_names(request):

    key = request.GET.get('name', None)
    if key in relation_names:
        result = relation_names[key]
    else:
        result = relation_names

    response = JsonResponse(result, encoder=RelationNameEncoder)

    return response