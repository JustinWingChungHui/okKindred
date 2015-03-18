from django.db import models
from gallery.models import Image


class Tag(models.Model):
    '''
    Represents a family meber tag in an image
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'gallery'


    image = models.ForeignKey(Image, blank=False, null=False, db_index = True)
    person = models.ForeignKey('family_tree.Person', null=False, db_index = True) #Use of model string name to prevent circular import

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