from django.db import models
from gallery.models import Image
from math import sin, cos, pi
from django.utils import translation
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

class Tag(models.Model):
    '''
    Represents a family member tag in an image
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'gallery'
        unique_together = ("image", "person")

        indexes = [
            models.Index(fields=['image']),
            models.Index(fields=['person'])
        ]

    image = models.ForeignKey(Image, blank=False, null=False, on_delete=models.CASCADE)
    person = models.ForeignKey('family_tree.Person', null=False, on_delete=models.CASCADE) #Use of model string name to prevent circular import

    #Box coordinates in the photo normalised to 1 (ie [(0,0),(1,1)] is entire photo
    x1 = models.FloatField(blank=False, null=False)
    y1 = models.FloatField(blank=False, null=False)
    x2 = models.FloatField(blank=False, null=False)
    y2 = models.FloatField(blank=False, null=False)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self): # __unicode__ on Python 2
        return self.image.title + ': ' + self.person.name

    def rotate(self, anticlockwise_angle_degrees = 90):
        '''
        Rotates tag in relation to center of image
        '''
        t = anticlockwise_angle_degrees / 360 * 2 * pi

        # Change origin from top left corner of image to center of image
        x1 = self.x1 - 0.5
        y1 = 0.5 - self.y1
        x2 = self.x2 - 0.5
        y2 = 0.5 - self.y2

        # Use matrix rotation
        x1r = x1 * cos(t) - y1 * sin(t)
        y1r = x1 * sin(t) + y1 * cos(t)
        x2r = x2 * cos(t) - y2 * sin(t)
        y2r = x2 * sin(t) + y2 * cos(t)

        # Change origin back to top left corner of page
        self.x1 = min(x1r + 0.5, x2r + 0.5)
        self.x2 = max(x1r + 0.5, x2r + 0.5)
        self.y1 = min(0.5 - y1r, 0.5 - y2r)
        self.y2 = max(0.5 - y1r, 0.5 - y2r)


    def send_tag_notification_email(self):
        '''
        Sends out an email to a user that they have been tagged in a photo
        '''
        person = self.person
        image = self.image

        if person.user and person.user.receive_photo_update_emails:
            language = person.user.language
            translation.activate(language)

            subject = translation.ugettext('You have been identified in a new photo in ok!Kindred')

            content = translation.ugettext( """Hi {0}
                                                You have been identified in a photo.
                                                To see it, please go to {1}/gallery/{2}/?image_id={3}
                                            """.format(person.user.name, settings.DOMAIN, image.gallery_id, image.id))

            content_html = self.create_email_body_html(person, image)


            send_mail(subject, content, 'info@okkindred.com',[person.user.email], fail_silently=False, html_message=content_html)


    def create_email_body_html(self, person, image):
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


