from django.db import models

class Gallery(models.model):
    '''
    Represents a gallery object uses some principes from
    https://github.com/jdriscoll/django-photologue/blob/master/photologue/models.py
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'gallery'
        verbose_name_plural = "Galleries"
        unique_together = (('title', 'family'),)

    title = models.CharField(max_length=50)
    family = models.ForeignKey('family_tree.Family', null=False, db_index = True) #Use of model string name to prevent circular import

    description = models.TextField(blank=True)


    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
