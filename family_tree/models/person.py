from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Other'),
)


class Person(models.Model):
    '''
    Represents a family member
    Most fields are nullable as a lot of information will be incomplete or private
    '''
    class Meta:
        #Allows models.py to be spp[lit up across multiple files
        app_label = 'family_tree'

    #Only required fields
    name = models.CharField(max_length=255, db_index = True, unique = True, null = False, blank = False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null = False, blank = False)
    locked = models.BooleanField(default = False, null=False) #Allows a user to lock their profile


    #Optional Fields
    birth_year = models.IntegerField(blank=True, null=False, default = 0)
    year_of_death = models.IntegerField(blank=True, null=False, default = 0)

    photo = models.ImageField(upload_to='profile_photos', blank=True, null=False)
    email =  models.CharField(max_length=100, blank=True, null=False)
    telephone_number = models.CharField(max_length=30, blank=True, null=False)
    website = models.CharField(max_length=100, blank=True, null=False)


    #Location use https://pypi.python.org/pypi/googlemaps?
    latitude = models.FloatField(blank=True, null=False, default = 0) #(0,0) is in the middle of the ocean so can set this to 0 to avoid nulls
    longitude = models.FloatField(blank=True, null=False, default = 0)

    #Calculated Fields
    user = models.ForeignKey(User, blank=True, null=True) #link this to a user if they have an email address
    hierarchy_score = models.IntegerField(default = 100) #parents have lower score, children have higher

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)



    def __init__(self, *args, **kwargs):
        '''
        Initialization of object
        Keeps track of original values in initialization
        '''
        super(Person, self).__init__(*args, **kwargs)
        self._original_email = self.email


    def is_valid_email(self,email):
        '''
        Tests if valid email address using regular expression
        (from http://stackoverflow.com/questions/8022530/python-check-for-valid-email-address
        and http://stackoverflow.com/questions/201323/using-a-regular-expression-to-validate-an-email-address)
        '''
        import re
        if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return True
        else:
            return False


    def create_update_user(self):
        '''
        Creates a django user if an email address is supplied with  Person
        '''
        #No email, then don't create a user
        if len(self.email) == 0 or not self.is_valid_email(self.email):
            return


        if User.objects.filter(username = self.email).count() == 0:

            if not self.is_valid_email(self._original_email) or User.objects.filter(username = self._original_email).count() == 0:

                #Create a new user
                user = User(username=self.email,
                            email=self.email,
                            password=User.objects.make_random_password(length=8))

                user.save()


            else:
                #Update existing user
                user = User.objects.get(username = self._original_email)
                user.username = self.email
                user.email = self.email
                user.save()

            self.user = user


    def save(self, *args, **kwargs):
        '''
        Overrides the save method to determine the calculated fields
        '''
        self.create_update_user()
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
            #Orphaned!
            raise Exception("Orphaned person!")

        return relation
