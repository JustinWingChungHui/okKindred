from gallery.models import Tag, Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
import json

@login_required
def get_tags(request, image_id):
    '''
    Shows the image detail view
    '''
    im = get_object_or_404(Image, pk = image_id)

    #Check same family
    if request.user.family_id != im.family_id:
        raise Http404

    tags = Tag.objects.filter(image_id = image_id)
    data = []

    for tag in tags:
        data.append(
                {
                    'id': tag.id,
                    'name': tag.person.name,
                    'person': tag.person_id,
                    'x1': tag.x1,
                    'x2': tag.x2,
                    'y1': tag.y1,
                    'y2': tag.y2,
                })

    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def delete_tag(request, tag_id):
    '''
    Deletes a tag
    '''
    if request.method != 'POST':
        return HttpResponse(status=405, content="Only POST requests allowed")

    tag = get_object_or_404(Tag, pk = tag_id)

    #Check same family
    if request.user.family_id != tag.image.family_id:
        raise Http404

    tag.delete()

    return HttpResponse(status=200, content="OK")


@login_required
def create_tag(request, image_id):
    '''
    Creates a tag
    '''
    if request.method != 'POST':
        return HttpResponse(status=405, content="Only POST requests allowed")

    im = get_object_or_404(Image, pk = image_id)

    #Check same family
    if request.user.family_id != im.family_id:
        raise Http404

    x1 = request.POST.get("x1")
    y1 = request.POST.get("y1")
    x2 = request.POST.get("x2")
    y2 = request.POST.get("y2")
    person_id = request.POST.get("person")

    tag = Tag.objects.create(image_id=image_id, x1=x1, y1=y1, x2=x2, y2=y2, person_id=person_id)
    response =  {
                    'id': tag.id,
                    'name': tag.person.name,
                    'person': tag.person_id,
                    'x1': tag.x1,
                    'x2': tag.x2,
                    'y1': tag.y1,
                    'y2': tag.y2,
                }
    return HttpResponse(json.dumps(response), content_type="application/json")