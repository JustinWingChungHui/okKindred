from django.test import TestCase
from custom_user.models import User
from gallery.models import Gallery, Image
from family_tree.models import Family
from django.test.utils import override_settings
from django.conf import settings
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@override_settings(SSLIFY_DISABLE=True,
                    MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
                    MEDIA_URL=settings.MEDIA_URL_TEST,
                    AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST,)
class TestGallery(TestCase): # pragma: no cover
    '''
    Test class for the gallery object
    '''

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='arif_mardin:@queenonline.com', password='Staying Power', name='Arif Mardin:', family_id=self.family.id)

        self.gallery = Gallery.objects.create(family_id=self.family.id, title="gallery")

        self.test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        self.images = []

        for i in range(0,20):
            self.images.append(
                                Image(
                                    gallery=self.gallery,
                                    family=self.family,
                                    original_image=self.test_image_destination,
                                    thumbnail=self.test_image_destination,
                                    large_thumbnail=self.test_image_destination
                                    )
                                )

    def test_delete_all_images(self):
        '''
        Tests we can delete all images associated with gallery
        '''
        for i in range(0,20):
            self.images[i].save()

        self.gallery.delete_all_images()

        self.assertEqual(0, Image.objects.filter(gallery_id = self.gallery.id).count())




