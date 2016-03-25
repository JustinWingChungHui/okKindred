from gallery.models import Gallery, Image
from family_tree.services import map_service
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
import json


def gallery_map(request, gallery_id):
    '''
    Loads a map view of the image gallery
    '''

    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    return render(request, 'gallery/gallery_map.html', {
                                    'gallery' : gallery,
                                    'latitude' : 0,
                                    'longitude' : 0,
                                    'zoom' : 5,
                                })


def gallery_map_data(request, gallery_id, division_size):
    '''
    Gets the data for the map view
    '''
    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    location_points = {}

    images = Image.objects.filter(family_id = request.user.family_id, gallery_id = gallery_id).exclude(latitude = 0, longitude = 0)

    division_size_float = float(division_size)

    for image in images:
        loc = map_service.get_snapped_location(image, division_size_float)

        key = str(loc) #Needs to be a string to serialize

        if key not in location_points:
            location_points[key] = []

        location_points[key].append({
                                        'id': image.id,
                                        'name': image.title,
                                        'thumbnail': str(image.thumbnail),
                                        'large_thumbnail': str(image.large_thumbnail),
                                        'latitude': image.latitude,
                                        'longitude': image.longitude,
                                        'title' : image.title,
                                        'large_thumbnail_width' : image.large_thumbnail_width,
                                        'large_thumbnail_height' : image.large_thumbnail_height
                                    })

    return HttpResponse(json.dumps(location_points), content_type="application/json")


