# encoding: utf-8
from django.contrib.auth.decorators import login_required
from family_tree.decorators import same_family_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person

@login_required
@same_family_required
def map(request, person_id = 0, person = None):

    locations = {}
    for member in list(Person.objects.filter(family_id = request.user.family_id).exclude(latitude = 0, longitude = 0)):

        point = (member.latitude, member.longitude)

        if not point in locations:
            locations[point] = Location(str(point), member.latitude, member.longitude)

        locations[point].people.append(member)


    template = loader.get_template('family_tree/family_map.html')
    context = RequestContext(request,{
                                    'this_person' : person,
                                    'locations' : locations.values(),
                                    'zoom' : 7 if request.user.id == person.user_id else 12,
                                })

    response = template.render(context)
    return HttpResponse(response)


class Location(object):

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.people = []


