from django.test import TestCase
from gallery.models import Image, Gallery
from family_tree.models import Family
from django.conf import settings
import os
import shutil
import PIL

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

        thumbnail = settings.MEDIA_ROOT + image._create_thumbnail((500,500))

        PIL.Image.open(thumbnail)

        #Clear up mess afterwards
        os.remove(self.test_image_destination)
        os.remove(thumbnail)


    def test_make_thumbnails(self):
        '''
        Tests themake thumbnails routine
        '''
        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)
        image = Image(gallery=self.gallery, family=self.family, original_image=self.test_image_destination)
        image.make_thumbnails()

        PIL.Image.open(settings.MEDIA_ROOT+ str(image.thumbnail))
        PIL.Image.open(settings.MEDIA_ROOT + str(image.large_thumbnail))
        PIL.Image.open(settings.MEDIA_ROOT +str(self.gallery.thumbnail))


