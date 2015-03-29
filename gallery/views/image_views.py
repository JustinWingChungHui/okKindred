from gallery.models import Gallery, Image
from django.contrib.auth.decorators import login_required
from custom_user.decorators import set_language
from django.template import RequestContext, loader
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.shortcuts import get_object_or_404


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

    template = loader.get_template('gallery/upload_images.html')

    context = RequestContext(request,
                                {
                                    'gallery' : gallery,
                                })

    response = template.render(context)
    return HttpResponse(response)