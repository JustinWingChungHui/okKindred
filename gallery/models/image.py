from django.db import models
from gallery.models import Gallery

# look at http://stackoverflow.com/questions/23977483/fit-images-with-different-aspect-ratios-into-multiple-rows-evenly
#Look to add comments?
#http://django-contrib-comments.readthedocs.org/en/latest/

def upload_to(instance, filename):
    '''
    Defines a dynamic directory for files to be uploaded to
    http://stackoverflow.com/questions/6350153/getting-username-in-imagefield-upload-to-path
    '''
    return 'galleries/%s/%s/%s' % (instance.family_id,instance.gallery.id,filename)


class Image(models.Model):
    '''
    Represents an image uploaded to a gallery
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'gallery'


    gallery = models.ForeignKey(Gallery, blank=False, null=False, db_index = True)
    family = models.ForeignKey('family_tree.Family', null=False, db_index=True) #Use of model string name to prevent circular import

    original_image = models.ImageField(upload_to=upload_to, blank=True, null=False)
    thumbnail = models.ImageField(upload_to=upload_to, blank=True, null=False)
    large_thumbnail = models.ImageField(upload_to=upload_to, blank=True, null=False)

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    #EXIF data
    date_taken = models.DateTimeField(null=True, blank=True, db_index = True)
    latitude = models.FloatField(blank=True, null=False, default = 0) #(0,0) is in the middle of the ocean so can set this to 0 to avoid nulls
    longitude = models.FloatField(blank=True, null=False, default = 0)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self): # __unicode__ on Python 2
        return self.title


    def save(self, *args, **kwargs):
        '''
        Overrides the save method
        '''
        self.family_id = self.gallery.family_id

        if not self.thumbnail:
            self._create_thumbnail(200)

        if not self.large_thumbnail:
            self._create_thumbnail(960)

        super(Image, self).save(*args, **kwargs) # Call the "real" save() method.


    def _create_thumbnail(self, size):
        '''
        Creates the thumbnails
        '''





