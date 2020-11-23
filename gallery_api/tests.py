from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from family_tree.models.family import Family
from family_tree.models.person import Person
from custom_user.models import User
from gallery.models import Gallery, Image
import json
import os
import shutil

@override_settings(SECURE_SSL_REDIRECT=False,
                    AXES_BEHIND_REVERSE_PROXY=False,
                    MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
                    AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST)
class GalleryApiTestCase(TestCase):
    '''
    Tests for the Gallery API
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='philcollins@example.com',
                                        password='easylover',
                                        name='Phil Collins',
                                        family = self.family)

        self.person = Person(name='Phil Collins',
                        gender='M',
                        email='philcollins@example.com',
                        family_id=self.family.id,
                        language='en',
                        user_id=self.user.id)
        self.person.save()

        self.gallery = Gallery.objects.create(title="test_gallery", family_id=self.family.id)

        self.gallery2 = Gallery.objects.create(title="test_gallery2", family_id=self.family.id)


        self.family2 = Family()
        self.family2.save()

        self.user2 = User.objects.create_user(email='phillipbailey@example.com',
                                        password='BetterForgetIt',
                                        name='Phillip Bailey',
                                        family = self.family2)

        self.person2 = Person(name='Phillip Bailey',
                        gender='M',
                        email='phillipbailey@example.com',
                        family_id=self.family2.id,
                        language='en',
                        user_id=self.user2.id)
        self.person2.save()

        self.test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)


    def tearDown(self):

        try:
            os.remove(self.test_image_destination)
        except:
            pass



    def test_list_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        response = client.get('/api/gallery/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_list_page1(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        # Check this works with JWT token
        auth_details = {
            'email': 'philcollins@example.com',
            'password': 'easylover'
        }
        auth_response = client.post('/api/auth/obtain_token/', auth_details, format='json')
        token = json.loads(auth_response.content)["access"]

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/api/gallery/', format='json')

        # Check it contains both galleries
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(self.gallery.title).encode() in response.content)
        self.assertTrue(str(self.gallery2.title).encode() in response.content)
        json.loads(response.content)


    def test_list_page1_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        # Login with other user
        auth_details = {
            'email': 'phillipbailey@example.com',
            'password': 'BetterForgetIt'
        }
        auth_response = client.post('/api/auth/obtain_token/', auth_details, format='json')
        token = json.loads(auth_response.content)["access"]

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/api/gallery/', format='json')

        # Check it contains neither galleries
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(str(self.gallery.title).encode() in response.content)
        self.assertFalse(str(self.gallery2.title).encode() in response.content)
        json.loads(response.content)



    def test_retrieve_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/gallery/{0}/'.format(self.gallery.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_retrieve(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/gallery/{0}/'.format(self.gallery.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(self.gallery.title).encode() in response.content)
        json.loads(response.content)


    def test_retrieve_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user2)
        url = '/api/gallery/{0}/'.format(self.gallery.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_partial_update(self):
        shutil.copy2(self.test_image, self.test_image_destination)

        image = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        image.save()

        image2 = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        image2.save()

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/gallery/{0}/'.format(self.gallery.id)

        data = {
            'family_id': self.family2.id, # try to switch families
            'title': 'new title',
            'description': 'new description',
            'thumbnail_id': image2.id,
        }

        response = client.patch(url, data, format='json')

        gallery = Gallery.objects.get(id=self.gallery.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new title', gallery.title)
        self.assertEqual(self.family.id, gallery.family_id)
        self.assertTrue(b'new title' in response.content)
        self.assertTrue(b'new description' in response.content)
        self.assertTrue(str(image2.thumbnail) in response.content.decode("utf-8"))
        json.loads(response.content)

        image.delete_local_image_files()
        image.delete_remote_image_files()
        image2.delete_local_image_files()
        image2.delete_remote_image_files()


    def test_partial_update_remove_thumbnail(self):

        shutil.copy2(self.test_image, self.test_image_destination)
        image = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        image.save()

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/gallery/{0}/'.format(self.gallery.id)

        data = {
            'thumbnail_id': '',
        }

        response = client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('"thumbnail":null' in response.content.decode("utf-8"))
        json.loads(response.content)

        image.delete_local_image_files()
        image.delete_remote_image_files()

    def test_partial_update_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        url = '/api/gallery/{0}/'.format(self.gallery.id)

        data = {
            'title': 'new title',
            'description': 'new description',
            'thumbnail': 'test_image.jpg',
        }

        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_partial_update_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user2)

        data = {
            'title': 'new title',
            'description': 'new description',
            'thumbnail': 'test_image.jpg',
        }

        url = '/api/gallery/{0}/'.format(self.gallery.id)
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_create(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/gallery/'

        data = {
            'family_id': self.family2.id, # try to switch families
            'title': 'new gallery title',
            'description': 'new gallery description',
        }

        response = client.post(url, data, format='json')

        gallery = Gallery.objects.get(title='new gallery title')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new gallery title', gallery.title)
        self.assertEqual(self.family.id, gallery.family_id)
        self.assertTrue(b'new gallery title' in response.content)
        json.loads(response.content)


    def test_create_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        url = '/api/gallery/'.format(self.gallery.id)

        data = {
            'title': 'new title',
            'description': 'new description',
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)



    def test_create_no_title(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/gallery/'

        data = {
            'title': '',
            'description': 'new gallery description',
        }

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)
