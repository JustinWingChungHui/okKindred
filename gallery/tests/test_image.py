from django.test import TestCase
from gallery.models import Image, Gallery
from family_tree.models import Family
from django.conf import settings
from django.test.utils import override_settings
from datetime import timezone
import os
import shutil
import PIL
from datetime import datetime

@override_settings(SECURE_SSL_REDIRECT=False,
                MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
                MEDIA_URL=settings.MEDIA_URL_TEST,
                AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST,)
class ImageTestCase(TestCase): # pragma: no cover
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
        self.test_image_s3_key = ''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        self.test_png = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image2.png')
        self.test_png_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image2.png'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)


    def tearDown(self):
        try:
            os.remove(self.test_image_destination)
        except:
            pass


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
        os.remove(settings.MEDIA_ROOT + thumbnail)


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
        image.delete_local_image_files()
        image.delete_remote_image_files()


    def test_get_exif_data(self):
        '''
        Tests we can extract gps data from an image
        '''
        exif_test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/exif_test.jpg')
        exif_test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/exif_test.jpg'])
        shutil.copy2(exif_test_image, exif_test_image_destination)

        image = Image(gallery=self.gallery, family=self.family, original_image=exif_test_image_destination)

        image._populate_exif_data()

        self.assertEqual(datetime(2014, 3, 30, 13, 18, 6).replace(tzinfo=timezone.utc), image.date_taken)
        self.assertEqual(True, image.latitude != 0)
        self.assertEqual(True, image.longitude != 0)

        #Clear up mess afterwards
        os.remove(exif_test_image_destination)
        image.delete_local_image_files()
        image.delete_remote_image_files()

    def test_get_exif_data2(self):
        '''
        Tests we can extract gps data from an image
        '''
        exif_test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/exif_test_2.jpg')
        exif_test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/exif_test_2.jpg'])
        shutil.copy2(exif_test_image, exif_test_image_destination)

        image = Image(gallery=self.gallery, family=self.family, original_image=exif_test_image_destination)

        image._populate_exif_data()

        self.assertEqual(datetime(2015, 6, 21, 13, 50, 35).replace(tzinfo=timezone.utc), image.date_taken)
        self.assertEqual(True, image.latitude != 0)
        self.assertEqual(True, image.longitude != 0)

        #Clear up mess afterwards
        os.remove(exif_test_image_destination)
        image.delete_local_image_files()
        image.delete_remote_image_files()

    def test_save_and_rotate_image(self):
        '''
        Tests that we can save an image and rotate it without error
        '''

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        image = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        image.save()
        image.upload_files_to_s3()

        image.rotate(90)

        #Clear up
        image.delete_local_image_files()
        image.delete_remote_image_files()

    def test_save_png(self):
        #Copy test image to media area
        shutil.copy2(self.test_png, self.test_png_destination)

        image = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image2.png']))
        image.save()
        image.upload_files_to_s3()

        image.rotate(90)

        #Clear up
        image.delete_local_image_files()
        image.delete_remote_image_files()

