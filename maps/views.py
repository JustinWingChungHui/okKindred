# encoding: utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from family_tree.decorators import same_family_required
from custom_user.decorators import set_language
from maps import map_service
import json

@login_required
@set_language
@same_family_required
def map(request, person_id = 0, person = None):
    '''
    View to show open map
    '''
    return render(request, 'maps/map.html', {
                                    'latitude' : person.latitude,
                                    'longitude' : person.longitude,
                                    'zoom' : 12 if person_id != 0 else 7,
                                    'token' : settings.MAP_BOX_TOKEN,
                                })


@login_required
@set_language
def map_points(request, division_size):
    '''
    API to get person location data
    '''
    data = map_service.get_person_location_points(request.user.family_id, float(division_size))
    return HttpResponse(json.dumps(data), content_type="application/json")

