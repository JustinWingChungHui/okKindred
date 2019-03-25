from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient

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

        self.user = User.objects.create(email='adalovelace@example.com',
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

        super(PersonApiTestCase, self).setUp()


    def test_list_requires_authentication(self):
        client = APIClient()
        response = client.get('/api/person/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/person/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'Ada Lovelace' in response.content)

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
