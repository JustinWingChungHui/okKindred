from gallery.models import Gallery
from django.contrib.auth.decorators import login_required
from custom_user.decorators import set_language
#from family_tree.decorators import same_family_required
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
#http://miromannino.github.io/Justified-Gallery/
#http://masonry.desandro.com/
#http://www.sitepoint.com/jquery-infinite-scrolling-demos/

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
def gallery_data(request, page):
    '''
    Gets the paginated gallery data as JSON
    https://docs.djangoproject.com/en/1.7/topics/pagination/
    '''
    gallery_list = Gallery.objects.filter(family_id=request.user.family_id)
    paginator = Paginator(gallery_list, 12) #show 12 per request, divisable by lots of numbers

    try:
        galleries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        galleries = paginator.page(1)
    except EmptyPage:
        # If page is out of range return blank
        return HttpResponse('', content_type="application/json")

    data = serializers.serialize('json', galleries, fields=('id','title', 'thumbnail'))

    return HttpResponse(data, content_type="application/json")


