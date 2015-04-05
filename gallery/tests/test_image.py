from django.test import TestCase
from gallery.models import Image, Gallery
from family_tree.models import Family
from django.conf import settings
from django.utils.timezone import utc
import os
import shutil
import PIL
from datetime import datetime


class ImageTestCase(TestCase):
    '''
    Tests for the image class
    '''

    def setUp(self):
        '''
        Need to create a family and a gallery
        '''
        self.family = Family()
        self.family.save()

        self.gallery = Gallery.objects.create(title="test_gallery", family_id=self.family.id)

        self.test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

    def test_create_thumbnail(self):
        '''
        Tests that we can create a thumbnail
        '''
        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        image = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))

        thumbnail, image = image._create_thumbnail((500,500))

        PIL.Image.open(settings.MEDIA_ROOT + thumbnail)

        #Clear up mess afterwards
        os.remove(self.test_image_destination)
        os.remove(settings.MEDIA_ROOT +thumbnail)


    def test_make_thumbnails_and_delete(self):
        '''
        Tests the make thumbnails routine
        '''
        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)
        image = Image(gallery=self.gallery, family=self.family, original_image=self.test_image_destination)
        image.make_thumbnails()

        PIL.Image.open(settings.MEDIA_ROOT+ str(image.thumbnail))
        PIL.Image.open(settings.MEDIA_ROOT + str(image.large_thumbnail))
        PIL.Image.open(settings.MEDIA_ROOT +str(self.gallery.thumbnail))

        #Clear up mess afterwards
        image.delete_image_files()


    def test_get_exif_data(self):
        '''
        Tests we can extract gps data from an image
        '''
        exif_test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/exif_test.jpg')
        exif_test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/exif_test.jpg'])
        shutil.copy2(exif_test_image, exif_test_image_destination)

        image = Image(gallery=self.gallery, family=self.family, original_image=exif_test_image_destination)
        values = image._get_exif()

        self.assertEqual(True, 'DateTimeOriginal' in values)
        self.assertEqual(True, 'GPSInfo' in values)

        image._populate_exif_data()

        self.assertEqual(datetime(2014, 3, 30, 13, 18, 6).replace(tzinfo=utc), image.date_taken)
        self.assertEqual(True, image.latitude != 0)
        self.assertEqual(True, image.longitude != 0)

        #Clear up mess afterwards
        os.remove(exif_test_image_destination)

