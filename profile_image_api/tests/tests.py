from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from rest_framework import status
from rest_framework.test import APIClient
from custom_user.models import User
from family_tree.models import Person, Family

import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@override_settings(
    SECURE_SSL_REDIRECT = False,
    MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
    AXES_BEHIND_REVERSE_PROXY = False)
class ProfileImageApiTestCase(TestCase):

    def setUp(self):
        '''
        Set up a family, user and profile to test with
        '''

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='fairy_fellar@email.com', password='masterstroke', name='Fairy Fellar', family_id = self.family.id)
        self.user.save()

        self.person = Person.objects.create(name='Fairy Fellar', gender='M', user_id=self.user.id, email='fairy_fellar@email.com', family_id=self.family.id)
        self.person.save()

        self.another_family = Family()
        self.another_family.save()
        self.another_user = User.objects.create_user(email='dale_arden@email.com', password="flash i love you", name='Dale Arden', family_id=self.another_family.id)
        self.another_user.save()

        self.image_path = os.path.join(BASE_DIR, 'tests/large_test_image.jpg')


    def test_image_upload_successful(self):
        '''
        test that we can upload a file
        '''
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        url = '/api/profile_image/{0}/'.format(self.person.id)
        with open(self.image_path, 'rb') as fp:

            data = {
                'picture': fp,
                'x': 100,
                'y': 200,
                'w': 300,
                'h': 300,
                'r': 90,
            }

            response = client.put(url, data)

        self.assertEqual(200, response.status_code)

        # Clear up remote images
        person =  Person.objects.get(id=self.person.id)
        json.loads(response.content)

        person.remove_local_images()
        person.remove_remote_images()


    def test_image_upload_without_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/profile_image/{0}/'.format(self.person.id)

        with open(self.image_path, 'rb') as fp:

            data = {
                'picture': fp,
                'x': 100,
                'y': 200,
                'w': 300,
                'h': 300,
                'r': 90,
            }

            response = client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_image_upload_other_family(self):
        '''
        test that we can upload a file
        '''
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.another_user)

        url = '/api/profile_image/{0}/'.format(self.person.id)
        with open(self.image_path, 'rb') as fp:

            data = {
                'picture': fp,
                'x': 100,
                'y': 200,
                'w': 300,
                'h': 300,
                'r': 90,
            }

            response = client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_image_upload_invalid_parameter(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/profile_image/{0}/'.format(self.person.id)

        with open(self.image_path, 'rb') as fp:

            data = {
                'picture': fp,
                'x': 'blah',
                'y': 200,
                'w': 300,
                'h': 300,
                'r': 90,
            }

            response = client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)



    def test_image_upload_invalid_picture(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/profile_image/{0}/'.format(self.person.id)

        image_path = os.path.join(BASE_DIR, 'tests/test_not_a_real_picture.png')

        with open(image_path, 'rb') as fp:

            data = {
                'picture': fp,
                'x': 100,
                'y': 200,
                'w': 300,
                'h': 300,
                'r': 90,
            }

            response = client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)

