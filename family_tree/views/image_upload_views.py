# encoding: utf-8
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.http import Http404
from django.conf import settings
from django.http import HttpResponseRedirect
from family_tree.decorators import same_family_required
from custom_user.decorators import set_language
from common import create_hash
import json


MAX_FILE_SIZE = 15000000  # bytes


def get_file_size(file):
    file.seek(0, 2)  # Seek to the end of the file
    size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return size


@login_required
@set_language
@same_family_required
def edit_profile_photo(request, person_id = 0, person = None):
    '''
    That shows the upload form
    '''

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
@set_language
@same_family_required
def image_upload(request, person_id = 0, person = None):
    '''
    View that receives the uploaded image
    '''

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404

    try:
        uploaded = request.FILES['picture']
    except:
        raise Http404


    #get the name, and extension and create a unique filename
    name, ext = os.path.splitext(uploaded.name)
    filename =  create_hash(person.name) +'.jpg'
    photo_file = ''.join([settings.MEDIA_ROOT, 'profile_photos/', filename])

    result = {
        'name': uploaded.name,
        'size': uploaded.size,
        'url': '/media/profile_photos/' + filename,
        'filename': filename
    }

    if uploaded.size > MAX_FILE_SIZE:
        result['error'] = _('File is too big')
        return HttpResponse(json.dumps(result), content_type='application/json')

    #Write the file to the destination
    destination = open(photo_file, 'wb+')

    for chunk in uploaded.chunks():
        destination.write(chunk)
    destination.close()

    #Check this is a valid image
    try:
        person.set_hires_photo(filename)

    except Exception as ex:
        result['error'] = str(ex)

        return HttpResponse(json.dumps(result), content_type='application/json')

    person.save()


    return HttpResponse(json.dumps(result), content_type='application/json')



@login_required
@set_language
@same_family_required
def image_resize(request, person_id = 0, person = None):
    '''
    Shows the image resize page
    '''

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


@login_required
@set_language
@same_family_required
def image_crop(request, person_id = 0, person = None):
    '''
    Crops the image and assigns the thumbnails to the profile
    '''

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404

    try:
        x = int(request.POST.get("x"))
        y = int(request.POST.get("y"))
        w = int(request.POST.get("w"))
        h = int(request.POST.get("h"))
        display_height = int(request.POST.get("display_height"))
    except:
        raise Http404

    if w != h:
        raise Http404

    if display_height == 0:
        raise Http404

    person.crop_and_resize_photo(x, y, w, h, display_height)
    person.save()

    return HttpResponseRedirect('/edit_profile={0}/'.format(person_id))
