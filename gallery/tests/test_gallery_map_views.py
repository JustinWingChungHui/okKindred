from django.test import TestCase
from django.test.client import Client as HttpClient
from custom_user.models import User
from gallery.models import Gallery, Image
from family_tree.models import Family
from django.test.utils import override_settings
from django.conf import settings
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@override_settings(SECURE_SSL_REDIRECT=False, MEDIA_ROOT=settings.MEDIA_ROOT_TEST, AXES_BEHIND_REVERSE_PROXY=False)
class TestGalleryMapViews(TestCase): # pragma: no cover
    '''
    Test class for the gallery views
    '''

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.client = HttpClient(HTTP_X_REAL_IP='127.0.0.1')

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='gromit@aardman.com', password='cheese', name='gromit', family_id=self.family.id)

        self.gallery = Gallery.objects.create(family_id=self.family.id, title="gallery")

        self.test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        self.images = []

        for i in range(0,3):
            self.images.append  (
                                Image(
                                    gallery=self.gallery,
                                    family=self.family,
                                    title="title{0}".format(i),
                                    original_image=self.test_image_destination,
                                    thumbnail=self.test_image_destination,
                                    large_thumbnail=self.test_image_destination,
                                    latitude=i,
                                    longitude=i
                                    )
                                )

        self.another_family = Family.objects.create()
        self.another_user = User.objects.create_user(email='shaun@aardman.com', password='baaa', name='shaun', family_id=self.another_family.id)


    def test_gallery_map_loads(self):
        '''
        Tests the gallery map view loads and uses the correct template
        '''

        self.client.post('/accounts/auth/',  {'username': 'gromit@aardman.com', 'password': 'cheese'})
        response = self.client.get('/gallery={0}/map/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/gallery_map.html')


    def test_gallery_map_does_not_load_for_another_family(self):
        '''
        Tests gallery does not load for another family
        '''
        self.client.post('/accounts/auth/',  {'username': 'shaun@aardman.com', 'password': 'baaa'})
        response = self.client.get('/gallery={0}/map/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 404)


    def test_gallery_map_data_does_not_load_another_family(self):
        '''
        Tests gallery data does not load for another family
        '''
        self.client.post('/accounts/auth/',  {'username': 'shaun@aardman.com', 'password': 'baaa'})
        response = self.client.get('/gallery={0}/map_data/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 404)


    def test_gallery_map_data_loads(self):
        '''
        Tests gallery data loads
        '''
        for i in self.images:
            i.save()

        self.client.post('/accounts/auth/',  {'username': 'gromit@aardman.com', 'password': 'cheese'})
        response = self.client.get('/gallery={0}/map_data/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, b'title' in response.content)





