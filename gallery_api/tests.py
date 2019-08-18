from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from family_tree.models.family import Family
from family_tree.models.person import Person
from custom_user.models import User
from gallery.models import Gallery
import json

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
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


    def test_list_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        response = client.get('/api/gallery/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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


    def test_retrieve_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user2)
        url = '/api/gallery/{0}/'.format(self.gallery.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)