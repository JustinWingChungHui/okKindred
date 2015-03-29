from django.test import TestCase
from custom_user.models import User
from gallery.models import Gallery, Image
from family_tree.models import Family
from django.test.utils import override_settings
from django.conf import settings
from django.core import serializers
import os
import shutil

@override_settings(SSLIFY_DISABLE=True)
class TestImageViews(TestCase):
    '''
    Test class for the gallery views
    '''

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='badger@queenonline.com', password='save the badgers', name='badger', family_id=self.family.id)

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
            self.images.append  (
                                Image(
                                    gallery=self.gallery,
                                    family=self.family,
                                    original_image=self.test_image_destination,
                                    thumbnail=self.test_image_destination,
                                    large_thumbnail=self.test_image_destination
                                    )
                                )

        self.another_family = Family.objects.create()
        self.another_user = User.objects.create_user(email='weebl@queenonline.com', password='mushroom', name='weebl', family_id=self.another_family.id)

    def test_gallery_loads(self):
        '''
        Tests the gallery view loads and uses the correct template
        '''

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/gallery.html')


    def test_gallery_does_not_load_for_another_family(self):
        '''
        Tests gallery does not lad for another family
        '''
        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.get('/gallery={0}/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 404)


    def test_first_page_of_images_loaded(self):
        '''
        Tests that the images load for a gallery
        '''
        for i in self.images:
            i.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/image_data=1/'.format(self.gallery.id))

        #Clear up
        for i in self.images:
            i.delete()

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, b'test_image.jpg' in response.content)

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)


    def test_second_page_of_images_loaded(self):
        '''
        Tests that the images load for page 2 of a gallery
        '''
        for i in self.images:
            i.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/image_data=1/'.format(self.gallery.id))

        #Clear up
        for i in self.images:
            i.delete()

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, b'test_image.jpg' in response.content)

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)


    def test_images_cannot_be_seen_by_another_family(self):
        '''
        Tests that the images cannot be loaded by someone form another family
        '''
        another_family = Family.objects.create()
        User.objects.create_user(email='chris_lintott@queenonline.com', password='bang', name='Chris Lintott', family_id=another_family.id)

        self.client.login(email='chris_lintott@queenonline.com', password='bang')
        response = self.client.get('/gallery={0}/image_data=1/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 404)


    def test_upload_images_view_loads(self):
        '''
        Tests that the upload images view loads
        '''

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/upload_images/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 200)


    def test_upload_images_view_does_not_load_for_another_family(self):
        '''
        Tests that the upload images view loads
        '''

        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.get('/gallery={0}/upload_images/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 404)