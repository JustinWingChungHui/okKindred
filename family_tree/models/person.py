from django.db import models
from custom_user.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email
from family_tree.models.family import Family

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


    def get_related_data(self,person):
        '''
        Gets all the relations and people that are related to the arguement person as a named tuple
        people_upper: People with a higher hierachy score (e.g. parents)
        people_lower: People with a lower hierachy score (e.g. kids)
        relations: List of relations
        '''
        import collections
        related_data = collections.namedtuple('related_data', ['people_upper', 'people_same_level', 'people_lower', 'relations'])

        from django.db.models import Q
        from family_tree.models import Relation
        relations = Relation.objects.filter(Q(from_person=person) | Q(to_person=person))

        #Yeah get some raw SQL on!  We are assuming that the 'from' has a higher hierarchy than the 'to'
        people_upper = list(Person.objects.raw("""   SELECT p.*
                                                FROM family_tree_person p
                                                INNER JOIN family_tree_relation r
                                                    ON r.from_person_id = p.id
                                                WHERE r.to_person_id = %s AND r.relation_type = 2
                                                ORDER BY p.hierarchy_score, gender
                                        """, [person.id]))

        people_same_level = list(Person.objects.raw("""  SELECT p.*
                                                    FROM family_tree_person p
                                                    INNER JOIN family_tree_relation r
                                                        ON r.from_person_id = p.id
                                                    WHERE r.to_person_id = {0} AND r.relation_type = 1
                                                    UNION ALL
                                                    SELECT p.*
                                                    FROM family_tree_person p
                                                    INNER JOIN family_tree_relation r
                                                        ON r.to_person_id = p.id
                                                    WHERE r.from_person_id = {0} AND r.relation_type = 1
                                                    ORDER BY p.hierarchy_score, gender
                                        """.format(person.id)))

        people_lower = list(Person.objects.raw("""   SELECT p.*
                                                FROM family_tree_person p
                                                INNER JOIN family_tree_relation r
                                                    ON r.to_person_id = p.id
                                                WHERE r.from_person_id = %s AND r.relation_type = 2
                                                ORDER BY p.hierarchy_score, gender
                                        """, [person.id]))

        return related_data(people_upper, people_same_level, people_lower, relations)


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
    name = models.CharField(max_length=255, db_index = True, unique = True, null = False, blank = False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null = False, blank = False)
    locked = models.BooleanField(default = False, null=False) #Allows a user to lock their profile
    family = models.ForeignKey(Family, blank=False, null=False) #Family

    #Optional Fields
    birth_year = models.IntegerField(blank=True, null=False, default = 0)
    year_of_death = models.IntegerField(blank=True, null=False, default = 0)

    photo = models.ImageField(upload_to='profile_photos', blank=True, null=False)
    email = NullableEmailField(blank=True, null=True, default=None, unique=True)
    telephone_number = models.CharField(max_length=30, blank=True, null=False)
    website = models.CharField(max_length=100, blank=True, null=False)
    address = models.CharField(max_length=255, blank=True, null=False)

    #Location use https://pypi.python.org/pypi/googlemaps?
    latitude = models.FloatField(blank=True, null=False, default = 0) #(0,0) is in the middle of the ocean so can set this to 0 to avoid nulls
    longitude = models.FloatField(blank=True, null=False, default = 0)

    #Calculated Fields
    user = models.ForeignKey(User, blank=True, null=True) #link this to a user if they have an email address
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



    def create_update_user(self):
        '''
        Creates a django user if an email address is supplied with  Person
        '''
        #No email or email hasn't changed, then don't create a user
        if not self.email or (self._original_email == self.email and self.id):
            return

        if self.email:
            validate_email(self.email)

        #If person is already linked to a user
        if self.user:

            #Update user details
            self.user.name=self.name
            self.user.email = self.email
            self.user.save()

        else: #Person is not already linked to a user

            user = User.objects.filter(email = self.email).first() #returns None if none already exists

            #No user with this email already exists
            if not user:

                password=User.objects.make_random_password(length=8)

                #Create a new user
                user = User(email=self.email, name=self.name, password=password)
                user.save()
                self.user = user

                return password

            else:

                #if user already is taken
                if Person.objects.filter(user_id = user.id).count() > 0:
                    raise Exception(_("Email Address is already in use!"))
                else:
                    self.user_id = user.id


    def save(self, *args, **kwargs):
        '''
        Overrides the save method to determine the calculated fields
        '''

        self.create_update_user()

        #If address has changed, geocode it
        if self._original_address != self.address:
            self.geocode_address()

        #If no address then reset it to 0
        if not self.address:
            self.latitude = 0
            self.longitude = 0

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

