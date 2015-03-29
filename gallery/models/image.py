from django.db import models
from gallery.models import Gallery
from common import create_hash
from django.conf import settings
from PIL.ExifTags import TAGS
import PIL
import os
from datetime import datetime
from django.utils.timezone import utc


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

        im = PIL.Image.open(self._get_absolute_image_path())

        self._populate_exif_data(im)
        self.make_thumbnails(im)

        #Set last updated dat on Gallery
        self.gallery.save()


        super(Image, self).save(*args, **kwargs) # Call the "real" save() method.


    def make_thumbnails(self, image=None):
        '''
        Creates the thumbnails for the images
        It also sets a thumbnail for the gallery if none exists
        '''
        if not self.original_image:
            return

        if not self.large_thumbnail:
            self.large_thumbnail, image = self._create_thumbnail((960,960))

        if not self.thumbnail:
            self.thumbnail, image = self._create_thumbnail((200,200), image)

        #Set the gallery thumbnail
        if not self.gallery.thumbnail:
            self.gallery.thumbnail =  self.thumbnail

    def _create_thumbnail(self, size, image = None):
        '''
        Creates the thumbnails
        '''
        if not image:
            image = PIL.Image.open(self._get_absolute_image_path())

        image.thumbnail(size)

        filename = create_hash(str(self.original_image)) + '.jpg'
        path_and_filename = upload_to(self, filename)

        image.save(settings.MEDIA_ROOT + path_and_filename, "JPEG", quality=90)

        return path_and_filename, image


    def _get_absolute_image_path(self):
        '''
        Gets the absolute image path
        '''
        if settings.MEDIA_ROOT in str(self.original_image):
            image_file = str(self.original_image)
        else:
            image_file = settings.MEDIA_ROOT + str(self.original_image)

        return image_file


    def _get_exif(self, image = None):
        '''
        http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/
        '''
        ret = {}

        if not image:
            image = PIL.Image.open(self._get_absolute_image_path())

        info = image._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret


    def _populate_exif_data(self, image=None):
        '''
        Uses the exif data from an image to populate fields on the image model
        http://stackoverflow.com/questions/6460381/translate-exif-dms-to-dd-geolocation-with-python
        '''

        if not image:
            image = PIL.Image.open(self._get_absolute_image_path())

        data = self._get_exif(image)

        try:
            lat = [float(x)/float(y) for x, y in data['GPSInfo'][2]]
            latref = data['GPSInfo'][1]
            lon = [float(x)/float(y) for x, y in data['GPSInfo'][4]]
            lonref = data['GPSInfo'][3]

            lat = lat[0] + lat[1]/60 + lat[2]/3600
            lon = lon[0] + lon[1]/60 + lon[2]/3600
            if latref == 'S':
                lat = -lat
            if lonref == 'W':
                lon = -lon

            self.latitude = lat
            self.longitude = lon
        except:
            pass

        try:
            self.date_taken = datetime.strptime(data['DateTimeOriginal'],"%Y:%m:%d %H:%M:%S").replace(tzinfo=utc)
        except:
            pass


