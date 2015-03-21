from django.db import models
from gallery.models import Gallery
from common import create_hash
from django.conf import settings
import PIL
import os


# look at http://stackoverflow.com/questions/23977483/fit-images-with-different-aspect-ratios-into-multiple-rows-evenly
#Look to add comments?
#http://django-contrib-comments.readthedocs.org/en/latest/

def upload_to(instance, filename):
    '''
    Defines a dynamic directory for files to be uploaded to
    http://stackoverflow.com/questions/6350153/getting-username-in-imagefield-upload-to-path
    '''
    directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(instance.family_id), '/', str(instance.gallery.id)])
    if not os.path.exists(directory):
        os.makedirs(directory)

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

        #Need to call save first before making thumbnails so image path is set properly
        super(Image, self).save(*args, **kwargs) # Call the "real" save() method.

        self.make_thumbnails()
        super(Image, self).save(*args, **kwargs) # Call the "real" save() method.


    def make_thumbnails(self):
        '''
        Creates the thumbnails for the images
        It also sets a thumbnail for the gallery if none exists
        '''
        if not self.original_image:
            return

        if not self.thumbnail:
            self.thumbnail = self._create_thumbnail((200,200))

        if not self.large_thumbnail:
            self.large_thumbnail = self._create_thumbnail((960,960))

        #Set the gallery thumbnail
        if not self.gallery.thumbnail:
            self.gallery.thumbnail =  self.thumbnail
            self.gallery.save()



    def _create_thumbnail(self, size):
        '''
        Creates the thumbnails
        '''

        if settings.MEDIA_ROOT in str(self.original_image):
            image_file = str(self.original_image)
        else:
            image_file = settings.MEDIA_ROOT + str(self.original_image)

        im = PIL.Image.open(image_file)
        im.thumbnail(size)

        filename = create_hash(str(self.original_image)) + '.jpg'
        path_and_filename = upload_to(self, filename)

        im.save(settings.MEDIA_ROOT + path_and_filename, "JPEG", quality=90)

        return path_and_filename





