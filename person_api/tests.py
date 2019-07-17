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

        self.person2 = Person(name='Evil Lovelace',
                        gender='M',
                        email='evillovelace@example.com',
                        family_id=self.family2.id,
                        language='en',
                        user_id=self.user2.id)
        self.person2.save()

        super(PersonApiTestCase, self).setUp()


    def test_list_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        response = client.get('/api/person/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

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
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

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

    def test_list_search_match(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/person/?search=ada'
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'Ada Lovelace' in response.content)

    def test_list_search_no_match(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/person/?search=asfasfasfa'
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(b'Ada Lovelace' in response.content)


    def test_retrieve_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/person/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_retrieve(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/person/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'Ada Lovelace' in response.content)


    def test_retrieve_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user2)
        url = '/api/person/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'fieldName': 'name',
            'value': 'Ada Lovelace II'
        }

        url = '/api/person/{0}/'.format(self.person.id)
        response = client.put(url, data, format='json')

        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'Ada Lovelace II' in response.content)
        self.assertEqual('Ada Lovelace II', self.person.name)


    def test_update_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user2)

        data = {
            'fieldName': 'name',
            'value': 'Ada Lovelace II'
        }

        url = '/api/person/{0}/'.format(self.person.id)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_locked(self):

        locked_person = Person(name='Locked Person',
                        gender='O',
                        email='locked_person@example.com',
                        family_id=self.family.id,
                        language='en',
                        locked=True)
        locked_person.save()

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'fieldName': 'name',
            'value': 'troll time!'
        }

        url = '/api/person/{0}/'.format(locked_person.id)
        response = client.put(url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_field_not_whitelisted(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'fieldName': 'creation_date',
            'value': '2001-01-01'
        }

        url = '/api/person/{0}/'.format(self.person.id)
        response = client.put(url, data, format='json')

        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_update_email_for_other_user(self):

        user = User.objects.create_user(email='adahorriblecousin@example.com',
                                        password='horrible',
                                        name='Ada Horrible Cousin',
                                        family = self.family)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=user)

        data = {
            'fieldName': 'email',
            'value': 'NOTadalovelace@example.com'
        }

        url = '/api/person/{0}/'.format(self.person.id)
        response = client.put(url, data, format='json')

        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

