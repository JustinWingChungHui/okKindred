from gallery.models import Tag, Image
from family_tree.models import Person
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
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

    response =  {
                    'id': tag_id
                }

    return HttpResponse(json.dumps(response) , content_type="application/json")


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

    #Check person from same family
    person = get_object_or_404(Person, pk = person_id)
    if person.family_id != request.user.family_id:
        raise Http404

    tag = Tag.objects.create(image_id=image_id, x1=x1, y1=y1, x2=x2, y2=y2, person_id=person_id)

    # Send notification email
    if person.user and person.user.receive_photo_update_emails:
        send_tag_notification_email(person, im)

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


def send_tag_notification_email(person, image):
    '''
    Sends out an email to a user that they have been tagged in a photo
    '''

    language = person.user.language
    translation.activate(language)

    subject = translation.ugettext('You have been identified in a new photo in ok!Kindred')

    content = translation.ugettext( """Hi {0}
                                        You have been identified in a photo.
                                        To see it, please go to {1}/person={2}/photos/image={3}/
                                    """.format(person.user.name, settings.DOMAIN, person.id, image.id))

    content_html = create_email_body_html(person, image)


    send_mail(subject, content, 'info@okkindred.com',[person.user.email], fail_silently=False, html_message=content_html)


def create_email_body_html(person, image):
    '''
    Creates the email from a template
    '''
    language = person.user.language
    translation.activate(language)

    content_html = get_template('gallery/you_have_been_tagged.html').render(
                    {
                        'language' : language,
                        'user' : person.user,
                        'image' : image,
                        'domain' : settings.DOMAIN,
                        'person' : person,
                    })

    return content_html