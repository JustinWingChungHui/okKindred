from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db import connection
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import localtime
from django.utils.translation import ugettext as tran
from django.views.decorators.http import require_POST, require_GET

from family_tree.decorators import same_family_required
from common.geocoder import geocode_address
from common.serialization_tools import JSONWithURLSerializer
from common.utils import create_hash
from custom_user.decorators import set_language
from gallery.models import Gallery, Image, Tag
from gallery.models.image import upload_to

from os.path import basename
import os
import json
import PIL

MAX_FILE_SIZE = 15000000  # bytes

@login_required
@set_language
@require_GET
def gallery(request, gallery_id, image_id = None):
    '''
    Page to show images in a gallery
    '''

    try:
        gallery = Gallery.objects.get(id=gallery_id)
    except:
        raise Http404

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    if image_id:
        im = get_object_or_404(Image, pk = image_id)

        #Check same family
        if request.user.family_id != im.family_id:
            raise Http404
    else:
        im = None

    return render(request, 'gallery/gallery.html', {
                                    'gallery' : gallery,
                                    'image' : im,
                                })



@login_required
@set_language
@require_GET
def gallery_images(request, gallery_id, page):
    '''
    Gets a view showing all the images within a gallery
    '''
    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    image_list = Image.objects.filter(family_id=request.user.family_id, gallery_id=gallery_id).order_by('date_taken', 'id')
    paginator = Paginator(image_list, 12) #show 12 per request, divisable by lots of numbers

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range return blank
        return HttpResponse('[]', content_type="application/json")

    serializer = JSONWithURLSerializer()
    data = serializer.serialize(
        images, fields=('id','title', 'thumbnail', 'large_thumbnail', 'original_image', 'latitude', 'thumbnail_width', 'thumbnail_height', 'large_thumbnail_width', 'large_thumbnail_height')) #Added latitude to unhide map button

    return HttpResponse(data, content_type="application/json")

@login_required
@set_language
@require_GET
def upload_images(request, gallery_id):
    '''
    Gets the upload image view
    '''
    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    #Gets the upload images view
    return render(request, 'gallery/upload_images.html', {
                                    'gallery' : gallery,
                                })



@login_required
@set_language
@require_POST
def upload_images_post(request, gallery_id):
    '''
    Gets the upload image view
    '''
    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    #Handles uploading of files
    results = []
    for filename, file in request.FILES.items():
        try:
            results.append(process_image(filename, file, gallery))

        except Exception as e:
            results.append(
                {
                    'error': str(e),
                })

    return HttpResponse(json.dumps(results), content_type='application/json')



def process_image(filename, file, gallery):
    '''
    Processes each image file
    '''
    name, ext = os.path.splitext(file.name)
    filename =  create_hash(name) +'.jpg'

    im = Image(gallery_id=gallery.id, family_id=gallery.family_id, title=name)
    upload_name = upload_to(im, filename)

    result = {
        'name': basename(name),
        'size': file.size,
        'url': settings.MEDIA_URL + str(upload_name),
        'filename': filename
    }

    if file.size > MAX_FILE_SIZE:
        result['error'] = tran('File is too big')
        return result

    #Write the file to the destination
    destination = open(os.path.join(settings.MEDIA_ROOT, str(upload_name)), 'wb+')

    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()

    im.original_image = upload_name

    #Check this is a valid image
    try:
        PIL.Image.open(os.path.join(settings.MEDIA_ROOT, str(im.original_image))).verify()
        im.save()
        im.upload_files_to_s3()
        im.delete_local_image_files()

        result['image_id'] = im.id


    except:
        im.delete_local_image_files()
        result['error'] = tran('Invalid image!')

    return result


@login_required
@set_language
@require_GET
def image_detail(request, image_id):
    '''
    Shows the image detail view
    '''
    im = get_object_or_404(Image, pk = image_id)

    #Check same family
    if request.user.family_id != im.family_id:
        raise Http404

    previous_image = list(Image.objects.raw(
            "SELECT * FROM gallery_image WHERE gallery_id = {0} AND (date_taken < '{1}' OR (date_taken = '{1}' AND id < {2})) ORDER BY date_taken DESC, id DESC LIMIT 1".format(im.gallery_id, localtime(im.date_taken), im.id)))

    if len(previous_image) == 0:
        previous_image_id = 0
    else:
        previous_image_id = previous_image[0].id



    next_image = list(Image.objects.raw(
            "SELECT * FROM gallery_image WHERE gallery_id = {0} AND (date_taken > '{1}' OR (date_taken = '{1}' AND id > {2})) ORDER BY date_taken ASC, id ASC LIMIT 1".format(im.gallery_id, localtime(im.date_taken), im.id)))

    if len(next_image) == 0:
        next_image_id = 0
    else:
        next_image_id = next_image[0].id

    #Gets the image detail view
    return render(request, 'gallery/image_tagging.html', {
                                    'image' : im,
                                    'previous_image_id': previous_image_id,
                                    'next_image_id': next_image_id
                                })


@login_required
@set_language
@require_POST
def image_detail_update(request, image_id):
    '''
    Handles the update of image details
    '''
    im = get_object_or_404(Image, pk = image_id)

    #Check same family
    if request.user.family_id != im.family_id:
        raise Http404

    field_name = request.POST.get("name")
    if field_name not in ['title', 'description','date_taken','longitude', 'latitude']:
        raise Http404

    try:
        setattr(im, field_name, request.POST.get("value"))
        im.save()
        return HttpResponse(status=200, content="OK")

    except Exception as e:
        return HttpResponse(status=405, content=e)


@login_required
@set_language
@require_POST
def image_delete(request, image_id):
    '''
    Handles the update of image details
    '''
    im = get_object_or_404(Image, pk = image_id)

    #Check same family
    if request.user.family_id != im.family_id:
        raise Http404

    gallery_id = im.gallery_id
    im.delete_local_image_files()
    im.delete_remote_image_files()
    im.delete()

    return HttpResponseRedirect('/gallery={0}/'.format(gallery_id))

@login_required
@set_language
@require_POST
def set_image_as_gallery_thumbnail(request, image_id):
    '''
    Sets the image as the gallery thumbnail
    '''
    im = get_object_or_404(Image, pk = image_id)

    #Check same family
    if request.user.family_id != im.family_id:
        raise Http404

    gallery = Gallery.objects.get(id=im.gallery_id)
    gallery.thumbnail = im.thumbnail
    gallery.save()

    return HttpResponseRedirect('/gallery/')

@login_required
@set_language
@require_POST
def rotate_image(request, image_id):
    '''
    Rotates the image and the tags
    '''
    im = get_object_or_404(Image, pk = image_id)

    #Check same family
    if request.user.family_id != im.family_id:
        raise Http404

    anticlockwise_angle = int(request.POST.get("anticlockwise_angle"))

    if anticlockwise_angle != 0:

        # Rotate the image
        im.rotate(anticlockwise_angle)

        # Rotate the tag
        for tag in list(Tag.objects.filter(image_id = image_id)):
            tag.rotate(anticlockwise_angle)
            tag.save()

    return HttpResponseRedirect('/image={0}/details/'.format(image_id))


@login_required
@set_language
@same_family_required
@require_GET
def person_gallery(request, person_id, person = None, image_id = None):
    '''
    Gets gallery for a particular person
    '''
    if image_id:
        im = get_object_or_404(Image, pk = image_id)

        #Check same family
        if request.user.family_id != im.family_id:
            raise Http404
    else:
        im = None

    return render(request, 'gallery/person_gallery.html', {
                                    'person' : person,
                                    'image' : im,
                                })


@login_required
@set_language
@same_family_required
@require_GET
def person_gallery_data(request, person_id, person = None, page = 1):
    '''
    Gets image data for a particular person
    '''
    image_list = Image.objects.filter(tag__person_id = person_id).order_by('creation_date')

    paginator = Paginator(image_list, 12) #show 12 per request, divisable by lots of numbers

    #Get count to paginate raw query
    cursor = connection.cursor()
    cursor.execute("""  SELECT COUNT(*)
                        FROM gallery_image i
                        INNER JOIN gallery_tag t
                            ON i.id = t.image_id
                            AND t.person_id = {0}
                    """.format(person.id))
    paginator._count = cursor.fetchone()[0]

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range return blank
        return HttpResponse('[]', content_type="application/json")

    serializer = JSONWithURLSerializer()
    data = serializer.serialize(
        images, fields=('id','title', 'thumbnail', 'large_thumbnail', 'original_image', 'latitude', 'thumbnail_width', 'thumbnail_height', 'large_thumbnail_width', 'large_thumbnail_height')) #Added latitude to unhide map button


    return HttpResponse(data, content_type="application/json")


@login_required
@require_POST
def geocode_image_location_post(request, image_id):
    '''
    Uses geolocation services to determine lat and lng
    '''
    im = get_object_or_404(Image, pk = image_id)

    #Check same family
    if request.user.family_id != im.family_id:
        raise Http404

    address = request.POST.get("address")
    location = geocode_address(address)

    im.latitude = location.latitude
    im.longitude = location.longitude
    im.save()

    data = {'latitude': location.latitude, 'longitude': location.longitude}

    return HttpResponse(json.dumps(data), content_type="application/json")