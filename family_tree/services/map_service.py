from family_tree.models import Person
import math

def get_person_location_points(family_id, division_size):
    '''
    Gets the location points of people given the family ID and the bounds
    of format [[Lat1, Lon1,], [Lat2,Lon2]]
    http://leafletjs.com/reference.html#latlngbounds
    '''
    location_points = {}

    people = Person.objects.filter(family_id = family_id).exclude(latitude = 0, longitude = 0)

    for person in people:
        loc = get_snapped_location(person, division_size)

        key = str(loc) #Needs to be a string to serialize

        if key not in location_points:
            location_points[key] = []

        location_points[key].append({
                                        'id': person.id,
                                        'name': person.name,
                                        'small_thumbnail': str(person.small_thumbnail),
                                        'latitude': person.latitude,
                                        'longitude': person.longitude
                                    })

    return location_points


def get_snapped_location(object, division_size):
    '''
    Gets the snapped location [Lat, Lon] given the bounds [[Lat1, Lon1,], [Lat2,Lon2]] and division size
    '''
    mid_division = division_size / 2

    #Get number of divisions from south pole
    n_across = math.floor((object.latitude + 90.0) / division_size)
    snapped_latitude = -90.0 + mid_division + n_across * division_size

    #Get number of divisions from date line
    n_up = math.floor((object.longitude + 180.0) / division_size)
    snapped_longitude = -180.0 + mid_division + n_up * division_size

    return (snapped_latitude, snapped_longitude)


