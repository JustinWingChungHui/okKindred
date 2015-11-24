from gallery.models import Gallery
from django.contrib.auth.decorators import login_required
from custom_user.decorators import set_language
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.shortcuts import get_object_or_404


@login_required
@set_language
def gallery_index(request):
    '''
    A list of galleries for a family
    '''
    template = loader.get_template('gallery/gallery_index.html')

    context = RequestContext(request)

    response = template.render(context)
    return HttpResponse(response)


@login_required
@set_language
def gallery_index_data(request, page):
    '''
    Gets the paginated image data as JSON
    https://docs.djangoproject.com/en/1.7/topics/pagination/
    '''
    gallery_list = Gallery.objects.filter(family_id=request.user.family_id).order_by('-last_updated_date')
    paginator = Paginator(gallery_list, 12) #show 12 per request, divisable by lots of numbers

    try:
        galleries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        galleries = paginator.page(1)
    except EmptyPage:
        # If page is out of range return blank
        return HttpResponse('[]', content_type="application/json")

    data = serializers.serialize('json', galleries, fields=('id','title', 'thumbnail', 'description', 'last_updated_date'))

    return HttpResponse(data, content_type="application/json")


@login_required
@set_language
def edit_gallery(request, gallery_id = 0):
    '''
    Shows the new/edit gallery form and handles POST request
    '''
    if request.method != 'POST':

        if gallery_id == 0:
            gallery = Gallery()
        else:
            gallery = get_object_or_404(Gallery, pk=gallery_id)

            if gallery.family_id != request.user.family_id:
                raise Http404

        template = loader.get_template('gallery/edit_gallery.html')

        context = RequestContext(request,
                            {
                                'gallery_id' : gallery_id,
                                'gallery_title' : gallery.title,
                                'gallery_description' : gallery.description,
                            })

        response = template.render(context)
        return HttpResponse(response)

    else:
        family_id = request.user.family_id
        title = request.POST.get("title").strip()
        description = request.POST.get("description").strip()

        if gallery_id != 0:
            gallery = get_object_or_404(Gallery, pk=gallery_id)

            #Ensure cannot edit another persons family
            if gallery.family_id != family_id:
                raise Http404

            gallery.title = title
            gallery.description = description
            gallery.save()

        else:
            gallery = Gallery.objects.create(family_id=family_id, title=title, description=description)

        return HttpResponseRedirect('/gallery={0}/'.format(gallery.id))

@login_required
@set_language
def delete_gallery(request, gallery_id):
    '''
    Deletes a gallery and all associated images
    '''
    if request.method != 'POST':
        raise Http404

    gallery = get_object_or_404(Gallery, pk=gallery_id)

    #Ensure cannot edit another persons family
    if gallery.family_id != request.user.family_id:
        raise Http404

    gallery.delete_all_images()
    gallery.delete()

    return HttpResponseRedirect('/gallery/')

