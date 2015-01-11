# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
from django.http import HttpResponseRedirect

#https://github.com/sigurdga/django-jquery-file-upload

@login_required
def edit_profile_photo(request, person_id):
    '''
    That shows the upload form
    '''
    person = get_object_or_404(Person, id = person_id)

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404


    template = loader.get_template('family_tree/image_upload.html')
    context = RequestContext(request,{
                                    'person' : person,
                                })

    response = template.render(context)
    return HttpResponse(response)


@login_required
def image_upload(request, person_id):
    '''
    View that receives the uploaded image
    '''

    person = get_object_or_404(Person, id = person_id)

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404

    try:
        import uuid
        photo_file = settings.MEDIA_ROOT + '/profile_photos/' + str(uuid.uuid4())
        f = request.FILES['picture']
        destination = open(photo_file, 'wb+')

        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

        person.photo = photo_file
        person.save()

    except:
        raise Http404

    return HttpResponseRedirect('/image_resize=%s/' % person_id)


@login_required
def image_resize(request, person_id):
    '''
    Shows the image resize page
    '''
    person = get_object_or_404(Person, id = person_id)

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404


    template = loader.get_template('family_tree/image_resize.html')
    context = RequestContext(request,{
                                    'person' : person,
                                })

    response = template.render(context)
    return HttpResponse(response)
