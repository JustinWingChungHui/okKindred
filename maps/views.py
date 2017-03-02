# encoding: utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from common.serialization_tools import JSONWithURLSerializer
from family_tree.decorators import same_family_required
from family_tree.models import Person
from custom_user.decorators import set_language


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
def map_points(request):
    '''
    API to get person location data
    '''

    objects = Person.objects.filter(family_id = request.user.family_id).exclude(longitude = 0, latitude = 0)

    serializer = JSONWithURLSerializer()
    data = serializer.serialize(objects, fields=('id','name','small_thumbnail','latitude','longitude'))
    return HttpResponse(data, content_type="application/json")

