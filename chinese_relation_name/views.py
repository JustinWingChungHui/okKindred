from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from family_tree.models.relation import RAISED, PARTNERED, RAISED_BY

from chinese_relation_name.relation_name_dictionary import get_relation_names, relation_names, RelationNameEncoder
from chinese_relation_name.solver import Solver
from chinese_relation_name.node import Node
from chinese_relation_name.path import Path, PathStep
from chinese_relation_name.path_to_name_mapper import get_name

import json

relations_by_name = {
    'raised': RAISED,
    'partnered': PARTNERED,
    'raised_by': RAISED_BY
}

# Public
@api_view(['GET'])
@permission_classes((AllowAny,))
def family_member_names(request):
    '''
    Public endpoint to get a list of family member names
    '''
    key = request.GET.get('name', None)
    if key:
        result = get_relation_names([key])
    else:
        result = relation_names

    response = JsonResponse(result, encoder=RelationNameEncoder, safe=False)

    return response



@api_view(['POST'])
@permission_classes((AllowAny,))
def solve_relation_name(request):
    '''
    Public endpoint to get a relation name between family members
    '''
    data = json.loads(request.body)

    path = Path()

    last_node = None
    for point in data:
        node = Node(point)
        if last_node:
            step = PathStep(last_node, node, relations_by_name[point.relation_type])
            path.steps.append(step)

        last_node = node

    path.set_success_properties()
    names = get_name(path)

    results = get_relation_names(names)

    response = JsonResponse(results, encoder=RelationNameEncoder, safe=False)

    return response




@api_view(['GET'])
def relation_name(request, from_person_id, to_person_id):
    '''
    Endpoint for logged in users to interogate relation between family members
    '''
    if not from_person_id or not to_person_id:
        return HttpResponse(status=400, content='from_person_id and to_person_id need to be defined')

    solver = Solver()
    names = solver.solve(request.user.family_id, from_person_id, to_person_id)

    results = get_relation_names(names)


    response = JsonResponse(results, encoder=RelationNameEncoder, safe=False)

    return response





