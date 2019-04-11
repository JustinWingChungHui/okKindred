from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient
import json

from family_tree.models.family import Family
from family_tree.models.person import Person
from custom_user.models import User

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class PersonApiTestCase(TestCase):
    '''
    Tests for the person API
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='adalovelace@example.com',
                                        password='algorithm',
                                        name='Ada Lovelace',
                                        family = self.family)

        self.person = Person(name='Ada Lovelace',
                        gender='F',
                        email='adalovelace@example.com',
                        family_id=self.family.id,
                        language='en',
                        user_id=self.user.id)
        self.person.save()

        self.family2 = Family()
        self.family2.save()

        self.user2 = User.objects.create_user(email='evillovelace@example.com',
                                        password='hacker',
                                        name='Evil Lovelace',
                                        family = self.family2)

        super(PersonApiTestCase, self).setUp()


    def test_list_requires_authentication(self):
        client = APIClient()
        response = client.get('/api/person/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list(self):
        client = APIClient()

        # Check this works with JWT token
        auth_details = {
            'email': 'adalovelace@example.com',
            'password': 'algorithm'
        }
        auth_response = client.post('/api/auth/obtain_token/', auth_details, format='json')
        token = json.loads(auth_response.content)["access"]

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/api/person/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'Ada Lovelace' in response.content)


    def test_list_other_family(self):
        client = APIClient()

        # Check this works with JWT token
        auth_details = {
            'email': 'evillovelace@example.com',
            'password': 'hacker'
        }
        auth_response = client.post('/api/auth/obtain_token/', auth_details, format='json')

        token = json.loads(auth_response.content)["access"]

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/api/person/', format='json')

        self.assertFalse(b'Ada Lovelace' in response.content)


    def test_retrieve_requires_authentication(self):
        client = APIClient()
        url = '/api/person/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = '/api/person/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'Ada Lovelace' in response.content)

    def test_retrieve_other_family(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        url = '/api/person/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

