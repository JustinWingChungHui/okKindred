from django.db import models
from family_tree.models.person import Person
from django.conf import settings

class Biography(models.Model):

    class Meta:
        #Allows models.py to be spp[lit up across multiple files
        app_label = 'family_tree'

        #Allows one biog per person per language
        unique_together = (('person', 'language'),)

    #Fields
    person = models.ForeignKey(Person, null = False, blank = False, db_index = True)
    language = models.CharField(max_length=5, choices=settings.LOCALES, null = False, blank = False, db_index = True)
    content = models.TextField(null = True, blank = True)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)



