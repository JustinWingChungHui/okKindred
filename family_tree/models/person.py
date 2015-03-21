from django.db import models
from custom_user.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as tran
from django.core.validators import validate_email
from family_tree.models.family import Family
from django.conf import settings
from PIL import Image
import os
from common import create_hash

#Localised Gender choices https://docs.djangoproject.com/en/1.7/ref/models/fields/#choices
FEMALE ='F'
MALE ='M'
OTHER = 'O'

GENDER_CHOICES = (
    (FEMALE, _('Female')),
    (MALE, _('Male')),
    (OTHER, _('Other')),
)



class PersonManager(models.Manager):
    '''
    Manager extended to get related family members
    '''



class NullableEmailField(models.EmailField):
    '''
    This allows an unique email field that stores Null but return ""
    Taken from http://bitofpixels.com/blog/unique-on-charfield-when-blanktrue/
    '''

    description = "EmailField that stores NULL but returns ''"
    __metaclass__ = models.SubfieldBase
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

    #Customer Manager
    objects = PersonManager()

    #Only required fields
    name = models.CharField(max_length=255, db_index = True, null = False, blank = False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null = False, blank = False)
    locked = models.BooleanField(default = False, null=False) #Allows a user to lock their profile
    family = models.ForeignKey(Family, blank=False, null=False, db_index = True) #Family
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, null = False, blank = False, default='en')

    #Optional Fields
    birth_year = models.IntegerField(blank=True, null=False, default = 0)
    year_of_death = models.IntegerField(blank=True, null=False, default = 0)

    photo = models.ImageField(upload_to='profile_photos', blank=True, null=False)
    small_thumbnail = models.ImageField(upload_to='profile_photos', blank=True, null=False)
    large_thumbnail = models.ImageField(upload_to='profile_photos', blank=True, null=False)

    email = NullableEmailField(blank=True, null=True, default=None, unique=True)
    telephone_number = models.CharField(max_length=30, blank=True, null=False)
    website = models.CharField(max_length=100, blank=True, null=False)
    address = models.CharField(max_length=255, blank=True, null=False)

    #Location use https://pypi.python.org/pypi/googlemaps?
    latitude = models.FloatField(blank=True, null=False, default = 0) #(0,0) is in the middle of the ocean so can set this to 0 to avoid nulls
    longitude = models.FloatField(blank=True, null=False, default = 0)

    #Calculated Fields
    user = models.ForeignKey(User, blank=True, null=True, db_index = True) #link this to a user if they have an email address
    hierarchy_score = models.IntegerField(default = 100, db_index = True) #parents have lower score, children have higher

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)


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
        self.original_language = self.language


    def have_user_details_changed(self):
        '''
        Do we need to update the user object?
        '''
        #No email no user
        if not self.email:
            return False

        #Change in email
        if (self._original_email != self.email):
            return True

        #Change in language
        if (self.original_language != self.language):
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

        from familyroot.secrets import GOOGLE_API_KEY

        #Attempt to google the location, if it fails, try bing as backup
        try:
            from geopy.geocoders import GoogleV3
            google_locator = GoogleV3(api_key = GOOGLE_API_KEY)
            location = google_locator.geocode(self.address)


            if location.latitude == 0 and location.longitude ==0:
                self._geocode_address_using_backup()

            self.latitude = location.latitude
            self.longitude = location.longitude

        except:
            self._geocode_address_using_backup()



    def _geocode_address_using_backup(self):
        '''
        Gets the logitude and latitude of address for plotting on a map from backup service (Bing)
        '''
        try:

            from familyroot.secrets import BING_MAPS_API_KEY
            from geopy.geocoders import Bing
            bing_locator = Bing(api_key = BING_MAPS_API_KEY)

            location = bing_locator.geocode(self.address)

            self.latitude = location.latitude
            self.longitude = location.longitude

        except:
            return


    def set_hires_photo(self, filename):
        '''
        Checks file is an image and converts it to a small jpeg
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

            im.save(path_and_filename, "JPEG", quality=90)


            self.photo = 'profile_photos/' + filename

        except:
            os.remove(path_and_filename)
            raise Exception(tran("Invalid image!")) #Use tran here as it gets serialized so lazy tran fails



    def crop_and_resize_photo(self, x, y, w, h, display_height):
        '''
        Crops the photo and produces a large and small thumbnail
        '''

        path_and_filename = ''.join([settings.MEDIA_ROOT, str(self.photo)])
        im = Image.open(path_and_filename)

        width, height=im.size
        ratio = height / display_height

        #Prevent picture becoming too big during crop
        if ratio > 6:
            raise Exception(tran("Invalid image!"))

        x = int(x * ratio)
        y = int(y * ratio)
        w = int(w * ratio)
        h = int(h * ratio)

        small_thumb_name = ''.join([create_hash(self.name), 'small_thumb', '.jpg'])
        large_thumb_name = ''.join([create_hash(self.name), 'large_thumb', '.jpg'])

        small_thumb = im.copy()
        small_thumb.crop((x, y, x + w, y + h)).resize((80,80), Image.ANTIALIAS).save(''.join([settings.MEDIA_ROOT, 'profile_photos/', small_thumb_name]), "JPEG", quality=75)
        self.small_thumbnail = 'profile_photos/' + small_thumb_name

        large_thumb = im.copy()
        large_thumb.crop((x, y, x + w, y + h)).resize((200,200), Image.ANTIALIAS).save(''.join([settings.MEDIA_ROOT, 'profile_photos/', large_thumb_name]), "JPEG", quality=75)
        self.large_thumbnail = 'profile_photos/' + large_thumb_name