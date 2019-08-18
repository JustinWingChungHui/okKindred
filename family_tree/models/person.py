from pathlib import Path
from PIL import Image
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext as tran
from django.conf import settings
from django.core.validators import validate_email

from common.utils import create_hash
from common.geocoder import geocode_address
from common.s3_synch import upload_file_to_s3, remove_file_from_s3

from custom_user.models import User
from family_tree.models.family import Family

import os
import bleach

#Localised Gender choices https://docs.djangoproject.com/en/1.7/ref/models/fields/#choices
FEMALE ='F'
MALE ='M'
OTHER = 'O'

GENDER_CHOICES = (
    (FEMALE, _('Female')),
    (MALE, _('Male')),
    (OTHER, _('Other')),
)

# Set when all relations are broken
ORPHANED_HIERARCHY_SCORE = -1;

class NullableEmailField(models.EmailField):
    '''
    This allows an unique email field that stores Null but return ""
    Taken from http://bitofpixels.com/blog/unique-on-charfield-when-blanktrue/
    '''

    description = "EmailField that stores NULL but returns ''"

    def __init__(self, *args, **kwargs):
        super(NullableEmailField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, models.EmailField):
            return value
        return value or ''
    def get_prep_value(self, value):
        return value or None



class Person(models.Model):
    '''
    Represents a family member
    Most fields are nullable as a lot of information will be incomplete or private
    '''
    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'family_tree'
        verbose_name_plural = "People"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['family']),
            models.Index(fields=['birth_year']),
            models.Index(fields=['user']),
            models.Index(fields=['hierarchy_score'])
        ]

    #Only required fields
    name = models.CharField(max_length=255, null = False, blank = False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null = False, blank = False)
    locked = models.BooleanField(default = False, null=False) #Allows a user to lock their profile
    family = models.ForeignKey(Family, blank=False, null=False, on_delete=models.CASCADE) #Family
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, null = False, blank = False, default='en')

    #Optional Fields
    birth_year = models.IntegerField(blank=True, null=False, default = 0)
    year_of_death = models.IntegerField(blank=True, null=False, default = 0)

    photo = models.ImageField(upload_to='profile_photos', blank=True, null=False)
    small_thumbnail = models.ImageField(upload_to='profile_photos', blank=True, null=False)
    large_thumbnail = models.ImageField(upload_to='profile_photos', blank=True, null=False)

    email = NullableEmailField(blank=True, null=True, default=None, unique=True)
    telephone_number = models.CharField(max_length=30, blank=True, null=False)
    skype_name = models.CharField(max_length=100, blank=True, null=False)

    website = models.CharField(max_length=100, blank=True, null=False)
    facebook = models.CharField(max_length=100, blank=True, null=False)
    twitter = models.CharField(max_length=100, blank=True, null=False)
    linkedin = models.CharField(max_length=100, blank=True, null=False)

    occupation = models.CharField(max_length=100, blank=True, null=False)
    spoken_languages = models.CharField(max_length=100, blank=True, null=False)
    address = models.CharField(max_length=255, blank=True, null=False)

    biography = models.TextField(null=False, blank=True)

    #Location use https://pypi.python.org/pypi/googlemaps?
    latitude = models.FloatField(blank=True, null=False, default = 0) #(0,0) is in the middle of the ocean so can set this to 0 to avoid nulls
    longitude = models.FloatField(blank=True, null=False, default = 0)

    #Calculated Fields
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) #link this to a user if they have an email address
    hierarchy_score = models.IntegerField(default = 100) #parents have lower score, children have higher

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    allowed_print_tags = [
            # tags whitelist
            "h1", "h2", "h3", "h4", "h5", "h6",
            "b", "i", "strong", "em", "tt","u","small",
            "p", "br",
            "span", "div", "blockquote", "code", "hr",
            "ul", "ol", "li", "dd", "dt",
            "table","thead","tbody","tfoot","tr","th","td",
            ]

    def __str__(self): # __unicode__ on Python 2
        return self.name


    def __init__(self, *args, **kwargs):
        '''
        Initialization of object
        Keeps track of original values in initialization
        '''
        super(Person, self).__init__(*args, **kwargs)
        self._original_email = self.email
        self._original_address = self.address
        self._original_language = self.language
        self._original_name = self.name
        self._original_biography = self.biography


    def have_user_details_changed(self):
        '''
        Do we need to update the user object?
        '''
        #No email no user
        if not self.email:
            return False

        #Change in email
        if self._original_email != self.email:
            return True

        #Change in language
        if self._original_language != self.language:
            return True

        if self._original_name != self.name:
            return True

        #New record
        if not self.id:
            return True

        return False


    def create_update_user(self):
        '''
        Creates a django user if an email address is supplied with  Person
        '''
        #No email or email hasn't changed, then don't create a user
        if not self.have_user_details_changed():
            return

        if self.email:
            validate_email(self.email)
            #Check not used by another user

        #If person is already linked to a user
        if self.user:

            #Update user details
            if self.user.name != self.name or self.user.email != self.email \
                or self.user.family_id != self.family_id or self.user.language != self.language:
                self.user.name = self.name
                self.user.email = self.email
                self.user.family_id = self.family_id
                self.user.language = self.language
                self.user.save_user_only()




    def save(self, *args, **kwargs):
        '''
        Overrides the save method to determine the calculated fields
        '''

        #Ensure email is in lowercase
        if self.email:
            self.email = self.email.lower()

        self.create_update_user()

        #If address has changed, geocode it
        if self._original_address != self.address:
            self.geocode_address()

        #If no address then reset it to 0
        if not self.address:
            self.latitude = 0
            self.longitude = 0

        self.format_urls()

        # Clean biography to mitigate against xss
        if self._original_biography != self.biography:
            self.biography = bleach.clean(text=self.biography, tags=self.allowed_print_tags)

        super(Person, self).save(*args, **kwargs) # Call the "real" save() method.

    def save_person_only(self, *args, **kwargs):
        '''
        Save method without any extras
        '''
        super(Person, self).save(*args, **kwargs) # Call the "real" save() method.


    def set_hierarchy_score(self, relation = None):
        '''
        Sets a hierachy score to help organise tree views
        First person is set to 100, his/her parents have score 99
        His/Her children have score 101
        '''
        from family_tree.models.relation import RAISED, PARTNERED

        if relation is None:
            relation = self._get_first_relation()

        #Orphaned
        if relation is None:
            return

        if relation.from_person_id == self.id:
            other_person = relation.to_person
        else:
            other_person = relation.from_person

        if relation.relation_type == PARTNERED:
            self.hierarchy_score = other_person.hierarchy_score

        elif relation.relation_type == RAISED:
            if relation.from_person_id == self.id:
                self.hierarchy_score = other_person.hierarchy_score - 1
            else:
                self.hierarchy_score = other_person.hierarchy_score + 1


    def _get_first_relation(self):
        '''
        Gets a relation in order to calculate hierarchy
        '''
        if self.to_person.all().count() > 0:
            relation = self.to_person.all()[0]

        elif self.from_person.all().count() > 0:
            relation = self.from_person.all()[0]

        else:
            return None

        return relation


    def geocode_address(self):
        '''
        Gets the logitude and latitude of address for plotting on a map
        '''
        if not self.address:
            return

        location = geocode_address(self.address)

        if location:
            self.latitude = location.latitude
            self.longitude = location.longitude



    def set_profile_image_crop_rotate_resize(self, path_and_filename, x, y, w, h, r, test = False):
        '''
        sets the profile photo, supercedes set_hires_photo, crop_and_resize_photo, rotate_photo
        '''

        try:
            media_path = Path(settings.MEDIA_ROOT)
            path = Path(path_and_filename)
            rel_path = Path(os.path.relpath(path, media_path))

            small_thumb_path = Path(rel_path.parent, rel_path.stem + '_small_thumb').with_suffix('.jpg')
            large_thumb_path = Path(rel_path.parent, rel_path.stem + '_large_thumb').with_suffix('.jpg')

            im = Image.open(path)
            im.verify()

            #Open it again!
            #https://pillow.readthedocs.io/en/3.0.x/reference/Image.html?highlight=verify#PIL.Image.Image.verify

            im = Image.open(path)
            im = im.convert('RGB')

            if r != 0:
                im = im.rotate(r, resample=Image.BICUBIC, expand=True)

            im = im.crop((x, y, x + w, y + h))

            # small thumbnail
            small_thumb = im.copy()
            small_thumb.thumbnail((80,80), Image.ANTIALIAS)
            small_thumb.save(media_path.joinpath(small_thumb_path), "JPEG", quality=75)

            # large thumbnail
            large_thumb = im.copy()
            large_thumb.thumbnail((200,200), Image.ANTIALIAS)
            large_thumb.save(media_path.joinpath(large_thumb_path), "JPEG", quality=75)

            old_photo = self.photo
            old_small_thumbnail = self.small_thumbnail
            old_large_thumbnail = self.large_thumbnail


            # Set model properties
            self.photo = str(rel_path)
            self.small_thumbnail = str(small_thumb_path)
            self.large_thumbnail = str(large_thumb_path)

            upload_file_to_s3(self.photo)
            upload_file_to_s3(self.small_thumbnail)
            upload_file_to_s3(self.large_thumbnail)

            # Remove old photos from S3
            if old_photo:
                old_photo_path = ''.join([settings.MEDIA_ROOT, str(old_photo)])
                remove_file_from_s3(old_photo_path)
                old_small_thumbnail_path = ''.join([settings.MEDIA_ROOT, str(old_small_thumbnail)])
                remove_file_from_s3(old_small_thumbnail_path)
                old_large_thumbnail_path = ''.join([settings.MEDIA_ROOT, str(old_large_thumbnail)])
                remove_file_from_s3(old_large_thumbnail_path)

        except:

            raise Exception("Invalid image!")

        finally:

            # Need to check these images if testing
            if not test:
                self.remove_local_images()




    def set_hires_photo(self, filename):
        '''
        Checks file is an image and converts it to a small jpeg
        DEPRECATED
        '''
        #Check this is a valid image
        try:

            path_and_filename = ''.join([settings.MEDIA_ROOT, 'profile_photos/', filename])
            im = Image.open(path_and_filename)
            im.verify()

            #Open it again!
            #http://stackoverflow.com/questions/12413649/python-image-library-attributeerror-nonetype-object-has-no-attribute-xxx
            im = Image.open(path_and_filename).convert('RGB') #Convert to RGB
            im.thumbnail((500,500), Image.ANTIALIAS) #Reasonble size to allow cropping down to 200x200

            im.save(path_and_filename, "JPEG", quality=95)

            self.photo = 'profile_photos/' + filename
            upload_file_to_s3(self.photo)

        except:
            os.remove(path_and_filename)
            raise Exception(tran("Invalid image!")) #Use tran here as it gets serialized so lazy tran fails



    def crop_and_resize_photo(self, x, y, w, h):
        '''
        Crops the photo and produces a large and small thumbnail
        DEPRECATED
        '''

        path_and_filename = ''.join([settings.MEDIA_ROOT, str(self.photo)])
        im = Image.open(path_and_filename)

        width, height=im.size

        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)

        small_thumb_name = ''.join([create_hash(self.name), 'small_thumb', '.jpg'])
        large_thumb_name = ''.join([create_hash(self.name), 'large_thumb', '.jpg'])

        small_thumb = im.copy()
        small_thumb.crop((x, y, x + w, y + h)
            ).resize((80,80), Image.ANTIALIAS
            ).save(''.join([settings.MEDIA_ROOT, 'profile_photos/', small_thumb_name]), "JPEG", quality=75)
        self.small_thumbnail = 'profile_photos/' + small_thumb_name

        large_thumb = im.copy()
        large_thumb.crop((x, y, x + w, y + h)
            ).resize((200,200), Image.ANTIALIAS
            ).save(''.join([settings.MEDIA_ROOT, 'profile_photos/', large_thumb_name]), "JPEG", quality=75)

        self.large_thumbnail = 'profile_photos/' + large_thumb_name

        upload_file_to_s3(self.small_thumbnail)
        upload_file_to_s3(self.large_thumbnail)


    def rotate_photo(self, anticlockwise_angle):
        '''
        Rotates the photo
        DEPRECATED
        '''
        path_and_filename = ''.join([settings.MEDIA_ROOT, str(self.photo)])
        im = Image.open(path_and_filename)

        new_image = im.rotate(anticlockwise_angle, resample=Image.BICUBIC, expand=True)
        self.photo = ''.join(['profile_photos/', create_hash(self.name), '.jpg'])
        new_image.save(''.join([settings.MEDIA_ROOT, str(self.photo)]))

        os.remove(path_and_filename)
        remove_file_from_s3(path_and_filename)


    def format_urls(self):
        '''
        Ensures that urls start with http://
        '''
        if self.website and not self.website.startswith('http'):
            self.website = 'http://' + self.website


    def remove_local_images(self):
        '''
        Removes the local copies of the image files
        '''
        photo = ''.join([settings.MEDIA_ROOT, str(self.photo)])
        if os.path.exists(photo):
            os.remove(photo)

        small_thumb = ''.join([settings.MEDIA_ROOT, str(self.small_thumbnail)])
        if os.path.exists(small_thumb):
            os.remove(small_thumb)

        large_thumb = ''.join([settings.MEDIA_ROOT, str(self.large_thumbnail)])
        if os.path.exists(large_thumb):
            os.remove(large_thumb)


    def remove_remote_images(self):
        '''
        Removes the remote copies of the image files
        '''
        photo = ''.join([settings.MEDIA_ROOT, str(self.photo)])
        remove_file_from_s3(photo)

        small_thumb = ''.join([settings.MEDIA_ROOT, str(self.small_thumbnail)])
        remove_file_from_s3(small_thumb)

        large_thumb = ''.join([settings.MEDIA_ROOT, str(self.large_thumbnail)])
        remove_file_from_s3(large_thumb)

