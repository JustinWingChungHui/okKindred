from gallery.models import Gallery, Image
from gallery.models.image import upload_to
from django.contrib.auth.decorators import login_required
from custom_user.decorators import set_language
from django.template import RequestContext, loader
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.conf import settings
from django.shortcuts import get_object_or_404
from common import create_hash
from django.utils.translation import ugettext as tran
from os.path import basename
import os
import json
import PIL

MAX_FILE_SIZE = 15000000  # bytes

@login_required
@set_language
def gallery(request, gallery_id):
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

    template = loader.get_template('gallery/gallery.html')

    context = RequestContext(request,
                                {
                                    'gallery' : gallery,
                                })

    response = template.render(context)
    return HttpResponse(response)



@login_required
@set_language
def gallery_images(request, gallery_id, page):
    '''
    Gets a view showing all the images within a gallery
    '''
    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    image_list = Image.objects.filter(family_id=request.user.family_id, gallery_id=gallery_id).order_by('date_taken')
    paginator = Paginator(image_list, 12) #show 12 per request, divisable by lots of numbers

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range return blank
        return HttpResponse('', content_type="application/json")

    data = serializers.serialize('json', images, fields=('id','title', 'thumbnail', 'large_thumbnail', 'original_image'))

    return HttpResponse(data, content_type="application/json")

@login_required
@set_language
def upload_images(request, gallery_id):
    '''
    Gets the upload image view
    '''
    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    #Gets the upload images view
    template = loader.get_template('gallery/upload_images.html')
    context = RequestContext(request,
                                {
                                    'gallery' : gallery,
                                })

    response = template.render(context)
    return HttpResponse(response)



@login_required
@set_language
def upload_images_post(request, gallery_id):
    '''
    Gets the upload image view
    '''
    gallery = get_object_or_404(Gallery, pk = gallery_id)

    #Check same family
    if request.user.family_id != gallery.family_id:
        raise Http404

    if request.method != 'POST':
        raise Http404

    #Handles uploading of files

    results = []
    for filename, file in request.FILES.items():
        try:
            results.append(process_image(filename, file, gallery))
        except:
            pass

    return HttpResponse(json.dumps(results), content_type='application/json')



def process_image(filename, file, gallery):
    '''
    Processes each image file
    '''
    name, ext = os.path.splitext(file.name)
    filename =  create_hash(name) +'.jpg'

    im = Image(gallery_id=gallery.id, family_id=gallery.family_id, title=name)
    im.original_image = upload_to(im, filename)

    result = {
        'name': basename(name),
        'size': file.size,
        'url': '/media/' + str(im.original_image),
        'filename': filename
    }

    if file.size > MAX_FILE_SIZE:
        result['error'] = tran('File is too big')
        return result

    #Write the file to the destination
    destination = open(os.path.join(settings.MEDIA_ROOT, str(im.original_image)), 'wb+')

    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()

    #Check this is a valid image
    try:
        PIL.Image.open(os.path.join(settings.MEDIA_ROOT, str(im.original_image))).verify()
        im.save()
    except:
        os.remove(''.join([settings.MEDIA_ROOT,im.original_image]))
        result['error'] = tran('Invalid image!')

    return result