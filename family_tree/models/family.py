from django.db import models

class Family(models.Model):
    '''
    Model that represents a family allows website to be used by more than one family
    '''
    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'family_tree'
        verbose_name_plural = "Families"

    description = models.CharField(max_length=255, null = False, blank = True)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self): # __unicode__ on Python 2
        return self.description