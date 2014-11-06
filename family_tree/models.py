from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Other'),
)


class Person(models.model):
    '''
    Represents a family member
    Most fields are nullable as a lot of information will be incomplete or private
    '''

    #Only required fields
    name = models.CharField(max_length=255, db_index = True, null = False, blank = False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null = False, blank = False)

    #Optional Fields
    birth_year = models.IntegerField(blank=True, null=True)
    year_of_death = models.IntegerField(blank=True, null=True)

    picture = models.ImageField(blank=True, null=True)
    email =  models.CharField(max_length=100, blank=True, null=True)
    telephone_number = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)


    #Location use https://pypi.python.org/pypi/googlemaps?
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    #Calculated Fields
    user = models.ForeignKey(User, blank=True, null=True) #link this to a user if they have an email address
    deceased = models.BooleanField(default = False)
    hierarchy_score = birth_year = models.IntegerField(default = 100) #parents have lower score, children have higher
