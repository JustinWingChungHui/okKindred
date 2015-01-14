# encoding: utf-8

import os
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
#from django.http import HttpResponseRedirect
import json
from PIL import Image

#https://blueimp.github.io/jQuery-File-Upload/basic-plus.html
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
        uploaded = request.FILES['picture']

        #get the name, and extension and create a unique filename
        name, ext = os.path.splitext(uploaded.name)
        filename =  str(uuid.uuid4()) + ext
        photo_file = settings.MEDIA_ROOT + 'profile_photos/' + filename

        #Write the file to the destination
        destination = open(photo_file, 'wb+')

        for chunk in uploaded.chunks():
            destination.write(chunk)
        destination.close()

        #Check this is a valid image
        try:
            trial_image = Image.open(photo_file)
            trial_image.verify()
        except:
            os.remove(photo_file)
            return HttpResponse(_('Invalid image!'))


        #Update the person object with the new photo
        person.photo = 'profile_photos/' + filename
        person.save()

    except:
        raise Http404

    result = {
            'name': uploaded.name,
            'size': uploaded.size,
            'url': '/media/profile_photos/' + filename,
            'filename': filename,
        }
    results = {'picture': result}
    return HttpResponse(json.dumps(results), content_type='application/json')


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

