from django.db import models
from gallery.models import Gallery
from common.utils import create_hash
from common.get_lat_lon_exif_pil import get_lat_lon_backup
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

    return 'galleries/%s/%s/%s' % (instance.family_id, instance.gallery.id, filename)


class Image(models.Model):
    '''
    Represents an image uploaded to a gallery
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'gallery'


    gallery = models.ForeignKey(Gallery, blank=False, null=False, db_index = True)
    family = models.ForeignKey('family_tree.Family', null=False, db_index=True) #Use of model string name to prevent circular import

    original_image = models.ImageField(upload_to=upload_to, blank=True, null=False, width_field='original_image_width', height_field='original_image_height')
    original_image_height = models.IntegerField(null=True)
    original_image_width = models.IntegerField(null=True)

    thumbnail = models.ImageField(upload_to=upload_to, blank=True, null=False, width_field='thumbnail_width', height_field='thumbnail_height')
    thumbnail_height = models.IntegerField(null=True)
    thumbnail_width = models.IntegerField(null=True)

    large_thumbnail = models.ImageField(upload_to=upload_to, blank=True, null=False, width_field='large_thumbnail_width', height_field='large_thumbnail_height')
    large_thumbnail_height = models.IntegerField(null=True)
    large_thumbnail_width = models.IntegerField(null=True)

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

        if self.id is None or self.id <= 0:
            new_record = True
        else:
            new_record = False

        #Need to call save first before making thumbnails so image path is set properly
        super(Image, self).save(*args, **kwargs) # Call the "real" save() method.

        # Don't need to do the rest if editing existing image
        if new_record == False:
            return

        im = PIL.Image.open(self._get_absolute_image_path())

        self._populate_exif_data(im)
        self.make_thumbnails(im)

        #Set last updated data on Gallery
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
        path_and_filename = upload_to(self, str(filename))

        image.save(settings.MEDIA_ROOT + str(path_and_filename), "JPEG", quality=90)

        return path_and_filename, image


    def _get_absolute_image_path(self, path = None):
        '''
        Gets the absolute image path
        '''
        if not path:
            path = self.original_image

        if settings.MEDIA_ROOT in str(path):
            image_file = str(path)
        else:
            image_file = settings.MEDIA_ROOT + str(path)

        return image_file


    def _populate_exif_data(self, image=None):
        '''
        Uses the exif data from an image to populate fields on the image model
        http://stackoverflow.com/questions/6460381/translate-exif-dms-to-dd-geolocation-with-python
        '''

        if self.latitude != 0 and self.longitude != 0:
            return

        if not image:
            image = PIL.Image.open(self._get_absolute_image_path())

        # Issue with PIL GPS tag reading so using another library
        lat, lon, date_time = get_lat_lon_backup(self._get_absolute_image_path())

        self.latitude = lat
        self.longitude = lon
        self.date_taken = date_time


    def delete_image_files(self):
        '''
        Deletes the original image and thumbails associated with this
        object
        '''
        try:
            os.remove(self._get_absolute_image_path(self.original_image))
            os.remove(self._get_absolute_image_path(self.thumbnail))
            os.remove(self._get_absolute_image_path(self.large_thumbnail))
        except:
            pass


    def rotate(self, anticlockwise_angle = 90):
        '''
        Rotates the image and all thumbnails
        '''

        thumbnail = self._rotate_image(self._get_absolute_image_path(self.thumbnail), anticlockwise_angle)
        thumbnail_path_and_filename = upload_to(self, str(create_hash(str(self.original_image)) + '.jpg'))
        thumbnail.save(settings.MEDIA_ROOT + str(thumbnail_path_and_filename), "JPEG", quality=95)

        large_thumbnail = self._rotate_image(self._get_absolute_image_path(self.large_thumbnail), anticlockwise_angle)
        large_thumbnail_path_and_filename = upload_to(self, str(create_hash(str(self.original_image)) + '.jpg'))
        large_thumbnail.save(settings.MEDIA_ROOT + str(large_thumbnail_path_and_filename), "JPEG", quality=95)

        original_image = self._rotate_image(self._get_absolute_image_path(self.original_image), anticlockwise_angle)
        original_image_path_and_filename = upload_to(self, str(create_hash(str(self.original_image)) + '.jpg'))
        original_image.save(settings.MEDIA_ROOT + str(original_image_path_and_filename), "JPEG", quality=95)

        self.delete_image_files()
        self.thumbnail = thumbnail_path_and_filename
        self.large_thumbnail = large_thumbnail_path_and_filename
        self.original_image = original_image_path_and_filename

        self.save()


    def _rotate_image(self, path, anticlockwise_angle = 90):
        '''
        Rotates an image
        '''
        image = PIL.Image.open(path)
        return image.rotate(anticlockwise_angle, resample=PIL.Image.BICUBIC, expand=True)


