# encoding: utf-8

import os
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
#from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
#from django.http import HttpResponseRedirect
import json
from django.core.urlresolvers import reverse

#https://github.com/Alem/django-jfu
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

#https://bitbucket.org/gruy/django-jquery-uploader/src/767bd9f2bf59fc9d0d2a228358e5f70608d2536a/jquery_uploader/views.py?at=default
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
        photo_file = settings.MEDIA_ROOT + '/profile_photos/' + filename

        #Write the file to the destination
        destination = open(photo_file, 'wb+')

        for chunk in uploaded.chunks():
            destination.write(chunk)
        destination.close()

        #Update the person object with the new photo
        person.photo = 'profile_photos/' + filename
        person.save()

    except:
        raise Http404

    result = []
    result.append({
        'delete_type': 'POST',
        'delete_url': reverse('jquery_uploader_delete', args=[uploaded.name, ]),
        'name': uploaded.name,
        'size': uploaded.size,
        'url': photo_file,
    })
    results = {'picture': result}
    return HttpResponse(json.dumps(results), mimetype='application/json')


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
