# encoding: utf-8
from django.contrib.auth.decorators import login_required
from family_tree.decorators import same_family_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
from custom_user.decorators import set_language

@login_required
@set_language
@same_family_required
def open_map(request, person_id = 0, person = None):
    '''
    View to show open map
    '''
    locations = {}
    for member in list(Person.objects.filter(family_id = request.user.family_id).exclude(latitude = 0, longitude = 0)):

        point = (member.latitude, member.longitude)

        if not point in locations:
            locations[point] = Location(str(point), member.latitude, member.longitude)

        locations[point].add_person(member)


    template = loader.get_template('family_tree/open_street_map.html')
    context = RequestContext(request,{
                                    'this_person' : person,
                                    'locations' : locations.values(),
                                    'zoom' : 7 if request.user.id == person.user_id else 12,
                                })

    response = template.render(context)
    return HttpResponse(response)


class Location(object):
    '''
    Represents a location on a map
    It can have multiple peopl on it
    '''

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.people = []
        self.double_width =  False

    def add_person(self, person):
        '''
        Adds a person to the location
        '''

        self.people.append(person)

        if len(self.people) > 1:
            #Used for map formatting
            self.double_width =  True

