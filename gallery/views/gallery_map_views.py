from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from common.serialization_tools import JSONWithURLSerializer
from gallery.models import Gallery, Image


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
                                    'token' : settings.MAP_BOX_TOKEN,
                                })


def gallery_map_data(request, gallery_id):
    '''
    Gets the data for the map view
    '''
    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    images = Image.objects.filter(family_id = request.user.family_id, gallery_id = gallery_id).exclude(latitude = 0, longitude = 0)

    serializer = JSONWithURLSerializer()
    data = serializer.serialize(images, fields=('id','name','thumbnail','large_thumbnail','latitude','longitude','title','large_thumbnail_width','large_thumbnail_height'))

    return HttpResponse(data, content_type="application/json")


